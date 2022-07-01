"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
import os
from pathlib import Path
from typing import IO, Union

from pyhuffman.backends.cffi._hfm_cffi import ffi, lib

InputType = Union[str, bytes, Path, IO]


def ensure_bytes(file) -> bytes:
    if isinstance(file, Path):
        return str(file).encode()
    elif isinstance(file, str):
        return file.encode()
    else:
        return bytes(file)


def encode_file(in_: InputType, out_: InputType) -> int:
    use_fopen = 0
    if hasattr(in_, "fileno") and hasattr(out_, "fileno"):
        in_file = lib.fdopen(os.dup(in_.fileno()), "rb")
        out_file = lib.fdopen(os.dup(out_.fileno()), "wb")
    else:
        use_fopen = 1
        in_name_bytes = ensure_bytes(in_)
        out_name_bytes = ensure_bytes(out_)
        in_file = lib.fopen(ffi.from_buffer(in_name_bytes), "rb")
        if in_file == ffi.NULL:
            raise FileNotFoundError

        out_file = lib.fopen(ffi.from_buffer(out_name_bytes), "wb")
        if out_file == ffi.NULL:
            raise FileNotFoundError

    ret: int = lib.huffman_encode_file(in_file, out_file)

    if use_fopen:
        lib.fclose(in_file)
        lib.fclose(out_file)
    if ret > 0:
        raise ValueError
    return ret


def decode_file(in_: InputType, out_: InputType) -> int:
    use_fopen = 0
    if hasattr(in_, "fileno") and hasattr(out_, "fileno"):
        in_file = lib.fdopen(os.dup(in_.fileno()), "rb")
        out_file = lib.fdopen(os.dup(out_.fileno()), "wb")
    else:
        use_fopen = 1
        in_name_bytes = ensure_bytes(in_)
        out_name_bytes = ensure_bytes(out_)
        in_file = lib.fopen(ffi.from_buffer(in_name_bytes), "rb")
        if in_file == ffi.NULL:
            raise FileNotFoundError

        out_file = lib.fopen(ffi.from_buffer(out_name_bytes), "wb")
        if out_file == ffi.NULL:
            raise FileNotFoundError

    ret: int = lib.huffman_decode_file(in_file, out_file)

    if use_fopen:
        lib.fclose(in_file)
        lib.fclose(out_file)
    if ret > 0:
        raise ValueError
    return ret


def encode(data: bytes) -> bytes:
    input_size = len(data)
    out_buf = ffi.new("unsigned char **")
    out_len = ffi.new("uint32_t*")

    ret: int = lib.huffman_encode_memory(
        ffi.cast("const unsigned char*", ffi.from_buffer(data)),
        input_size,
        out_buf,
        out_len,
    )
    assert out_buf[0] != ffi.NULL
    out: bytes = ffi.unpack(ffi.cast("char*", out_buf[0]), out_len[0])
    lib.PyMem_Free(out_buf[0])
    if ret > 0:
        raise ValueError
    return out


def decode(data: bytes) -> bytes:
    input_size = len(data)
    out_buf = ffi.new("unsigned char **")
    out_len = ffi.new("uint32_t*")

    ret: int = lib.huffman_decode_memory(
        ffi.cast("const unsigned char*", ffi.from_buffer(data)),
        input_size,
        out_buf,
        out_len,
    )
    assert out_buf[0] != ffi.NULL
    out: bytes = ffi.unpack(ffi.cast("char*", out_buf[0]), out_len[0])
    lib.PyMem_Free(out_buf[0])
    if ret > 0:
        raise ValueError
    return out
