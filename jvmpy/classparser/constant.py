import abc
from types import SimpleNamespace

from jvmpy.classparser import constants
from jvmpy.classparser.datastream import DataInputStream
from jvmpy.classparser.exceptions import ClassFormatException


class Constant(abc.ABC):
    tag: int

    def __init__(self, tag: int) -> None:
        self.tag = tag

    def get_tag(self) -> int:
        return self.tag

    def __repr__(self) -> str:
        return f'{constants.get_constant_name(self.tag)}[{self.tag}]'

    @staticmethod
    def read_constant(data: DataInputStream) -> 'Constant':
        _constant_utf8 = SimpleNamespace(from_data=(lambda d: ConstantUtf8.get_instance_from_data(d)))
        b = data.read_unsigned_byte()
        constant_class = {
            constants.CONSTANT_Class: ConstantClass,
            constants.CONSTANT_Fieldref: ConstantFieldref,
            constants.CONSTANT_Methodref: ConstantMethodref,
            # constants.CONSTANT_InterfaceMethodref: ConstantInterfaceMethodref,
            constants.CONSTANT_String: ConstantString,
            # constants.CONSTANT_Integer: ConstantInteger,
            # constants.CONSTANT_Float: ConstantFloat,
            # constants.CONSTANT_Long: ConstantLong,
            # constants.CONSTANT_Double: ConstantDouble,
            constants.CONSTANT_NameAndType: ConstantNameAndType,
            constants.CONSTANT_Utf8: _constant_utf8,
            # constants.CONSTANT_MethodHandle: ConstantMethodHandle,
            # constants.CONSTANT_MethodType: ConstantMethodType,
            # constants.CONSTANT_Dynamic: ConstantDynamic,
            # constants.CONSTANT_InvokeDynamic: ConstantInvokeDynamic,
            # constants.CONSTANT_Module: ConstantModule,
            # constants.CONSTANT_Package: ConstantPackage,
        }.get(b)
        if constant_class is None:
            raise ClassFormatException(f'Invalid byte tag in constant pool: {b}')
        return constant_class.from_data(data)


class ConstantCP(Constant):
    class_index: int
    name_and_type_index: int

    def __init__(self, tag: int, class_index: int, name_and_type_index: int) -> None:
        super().__init__(tag)
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    @classmethod
    def from_data(cls, tag: int, data: DataInputStream):
        return cls(tag, data.read_unsigned_short(), data.read_unsigned_short())

    def __repr__(self) -> str:
        return f'{super().__repr__()}(class_index = {self.class_index}, name_and_type_index = {self.name_and_type_index})'


class ConstantClass(Constant):
    name_index: int

    def __init__(self, name_index: int) -> None:
        super().__init__(constants.CONSTANT_Class)
        self.name_index = name_index

    @classmethod
    def from_data(cls, data: DataInputStream):
        return cls(data.read_unsigned_short())

    def __repr__(self) -> str:
        return f'{super().__repr__()}(name_index = {self.name_index})'


class ConstantFieldref(ConstantCP):
    def __init__(self, class_index: int, name_and_type_index: int) -> None:
        super().__init__(constants.CONSTANT_Fieldref, class_index, name_and_type_index)

    @classmethod
    def from_data(cls, data: DataInputStream):
        return ConstantCP.from_data(constants.CONSTANT_Fieldref, data)


class ConstantMethodref(ConstantCP):
    def __init__(self, class_index: int, name_and_type_index: int) -> None:
        super().__init__(constants.CONSTANT_Methodref, class_index, name_and_type_index)

    @classmethod
    def from_data(cls, data: DataInputStream):
        return ConstantCP.from_data(constants.CONSTANT_Methodref, data)


class ConstantString(Constant):
    string_index: int

    def __init__(self, name_index: int) -> None:
        super().__init__(constants.CONSTANT_Class)
        self.string_index = name_index

    @classmethod
    def from_data(cls, data: DataInputStream):
        return cls(data.read_unsigned_short())

    def __repr__(self) -> str:
        return f'{super().__repr__()}(name_index = {self.string_index})'


class ConstantNameAndType(Constant):
    name_index: int
    signature_index: int

    def __init__(self, name_index: int, signature_index: int) -> None:
        super().__init__(constants.CONSTANT_NameAndType)
        self.name_index = name_index
        self.signature_index = signature_index

    @classmethod
    def from_data(cls, data: DataInputStream):
        return cls(data.read_unsigned_short(), data.read_unsigned_short())

    def __repr__(self) -> str:
        return f'{super().__repr__()}(name_index = {self.name_index}, signature_index = {self.signature_index})'


class ConstantUtf8(Constant):
    value: str

    def __init__(self, value: str) -> None:
        super().__init__(constants.CONSTANT_Utf8)
        self.value = value

    @classmethod
    def from_data(cls, data: DataInputStream):
        return cls(data.read_utf())

    @classmethod
    def get_instance(cls, value: str):
        return cls(value)

    @classmethod
    def get_instance_from_data(cls, data: DataInputStream):
        return cls.get_instance(data.read_utf())
    
    def get_bytes(self) -> str:
        return self.value

    def __repr__(self) -> str:
        value = self.value.replace('\n', '\\n')
        return f'{super().__repr__()}("{value}")'
