<h1 align="center"><i>✨ pyhuffman ✨ </i></h1>

<h3 align="center">The python binding for <a href="https://github.com/synodriver/huffman">huffman</a> </h3>



[![pypi](https://img.shields.io/pypi/v/python-huffman.svg)](https://pypi.org/project/python-huffman/)
![python](https://img.shields.io/pypi/pyversions/python-huffman)
![implementation](https://img.shields.io/pypi/implementation/python-huffman)
![wheel](https://img.shields.io/pypi/wheel/python-huffman)
![license](https://img.shields.io/github/license/synodriver/pyhuffman.svg)
![action](https://img.shields.io/github/workflow/status/synodriver/pyhuffman/build%20wheel)

### 公开函数
```python
from typing import IO, Union
from pathlib import Path

InputType = Union[str, bytes, Path, IO]

def encode_file(in_: InputType, out_: InputType) -> int: ...
def decode_file(in_: InputType, out_: InputType) -> int: ...
def encode(data: bytes) -> bytes: ...
def decode(data: bytes) -> bytes: ...
```

### 环境变量
```HFM_USE_CFFI```强制使用cffi后端