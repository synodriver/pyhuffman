# cython: language_level=3
# cython: cdivision=True
# distutils: language=c++
from cpython.bytes cimport PyBytes_FromStringAndSize
from cpython.mem cimport PyMem_Free
from cpython.object cimport PyObject_HasAttrString
from libc.stdint cimport uint8_t, uint32_t
from libc.stdio cimport FILE, fclose, fdopen, fopen

from pyhuffman.backends.cython.huffman cimport (huffman_decode_file,
                                                huffman_decode_memory,
                                                huffman_encode_file,
                                                huffman_encode_memory)

import os
from pathlib import Path


cdef bytes ensure_bytes(object file):
    if isinstance(file, Path):
        return str(file).encode()
    elif isinstance(file, str):
        return file.encode()
    else:
        return bytes(file)

cpdef inline int encode_file(object in_, object out_) except +:
    cdef:
        int use_fopen = 0
        FILE * in_file
        FILE * out_file
    if PyObject_HasAttrString(in_, "fileno") and PyObject_HasAttrString(out_, "fileno"):
        in_file = fdopen(os.dup(in_.fileno()), "rb")
        out_file = fdopen(os.dup(out_.fileno()), "wb")
    else:
        use_fopen = 1
        in_name_bytes = ensure_bytes(in_)
        out_name_bytes = ensure_bytes(out_)
        in_file = fopen(<char*>in_name_bytes, "rb")
        if in_file == NULL:
            raise FileNotFoundError

        out_file = fopen(<char *> out_name_bytes, "wb")
        if out_file == NULL:
            raise FileNotFoundError

    cdef int ret = huffman_encode_file(in_file, out_file)

    if use_fopen:
        fclose(in_file)
        fclose(out_file)
    if ret > 0:
        raise ValueError
    return ret

cpdef inline int decode_file(object in_, object out_) except +:
    cdef:
        int use_fopen = 0
        FILE * in_file
        FILE * out_file
    if PyObject_HasAttrString(in_, "fileno") and PyObject_HasAttrString(out_, "fileno"):
        in_file = fdopen(os.dup(in_.fileno()), "rb")
        out_file = fdopen(os.dup(out_.fileno()), "wb")
    else:
        use_fopen = 1
        in_name_bytes = ensure_bytes(in_)
        out_name_bytes = ensure_bytes(out_)
        in_file = fopen(<char*>in_name_bytes, "rb")
        if in_file == NULL:
            raise FileNotFoundError

        out_file = fopen(<char *> out_name_bytes, "wb")
        if out_file == NULL:
            raise FileNotFoundError

    cdef int ret = huffman_decode_file(in_file, out_file)

    if use_fopen:
        fclose(in_file)
        fclose(out_file)
    if ret > 0:
        raise ValueError
    return ret

cpdef inline bytes encode(const uint8_t[::1] data):
    cdef:
        Py_ssize_t input_size = data.shape[0]
        unsigned char * out_buf = NULL
        uint32_t out_len
    cdef int ret = huffman_encode_memory(<const unsigned char*>&data[0], <uint32_t>input_size,&out_buf, &out_len )
    assert out_buf != NULL
    cdef bytes out = PyBytes_FromStringAndSize(<char *>out_buf, <Py_ssize_t>out_len)
    PyMem_Free(out_buf)
    if ret > 0:
        raise ValueError
    return out

cpdef inline bytes decode(const uint8_t[::1] data):
    cdef:
        Py_ssize_t input_size = data.shape[0]
        unsigned char * out_buf = NULL
        uint32_t out_len
    cdef int ret = huffman_decode_memory(<const unsigned char*>&data[0], <uint32_t>input_size,&out_buf, &out_len )
    assert out_buf != NULL
    cdef bytes out = PyBytes_FromStringAndSize(<char *>out_buf, <Py_ssize_t>out_len)
    PyMem_Free(out_buf)
    if ret > 0:
        raise ValueError
    return out
