import os
from typing import BinaryIO, Union

from jvmpy.classparser.constant_pool import ConstantPool
from jvmpy.classparser.datastream import DataInputStream
from jvmpy.classparser.exceptions import ClassFormatException
from jvmpy.classparser.field_or_method import Field
from jvmpy.classparser.javaclass import JavaClass

from . import constants


class ClassParser:
    is_owned: bool
    file: Union[os.PathLike, BinaryIO]
    data: DataInputStream

    minor: int
    major: int
    constant_pool: ConstantPool
    access_flags: int
    class_name_index: int
    superclass_name_index: int
    interfaces: list[int]
    fields: list[Field]

    def __init__(self, filename_or_file: Union[os.PathLike, BinaryIO]) -> None:
        self.is_owned = isinstance(filename_or_file, (os.PathLike, str, bytes))
        self.file = filename_or_file

    def parse(self) -> JavaClass:
        try:
            if self.is_owned:
                file = open(self.file, 'rb')
            else:
                file = self.file
            self.data = DataInputStream(file)
            #### Read headers ####
            # Check magic tag of class file
            self.read_id()
            # Get compiler version
            self.read_version()
            #### Read constant pool and related ####
            # Read constant pool entries
            self.read_constant_pool()
            # Get class information
            self.read_class_info()
            # Get interface information, i.e., implemented interfaces
            self.read_interfaces()
            #### Read class fields and methods ####
            # Read class fields, i.e., the variables of the class
            self.read_fields()
        finally:
            if self.is_owned:
                file.close()
        return self
    
    def read_id(self):
        if self.data.read_unsigned_int() != constants.JVM_CLASSFILE_MAGIC:
            raise ClassFormatException(f'{self.data.file.name} is not a Java .class file')
    
    def read_version(self):
        self.minor = self.data.read_unsigned_short()
        self.major = self.data.read_unsigned_short()
    
    def read_constant_pool(self):
        self.constant_pool = ConstantPool.from_data(self.data)
    
    def read_class_info(self):
        self.access_flags = self.data.read_unsigned_short()
        if self.access_flags & constants.ACC_INTERFACE:
            self.access_flags |= constants.ACC_ABSTRACT
        if (self.access_flags & constants.ACC_ABSTRACT) and (self.access_flags & constants.ACC_FINAL):
            raise ClassFormatException(f"Class {self.data.file.name} can't be both final and abstract")
        self.class_name_index = self.data.read_unsigned_short()
        self.superclass_name_index = self.data.read_unsigned_short()
    
    def read_interfaces(self):
        interfaces_count = self.data.read_unsigned_short()
        self.interfaces = [0] * interfaces_count
        for i in range(interfaces_count):
            self.interfaces[i] = self.data.read_unsigned_short()
    
    def read_fields(self):
        fields_count = self.data.read_unsigned_short()
        self.fields = [None] * fields_count
        for i in range(fields_count):
            self.fields[i] = Field.from_data(self.data, self.constant_pool)
