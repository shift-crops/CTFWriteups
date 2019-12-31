// Copyright 2018 The Fuchsia Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <iostream>
#include <memory>
#include <string>
#include <type_traits>
#include <vector>

#include <lib/async-loop/cpp/loop.h>
#include <lib/async-loop/default.h>
#include <lib/async/cpp/wait.h>
#include <lib/async/default.h>
#include <lib/fdio/fd.h>
#include <lib/fdio/fdio.h>
#include <lib/fdio/io.h>
#include <lib/fdio/spawn.h>
#include <lib/zx/job.h>
#include <lib/zx/process.h>
#include <zircon/process.h>
#include <zircon/processargs.h>
#include <zircon/types.h>
#include "lib/fsl/tasks/fd_waiter.h"
#include "lib/zx/channel.h"
#include "src/lib/fxl/logging.h"
#include "src/lib/fxl/macros.h"
#include "src/lib/fxl/strings/string_printf.h"

constexpr zx_rights_t kChildJobRights =
    ZX_RIGHTS_BASIC | ZX_RIGHTS_IO | ZX_RIGHT_DESTROY | ZX_RIGHT_MANAGE_JOB;

const auto kProgramPath = "/pkg/bin/caidanti";
const auto kServicePath = "/pkg/bin/caidanti-storage-service";
const char* kProgramArgv[] = {kProgramPath, nullptr};
const char* kServiceArgv[] = {kServicePath, nullptr};

zx_status_t make_child_job(const zx::job& parent, std::string name, zx::job* job) {
  zx_status_t s;
  if ((s = zx::job::create(parent, 0, job)) != ZX_OK) {
    FXL_PLOG(ERROR, s) << "Failed to create child job; parent = " << parent.get();
    return s;
  }

  if ((s = job->set_property(ZX_PROP_NAME, name.data(), name.size())) != ZX_OK) {
    FXL_PLOG(ERROR, s) << "Failed to set name of child job; job = " << job->get();
    return s;
  }
  if ((s = job->replace(kChildJobRights, job)) != ZX_OK) {
    FXL_PLOG(ERROR, s) << "Failed to set rights on child job; job = " << job->get();
    return s;
  }

  return ZX_OK;
}

class Service {
 public:
  explicit Service(int port) : port_(port) {
    sock_ = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
    if (sock_ < 0) {
      FXL_LOG(ERROR) << "Failed to create socket: " << strerror(errno);
      exit(1);
    }

    const struct sockaddr_in6 addr {
      .sin6_family = AF_INET6, .sin6_port = htons(port_), .sin6_addr = in6addr_any,
    };
    if (bind(sock_, reinterpret_cast<const sockaddr*>(&addr), sizeof addr) < 0) {
      FXL_LOG(ERROR) << "Failed to bind to " << port_ << ": " << strerror(errno);
      exit(1);
    }

    if (listen(sock_, 10) < 0) {
      FXL_LOG(ERROR) << "Failed to listen: " << strerror(errno);
      exit(1);
    }

    std::string job_name = fxl::StringPrintf("tcp:%d", port);
    if (make_child_job(*zx::job::default_job(), job_name, &job_) != ZX_OK) {
      exit(1);
    }
  
    Wait();
  }

  ~Service() {
    for (auto& waiter : process_waiters_) {
      zx_status_t s;
      if ((s = zx_task_kill(waiter->object())) != ZX_OK) {
        FXL_PLOG(ERROR, s) << "Failed kill child task";
      }
      if ((s = zx_handle_close(waiter->object())) != ZX_OK) {
        FXL_PLOG(ERROR, s) << "Failed close child handle";
      }
    }
  }

 private:
  void Wait() {
    waiter_.Wait(
        [this](zx_status_t /*success*/, uint32_t /*events*/) {
          struct sockaddr_in6 peer_addr;
          socklen_t peer_addr_len = sizeof(peer_addr);
          int conn = accept(sock_, reinterpret_cast<struct sockaddr*>(&peer_addr), &peer_addr_len);
          if (conn < 0) {
            if (errno == EPIPE) {
              FXL_LOG(ERROR) << "The netstack died. Terminating.";
              exit(1);
            } else {
              FXL_LOG(ERROR) << "Failed to accept: " << strerror(errno);
              // Wait for another connection.
              Wait();
            }
            return;
          }
          std::string peer_name = "unknown";
          char host[32];
          char port[16];
          if (getnameinfo(reinterpret_cast<struct sockaddr*>(&peer_addr), peer_addr_len, host,
                          sizeof(host), port, sizeof(port), NI_NUMERICHOST | NI_NUMERICSERV) == 0) {
            peer_name = fxl::StringPrintf("%s:%s", host, port);
          }

          zx::channel server, client;
          FXL_CHECK(zx::channel::create(0, &server, &client) == ZX_OK);
          LaunchStorageService(std::move(server), peer_name);
          Launch(conn, std::move(client), peer_name);
          Wait();
        },
        sock_, POLLIN);
  }

