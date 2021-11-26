import abc
import copy

from jvmpy.classparser import constants, utils
from jvmpy.classparser.constant import ConstantString, ConstantUtf8
from jvmpy.classparser.constant_pool import ConstantPool
from jvmpy.classparser.datastream import DataInputStream


class Attribute(abc.ABC):
    name_index: int
    length: int
    tag: int
    constant_pool: ConstantPool

    def __init__(self, tag: int, name_index: int, length: int, constant_pool: ConstantPool) -> None:
        self.tag = tag
        self.name_index = name_index
        self.length = length
        self.constant_pool = constant_pool

    @staticmethod
    def read_attribute(data: DataInputStream, constant_pool: ConstantPool) -> 'Attribute':
        tag = constants.ATTR_UNKNOWN
        name_index = data.read_unsigned_short()
        c: ConstantUtf8 = constant_pool.get_constant(name_index, constants.CONSTANT_Utf8)
        name = c.get_bytes()
        length = data.read_int()
        for i in range(constants.KNOWN_ATTRIBUTES):
            if name == constants.get_attribute_name(i):
                tag = i
                break
        if tag == constants.ATTR_UNKNOWN:
            pass # Do later if necessary
        elif tag == constants.ATTR_CONSTANT_VALUE:
            return ConstantValue.from_data(name_index, length, data, constant_pool)
        raise ValueError(f'Unrecognized attribute type tag parsed: {tag}')

    @abc.abstractmethod
    def copy(self, constant_pool: ConstantPool) -> 'Attribute':
        return NotImplemented

    def get_constant_pool(self) -> ConstantPool:
        return self.constant_pool
    
    def get_tag(self) -> int:
        return self.tag
    
    def set_constant_pool(self, constant_pool: ConstantPool):
        self.constant_pool = constant_pool
    
    def __repr__(self) -> str:
        return constants.get_attribute_name(self.tag)


class ConstantValue(Attribute):
    constant_value_index: int
    
    def __init__(self, name_index: int, length: int, constant_value_index: int, constant_pool: ConstantPool) -> None:
        super().__init__(constants.ATTR_CONSTANT_VALUE, name_index, length, constant_pool)
        self.constant_value_index = constant_value_index

    @classmethod
    def from_data(cls, name_index: int, length: int, data: DataInputStream, constant_pool: ConstantPool):
        return cls(name_index, length, data.read_unsigned_short(), constant_pool)
    
    def copy(self, constant_pool: ConstantPool) -> 'Attribute':
        c = copy.copy(self)
        c.set_constant_pool(constant_pool)
        return c
    
    def __repr__(self) -> str:
        c = super().get_constant_pool().get_constant(self.constant_value_index)
        t = c.get_tag()
        if t == constants.CONSTANT_Long:
            c2: ConstantLong = c
            result = c2.get_bytes()
        elif t == constants.CONSTANT_Float:
            c2: ConstantFloat = c
            result = c2.get_bytes()
        elif t == constants.CONSTANT_Double:
            c2: ConstantDouble = c
            result = c2.get_bytes()
        elif t == constants.CONSTANT_Integer:
            c2: ConstantInteger = c
            result = c2.get_bytes()
        elif t == constants.CONSTANT_String:
            c2: ConstantString = c
            i = c.get_string_index()
            c = super().get_constant_pool().get_constant(i, constants.CONSTANT_Utf8)
            c2: ConstantUtf8 = c
            result = f'"{utils.convert_string(c2.get_bytes())}"'
        else:
            raise ValueError(f'Type of ConstValue invalid: {c}')
        return result
