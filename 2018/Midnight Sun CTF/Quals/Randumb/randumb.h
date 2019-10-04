#ifndef RANDUMB_H
#define RANDUMB_H

#define DEVICE_NAME        "randumb"
#define DEBUG_FILE         "/tmp/randumb.log"

#define IOCTL_GET_SETTINGS -0xff
#define IOCTL_SET_SETTINGS -0x100

#define CHARSET_NONE       0
#define CHARSET_NUM        1
#define CHARSET_UPPER      2
#define CHARSET_LOWER      4

#define DEBUG_NONE         0
#define DEBUG_INFO         1
#define DEBUG_ALL          2

#endif