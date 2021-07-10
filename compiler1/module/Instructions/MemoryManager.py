from typing import Set
from .Types import Address


#ToDo: test
class MemoryManager:
    mmap: Set[Address] = set()
    _start = 0x0100
    _end = 0x08FF

    @staticmethod
    def getMemory() -> Address:
        for addr in range(MemoryManager._start, MemoryManager._end):
            if not addr in MemoryManager.mmap:
                MemoryManager.mmap.add(addr)
                return addr

    @staticmethod
    def freeMemory(addr) -> None:
        MemoryManager.mmap.remove(addr)

    def checkAddress(addr: Address) -> bool:
        return addr in MemoryManager.mmap
