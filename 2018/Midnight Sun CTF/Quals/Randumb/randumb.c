#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/cred.h>
#include <linux/fcntl.h>
#include <linux/file.h>
#include <linux/fs.h>
#include <linux/random.h>
#include <linux/slab.h> 
#include <linux/syscalls.h>
#include <linux/version.h>
#include <asm/uaccess.h>

#include "randumb.h"

static dev_t Dev;
static struct cdev Cdev;
static struct class *Class;

static int is_open    = 0;
static int charset    = CHARSET_NONE;
static int debug      = DEBUG_NONE;
static int debug_time = DEBUG_NONE;
static int debug_uid  = DEBUG_NONE;

struct settings {
        int charset;
        int debug;
        int debug_time;
        int debug_uid;
};

static int debug_msg(char *msg, ...) {
        
        struct file *file = NULL;
        loff_t pos = 0;
        int nbytes;
        char line[256];

        unsigned long ts;
        int sec, hr, min, tmp;
        struct timeval tv;

#if LINUX_VERSION_CODE >= KERNEL_VERSION(3, 13, 0)
        unsigned int uid = current_uid().val;
#else
        unsigned int uid = current_uid();
#endif

        va_list vargs;
        mm_segment_t old_fs;

        if (debug <= DEBUG_NONE)
                return 0;

        old_fs = get_fs();
        set_fs(KERNEL_DS);

        file = filp_open(DEBUG_FILE, O_WRONLY|O_CREAT|O_APPEND, 0644);

        if (IS_ERR(file))
                return -EINVAL;

        if (debug_time > DEBUG_NONE) {
                pos = 0;
                memset(line, 0, sizeof line);

                do_gettimeofday(&tv);
                ts  = tv.tv_sec;
                tmp = ts / 60;
                sec = ts % 60;
                min = tmp % 60;
                hr  = ((tmp / 60) % 24);

                nbytes = snprintf(line, sizeof line,
                                  "\033[32;1m[ %02d:%02d:%02d ]\033[0m ",
                                  (int) abs(hr), min, sec);
                nbytes = vfs_write(file, line, nbytes, &pos);
        }

        if (debug_uid > DEBUG_NONE) {
                pos = 0;
                memset(line, 0, sizeof line);

                nbytes = snprintf(line, sizeof line,
                                  "\033[33;1muid(%u)\033[0m: ", uid);
                nbytes = vfs_write(file, line, nbytes, &pos);
        }

        pos = 0;
        memset(line, 0, sizeof line);

        va_start(vargs, msg);
        nbytes = vscnprintf(line, sizeof line, msg, vargs);
        nbytes = vfs_write(file, line, nbytes, &pos);

        filp_close(file, NULL);
        set_fs(old_fs);

        return nbytes;
}

static int device_open(struct inode *inode, struct file *file) {

        if (is_open)
                return -EBUSY;

        is_open++;
        if (debug & DEBUG_ALL)
                debug_msg("/dev/%s opened\n", DEVICE_NAME);

        return 0;
}

static int device_release(struct inode *inode, struct file *file) {

        if (is_open)
                is_open--;

        return 0;
}

static ssize_t device_read(struct file *file, char *buff, size_t len,
                           loff_t *off) {

        int i;
        int nbytes;
        char *data;

        if ((data = kzalloc(len, GFP_KERNEL)) == 0)
                return -ENOMEM;

        get_random_bytes(data, len);
        for (i = 0; i < len; i++) {
                switch (charset) {
                case CHARSET_UPPER:
                        (data)[i] = 0x41 + (data)[i] % 26;
                        break;
                case CHARSET_LOWER:
                        (data)[i] = 0x61 + (data)[i] % 26;
                        break;
                case CHARSET_NUM:
                        (data)[i] = 0x30 + (data)[i] % 9;
                        break;
                case CHARSET_NONE:
                default:
                        break;
                }
        }

        if ((nbytes = copy_to_user(buff, data, len)) != 0)
                len = len - nbytes;

        debug_msg("read %d bytes from /dev/%s\n", len, DEVICE_NAME);

        kfree(data);
        return len;
}

static ssize_t device_write(struct file *file, const char __user *buff,
                            size_t len, loff_t *off) {

        return -EPERM;
}

static long device_ioctl(struct file *file, unsigned int cmd,
                         unsigned long arg) {

        int nbytes;
        struct settings s;

        switch (cmd) {
        case IOCTL_GET_SETTINGS:

                s.charset = charset;
                s.debug   = debug;

                if (s.debug > DEBUG_NONE) {
                        s.debug_time = debug_time;
                        s.debug_uid  = debug_uid;
                }

                if ((nbytes = copy_to_user((void *) arg, (void *) &s, sizeof s)) != 0)
                        return -EFAULT;

                debug_msg("get_settings: %d bytes copied\n", sizeof s - nbytes);
                break;

        case IOCTL_SET_SETTINGS:

                if ((nbytes = copy_from_user(&s, (void *) arg, sizeof s)) != 0)
                        return -EFAULT;

                charset    = s.charset;
                debug      = s.debug;
                debug_time = s.debug_time & 1;
                debug_uid  = s.debug_uid & 1;

                debug_msg("set_settings: %d bytes copied\n", sizeof s - nbytes);
                break;

        default:
                break;
        }

        return 0;
}

static const struct file_operations fops = {
        .owner          = THIS_MODULE,
        .open           = device_open,
        .read           = device_read,
        .write          = device_write,
        .unlocked_ioctl = device_ioctl,
        .release        = device_release,
};

static int __init mod_init(void) {

        if (alloc_chrdev_region(&Dev, 0, 1, DEVICE_NAME) < 0)
                goto out;

        cdev_init(&Cdev, &fops);
        Cdev.owner = THIS_MODULE;
        Cdev.ops = &fops;

        if (cdev_add(&Cdev, Dev, 1) < 0)
                goto device;

        if ((Class = class_create(THIS_MODULE, DEVICE_NAME)) == NULL)
                goto region;

        if (device_create(Class, NULL, Dev, NULL, DEVICE_NAME) == NULL)
                goto class;

        printk(KERN_INFO "randumb: registered device: /dev/%s\n", DEVICE_NAME);
        return 0;

device:
        device_destroy(Class, Dev);

class:
        class_destroy(Class);

region:
        unregister_chrdev_region(Dev, 1);

out:
        printk(KERN_INFO "randumb: could not register device.\n");
        return -EPERM;
}

static void __exit mod_exit(void) {

        cdev_del(&Cdev);
        device_destroy(Class, Dev);
        class_destroy(Class);
        unregister_chrdev_region(Dev, 1);

        printk(KERN_INFO "randumb: unregistered device: /dev/%s\n", DEVICE_NAME);
}

module_init(mod_init);
module_exit(mod_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Midnight Sun CTF");
MODULE_DESCRIPTION("randumb: a dumb random character device");
