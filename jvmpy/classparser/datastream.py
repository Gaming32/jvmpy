import struct
from typing import BinaryIO


class DataInputStream:
    file: BinaryIO

    def __init__(self, file: BinaryIO) -> None:
        self.file = file

    def read_unsigned_byte(self) -> int:
        return _UBYTE.unpack(self.file.read(1))[0]

    def read_unsigned_short(self) -> int:
        return _USHORT.unpack(self.file.read(2))[0]

    def read_int(self) -> int:
        return _INT.unpack(self.file.read(4))[0]

    def read_unsigned_int(self) -> int:
        return _UINT.unpack(self.file.read(4))[0]

    def read_utf(self) -> str:
        length = self.read_unsigned_short()
        data = self.file.read(length)
        return data.decode('utf-8')


_UBYTE = struct.Struct('>B')
_USHORT = struct.Struct('>H')
_INT = struct.Struct('>i')
_UINT = struct.Struct('>I')
