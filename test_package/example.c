#include <stdio.h>
#include <zlib.h>

int
main(
  int argc,
  char *argv[])
{
  /* more exciting tests can be implemented, for now just print the version */
  printf("zlib version %s\n", ZLIB_VERSION);
  return 0;
}

