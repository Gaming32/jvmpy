JVM_CLASSFILE_MAGIC = 0xCAFEBABE

CONSTANT_Utf8 = 1
CONSTANT_Integer = 3
CONSTANT_Float = 4
CONSTANT_Long = 5
CONSTANT_Double = 6
CONSTANT_Class = 7
CONSTANT_Fieldref = 9
CONSTANT_String = 8
CONSTANT_Methodref = 10
CONSTANT_InterfaceMethodref = 11
CONSTANT_NameAndType = 12
CONSTANT_MethodHandle = 15
CONSTANT_MethodType = 16
CONSTANT_Dynamic = 17
CONSTANT_InvokeDynamic = 18
CONSTANT_Module = 19
CONSTANT_Package = 20

CONSTANT_NAMES = [
    '', 'CONSTANT_Utf8', '', 'CONSTANT_Integer',
    'CONSTANT_Float', 'CONSTANT_Long', 'CONSTANT_Double',
    'CONSTANT_Class', 'CONSTANT_String', 'CONSTANT_Fieldref',
    'CONSTANT_Methodref', 'CONSTANT_InterfaceMethodref',
    'CONSTANT_NameAndType', '', '', 'CONSTANT_MethodHandle',
    'CONSTANT_MethodType', 'CONSTANT_Dynamic', 'CONSTANT_InvokeDynamic',
    'CONSTANT_Module', 'CONSTANT_Package']

ACC_PUBLIC = 0x0001
ACC_PRIVATE = 0x0002
ACC_PROTECTED = 0x0004
ACC_STATIC = 0x0008
ACC_FINAL = 0x0010
ACC_OPEN = 0x0020
ACC_SUPER = 0x0020
ACC_SYNCHRONIZED = 0x0020
ACC_TRANSITIVE = 0x0020
ACC_BRIDGE = 0x0040
ACC_STATIC_PHASE = 0x0040
ACC_VOLATILE = 0x0040
ACC_TRANSIENT = 0x0080
ACC_VARARGS = 0x0080
ACC_NATIVE = 0x0100
ACC_INTERFACE = 0x0200
ACC_ABSTRACT = 0x0400
ACC_STRICT = 0x0800
ACC_SYNTHETIC = 0x1000
ACC_ANNOTATION = 0x2000
ACC_ENUM = 0x4000
ACC_MANDATED = -0x8000
ACC_MODULE = -0x8000
MAX_ACC_FLAG_I = 0x8000

ACCESS_NAMES = [
    "public", "private", "protected", "static", "final", "synchronized",
    "volatile", "transient", "native", "interface", "abstract", "strictfp",
    "synthetic", "annotation", "enum", "module"
]

ATTR_UNKNOWN = -1
ATTR_SOURCE_FILE = 0
ATTR_CONSTANT_VALUE = 1
ATTR_CODE = 2
ATTR_EXCEPTIONS = 3
ATTR_LINE_NUMBER_TABLE = 4
ATTR_LOCAL_VARIABLE_TABLE = 5
ATTR_INNER_CLASSES = 6
ATTR_SYNTHETIC = 7
ATTR_DEPRECATED = 8
ATTR_PMG = 9
ATTR_SIGNATURE = 10
ATTR_STACK_MAP = 11
ATTR_RUNTIME_VISIBLE_ANNOTATIONS = 12
ATTR_RUNTIME_INVISIBLE_ANNOTATIONS = 13
ATTR_RUNTIME_VISIBLE_PARAMETER_ANNOTATIONS = 14
ATTR_RUNTIME_INVISIBLE_PARAMETER_ANNOTATIONS = 15
ATTR_ANNOTATION_DEFAULT = 16
ATTR_LOCAL_VARIABLE_TYPE_TABLE = 17
ATTR_ENCLOSING_METHOD = 18
ATTR_STACK_MAP_TABLE = 19
ATTR_BOOTSTRAP_METHODS = 20
ATTR_METHOD_PARAMETERS = 21
ATTR_MODULE = 22
ATTR_MODULE_PACKAGES = 23
ATTR_MODULE_MAIN_CLASS = 24
ATTR_NEST_HOST = 25
ATTR_NEST_MEMBERS = 26
KNOWN_ATTRIBUTES = 27

ATTRIBUTE_NAMES = [
    "SourceFile", "ConstantValue", "Code", "Exceptions",
    "LineNumberTable", "LocalVariableTable",
    "InnerClasses", "Synthetic", "Deprecated",
    "PMGClass", "Signature", "StackMap",
    "RuntimeVisibleAnnotations", "RuntimeInvisibleAnnotations",
    "RuntimeVisibleParameterAnnotations", "RuntimeInvisibleParameterAnnotations",
    "AnnotationDefault", "LocalVariableTypeTable", "EnclosingMethod", "StackMapTable",
    "BootstrapMethods", "MethodParameters", "Module", "ModulePackages",
    "ModuleMainClass", "NestHost", "NestMembers"
]


def get_constant_name(index: int) -> str:
    return CONSTANT_NAMES[index]


def get_access_name(index: int) -> str:
    return ACCESS_NAMES[index]


def get_attribute_name(index: int) -> str:
    return ATTRIBUTE_NAMES[index]
