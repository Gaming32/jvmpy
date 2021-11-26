from jvmpy.classparser.exceptions import ClassFormatException
from jvmpy.classparser import constants
from jvmpy.classparser.constant import Constant

from .datastream import DataInputStream


class ConstantPool:
    pool: list[Constant]

    @classmethod
    def from_data(cls, data: DataInputStream) -> 'ConstantPool':
        self = cls.__new__(cls)
        count = data.read_unsigned_short()
        self.pool = [None] * count
        i = 1
        while i < count:
            self.pool[i] = Constant.read_constant(data)
            tag = self.pool[i].get_tag()
            if tag in (constants.CONSTANT_Double, constants.CONSTANT_Long):
                i += 2
            else:
                i += 1
        return self

    def get_constant(self, index: int, tag: int = None) -> Constant:
        if index >= len(self.pool) or index < 0:
            raise ClassFormatException(f'Invalid constant pool reference: {index}. Constant pool size is: {len(self.pool)}')
        c = self.pool[index]
        if tag is None:
            return c
        if c is None:
            raise ClassFormatException(f'Constant pool at index {index} is None')
        if c.get_tag() != tag:
            raise ClassFormatException(f'Expected class `{constants.get_constant_name(tag)}` at index {index} and got {c}')
        return c

    def __repr__(self) -> str:
        result = ''
        for i in range(1, len(self.pool)):
            result += f'{i}) {self.pool[i]}\n'
        return result
