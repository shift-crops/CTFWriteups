#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define TYPE_REAL    0xdeadbeefcafebabeUL
#define TYPE_STRING  0xc0b3beeffee1deadUL

typedef struct {
  union {
    double real;
    char *string;
  };
  size_t type;
} item_t;

typedef struct {
  size_t size;
  item_t *items;
} storage_t;

/* Print string to stdout */
void print(const char *s) {
  if (write(STDOUT_FILENO, s, strlen(s)) != strlen(s)) exit(1);
}

/* Read string from stdin */
char* reads(const char *s) {
  char *p = NULL;
  size_t n = 0;
  print(s);
  if (getline(&p, &n, stdin) == -1) exit(1);
  p[strcspn(p, "\n")] = '\0';
  return p;
}

/* Read integer from stdin */
size_t readi(const char *s) {
  char *e, *p = reads(s);
  size_t i = strtoll(p, &e, 10);
  if (!*p || *e) exit(1);
  free(p);
  return i;
}

/* Read float from stdin*/
double readf(const char *s) {
  char *e, *p = reads(s);
  double f = strtold(p, &e);
  if (!*p || *e) exit(1);
  free(p);
  return f;
}

/**
 * Create a new storage
 */
void create_storage(storage_t *storage) {
  size_t size = readi("size: ");
  if (size >= 100) {
    print("size too big\n");
    return;
  }

  if (storage->items) free(storage->items);
  storage->items = (item_t*)malloc(size * sizeof(item_t));

  if (storage->items) {
    storage->size = size;
    print("success\n");
  } else {
    storage->size = 0;
    print("fail\n");
  }
}

/**
 * Set the value of an item in a storage
 */
void set_item(storage_t *storage) {
  if (!storage->items) {
    print("uninitialized\n");
    return;
  }

  size_t idx  = readi("index: ");
  size_t type = readi("type [0=str / x=real]: ");
  if (type == 0) {
    storage->items[idx].type = TYPE_STRING;
  } else {
    storage->items[idx].type = TYPE_REAL;
  }

  if (idx >= storage->size) {
    print("insufficient storage size\n");
    return;
  }

  if (storage->items[idx].type == TYPE_STRING) {
    storage->items[idx].string = reads("value: ");
  } else {
    storage->items[idx].real = readf("value: ");
  }
}

/**
 * Get the value of an item in a storage
 */
void get_item(storage_t *storage) {
  if (!storage->items) {
    print("uninitialized\n");
    return;
  }

  size_t idx = readi("index: ");
  if (idx >= storage->size) {
    print("out-of-bounds\n");
    return;
  }

  if (storage->items[idx].type == TYPE_STRING) {
    print(storage->items[idx].string);
    print("\n");
  } else {
    printf("%.99g\n", storage->items[idx].real);
  }
}

/**
 * Entry point
 */
int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  storage_t storage = { .size = 0, .items = NULL };

  print("1. new\n2. set\n3. get\n");
  while (1) {
    switch (readi("> ")) {
      case 1: create_storage(&storage); break;
      case 2: set_item(&storage); break;
      case 3: get_item(&storage); break;
      default: print("bye!\n"); exit(0);
    }
  }
}
