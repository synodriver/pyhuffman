# cython: language_level=3
# cython: cdivision=True
# distutils: language=c++
from libc.stdint cimport uint32_t
from libc.stdio cimport FILE


cdef extern from "huffman.h" nogil:
    int huffman_encode_file(FILE* in_, FILE* out)

    int huffman_decode_file(FILE* in_, FILE* out)

    int huffman_encode_memory(const unsigned char* bufin,
                  uint32_t bufinlen,
                  unsigned char** pbufout,
                  uint32_t* pbufoutlen)

    int huffman_decode_memory(const unsigned char* bufin,
                  uint32_t bufinlen,
                  unsigned char** bufout,
                  uint32_t* pbufoutlen)