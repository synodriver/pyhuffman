"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from random import randint
from unittest import TestCase

from pyhuffman import decode, encode


class Testall(TestCase):
    def test_encode(self):
        for i in range(1000):
            data = bytes([randint(0, 255) for _ in range(randint(100, 1000))])
            self.assertEqual(decode(encode(data)), data)


if __name__ == "__main__":
    import unittest

    unittest.maiN()