  bool LaunchStorageService(zx::channel ch, const std::string& peer_name) {
    zx::job child_job;
    FXL_CHECK(zx::job::create(job_, 0, &child_job) == ZX_OK);
    FXL_CHECK(child_job.set_property(ZX_PROP_NAME, peer_name.data(), peer_name.size()) == ZX_OK);
    FXL_CHECK(child_job.replace(kChildJobRights, &child_job) == ZX_OK);
    const std::vector<fdio_spawn_action_t> actions{
        {.action = FDIO_SPAWN_ACTION_CLONE_DIR, .dir = {.prefix = "/pkg"}},
        {.action = FDIO_SPAWN_ACTION_ADD_HANDLE,
         .h = {.id = PA_HND(PA_USER0, 0), .handle = ch.release()}},
    };

    zx::process process;
    char err_msg[FDIO_SPAWN_ERR_MSG_MAX_LENGTH];
    zx_status_t status =
        fdio_spawn_etc(child_job.get(), FDIO_SPAWN_DEFAULT_LDSVC | FDIO_SPAWN_CLONE_STDIO,
                       kServiceArgv[0], kServiceArgv, nullptr, actions.size(), actions.data(),
                       process.reset_and_get_address(), err_msg);
    if (status < 0) {
      FXL_LOG(ERROR) << "Error from fdio_spawn_etc: " << err_msg;
      return false;
    }
    auto waiter = std::make_unique<async::Wait>(process.get(), ZX_PROCESS_TERMINATED);
    waiter->set_handler([this, process = std::move(process), job = std::move(child_job)](
                            async_dispatcher_t*, async::Wait*, zx_status_t status,
                            const zx_packet_signal_t* signal) mutable {
      ProcessTerminated(std::move(process), std::move(job));
    });
    waiter->Begin(async_get_default_dispatcher());
    process_waiters_.push_back(std::move(waiter));
    return true;
  }

  void Launch(int conn, zx::channel ch, const std::string& peer_name) {
    // Create a new job to run the child in.
    zx::job child_job;
    FXL_CHECK(zx::job::create(job_, 0, &child_job) == ZX_OK);
    FXL_CHECK(child_job.set_property(ZX_PROP_NAME, peer_name.data(), peer_name.size()) == ZX_OK);
    FXL_CHECK(child_job.replace(kChildJobRights, &child_job) == ZX_OK);
    // Launch process with chrealm so that it gets /svc of sys realm
    const std::vector<fdio_spawn_action_t> actions{
        // Transfer the socket as stdin and stdout and stderr
        // DEBUG: Cloned stderr
        {.action = FDIO_SPAWN_ACTION_CLONE_FD,
         .fd = {.local_fd = conn, .target_fd = STDIN_FILENO}},
        // {.action = FDIO_SPAWN_ACTION_CLONE_FD,
        {.action = FDIO_SPAWN_ACTION_TRANSFER_FD,
         .fd = {.local_fd = conn, .target_fd = STDOUT_FILENO}},
        {.action = FDIO_SPAWN_ACTION_CLONE_FD,
         .fd = {.local_fd = STDERR_FILENO, .target_fd = STDERR_FILENO}},
        {.action = FDIO_SPAWN_ACTION_ADD_HANDLE,
         .h = {.id = PA_HND(PA_USER0, 0), .handle = ch.release()}},
    };
    
    zx::process process;
    char err_msg[FDIO_SPAWN_ERR_MSG_MAX_LENGTH];

    zx_status_t status = fdio_spawn_etc(
        child_job.get(),
        FDIO_SPAWN_DEFAULT_LDSVC,
        kProgramArgv[0], kProgramArgv, nullptr, actions.size(), actions.data(),
        process.reset_and_get_address(), err_msg);

    if (status < 0) {
      shutdown(conn, SHUT_RDWR);
      close(conn);
      FXL_LOG(ERROR) << "Error from fdio_spawn_etc: " << err_msg;
      return;
    }
    std::unique_ptr<async::Wait> waiter =
        std::make_unique<async::Wait>(process.get(), ZX_PROCESS_TERMINATED);
    waiter->set_handler(
        [this, process = std::move(process), job = std::move(child_job)](
            async_dispatcher_t*, async::Wait*, zx_status_t status,
            const zx_packet_signal_t* signal) mutable {
          ProcessTerminated(std::move(process), std::move(job));
        });
    waiter->Begin(async_get_default_dispatcher());
    process_waiters_.push_back(std::move(waiter));
  }

  void ProcessTerminated(zx::process process, zx::job job) {
    zx_status_t s;

    // Kill the process and the job.
    if ((s = process.kill()) != ZX_OK) {
      FXL_PLOG(ERROR, s) << "Failed to kill child process";
    }
    if ((s = job.kill()) != ZX_OK) {
      FXL_PLOG(ERROR, s) << "Failed to kill child job";
    }

    // Find the waiter.
    auto i = std::find_if(
        process_waiters_.begin(), process_waiters_.end(),
        [&process](const std::unique_ptr<async::Wait>& w) { return w->object() == process.get(); });
    // And remove it.
    if (i != process_waiters_.end()) {
      process_waiters_.erase(i);
    }
  }

  int port_;
  int sock_;
  fsl::FDWaiter waiter_;
  zx::job job_;
  std::vector<std::unique_ptr<async::Wait>> process_waiters_;
};

int main(int argc, const char** argv) {
  // We need to close PA_DIRECTORY_REQUEST otherwise clients that expect us to
  // offer services won't know that we've started and are not going to offer
  // any services.
  //
  // TODO(abarth): Instead of closing this handle, we should offer some
  // introspection services for debugging.
  zx_handle_close(zx_take_startup_handle(PA_DIRECTORY_REQUEST));
  async::Loop loop(&kAsyncLoopConfigNoAttachToThread);
  async_set_default_dispatcher(loop.dispatcher());
  
  Service service(31337);
  loop.Run();
  async_set_default_dispatcher(nullptr);
  return 0;
}
