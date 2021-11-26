import abc

from jvmpy.classparser import constants
from jvmpy.classparser.access_flags import AccessFlags
from jvmpy.classparser.attribute import Attribute, ConstantValue
from jvmpy.classparser.constant import ConstantUtf8
from jvmpy.classparser.constant_pool import ConstantPool
from jvmpy.classparser.datastream import DataInputStream

from . import utils


class FieldOrMethod(AccessFlags, abc.ABC):
    name_index: int
    signature_index: int
    attributes: list[Attribute]
    attributes_count: int
    constant_pool: ConstantPool
    signature_attribute_string: str
    searched_for_signature_attribute: bool

    def __init__(self, access_flags: int, name_index: int, signature_index: int, attributes: list[Attribute], constant_pool: ConstantPool) -> None:
        super().__init__(access_flags)
        self.name_index = name_index
        self.signature_index = signature_index
        self.constant_pool = constant_pool
        self.set_attributes(attributes)
    
    @classmethod
    def from_data(cls, data: DataInputStream, constant_pool: ConstantPool):
        self = cls(data.read_unsigned_short(), data.read_unsigned_short(), data.read_unsigned_short(), None, constant_pool)
        attributes_count = data.read_unsigned_short()
        self.attributes = [None] * attributes_count
        for i in range(attributes_count):
            self.attributes[i] = Attribute.read_attribute(data, constant_pool)
        self.attributes_count = attributes_count
        return self
    
    def get_attributes(self) -> list[Attribute]:
        return self.attributes
    
    def set_attributes(self, attributes: list[Attribute]):
        self.attributes = attributes
        self.attributes_count = len(attributes) if attributes is not None else 0
    
    def get_signature(self) -> str:
        c: ConstantUtf8 = self.constant_pool.get_constant(self.signature_index, constants.CONSTANT_Utf8)
        return c.get_bytes()
    
    def get_name(self) -> str:
        c: ConstantUtf8 = self.constant_pool.get_constant(self.name_index, constants.CONSTANT_Utf8)
        return c.get_bytes()


class Field(FieldOrMethod):
    def get_constant_value(self) -> ConstantValue:
        for attribute in super().get_attributes():
            if attribute.get_tag() == constants.ATTR_CONSTANT_VALUE:
                return attribute
        return None

    def __repr__(self) -> str:
        access = utils.access_to_string(super().get_access_flags())
        access = '' if not access else (access + ' ')
        signature = utils.signature_to_string(self.get_signature())
        name = self.get_name()
        result = f'{access}{signature} {name}'
        cv = self.get_constant_value()
        if cv is not None:
            result += f' = {cv}'
        for attribute in super().get_attributes():
            if not isinstance(attribute, ConstantValue):
                result += f' [{attribute}]'
        return result
