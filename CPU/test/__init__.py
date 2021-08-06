from ctypes import cdll
from os import path

path.join(path.abspath(__file__))

print(__file__)
testlib = cdll.LoadLibrary("bin/test.so")
