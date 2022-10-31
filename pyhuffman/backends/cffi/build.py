import glob
import sys

from cffi import FFI

ffibuilder = FFI()
ffibuilder.cdef(
    """
int huffman_encode_file(FILE* in, FILE* out);

int huffman_decode_file(FILE* in, FILE* out);

int huffman_encode_memory(const unsigned char* bufin,
			  uint32_t bufinlen,
			  unsigned char** pbufout,
			  uint32_t* pbufoutlen);

int huffman_decode_memory(const unsigned char* bufin,
			  uint32_t bufinlen,
			  unsigned char** bufout,
			  uint32_t* pbufoutlen);

FILE *fopen(const char *filename, const char  *opentype);
FILE *fdopen(int fdescriptor, const char *opentype);
int  fclose(FILE *stream);
void* PyMem_Malloc(size_t n);
void PyMem_Free(void *p);
    """
)

source = """
#include <stdint.h>
#include <stdio.h>
#include "huffman.h"
"""

ffibuilder.set_source(
    "pyhuffman.backends.cffi._hfm",
    source,
    sources=[f"./huffman/huffman.c"],
    include_dirs=["./huffman"],
    define_macros=[("PYTHON", None)],
)

if __name__ == "__main__":
    ffibuilder.compile()
