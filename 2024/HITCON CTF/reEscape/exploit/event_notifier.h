#ifndef _EVENT_NOTIFIER_H
#define _EVENT_NOTIFIER_H

#include <stdbool.h>

typedef struct EventNotifier {
    int rfd;
    int wfd;
    bool initialized;
} EventNotifier;

#endif
