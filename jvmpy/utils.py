import os
from pathlib import Path
from typing import Any, Optional, cast

from javatools import (CONST_Class, CONST_Double, CONST_Float, CONST_Integer,
                       CONST_Long, CONST_String, CONST_Utf8, JavaClassInfo,
                       JavaConstantPool, JavaMemberInfo, unpack_classfile)
from javatools.jarinfo import JarInfo

from jvmpy.rt_jar import find_rt_jar

# CLASSPATH = [Path(d) for d in os.get_exec_path()]
CLASSPATH: list[Path] = []
CLASSPATH.append(Path(os.getcwd()))
RT_JAR = find_rt_jar()
if RT_JAR is not None:
    CLASSPATH.append(RT_JAR)


_loaded_jars: dict[Path, JarInfo] = {}
_loaded_class_data: dict[str, JavaClassInfo] = {}

def load_class_data(class_name: str) -> Optional[JavaClassInfo]:
    if class_name in _loaded_class_data:
        return _loaded_class_data[class_name]
    class_file_name = class_name.replace('.', '/') + '.class'
    for path in CLASSPATH:
        if os.path.splitext(path)[1] == '.jar':
            if path in _loaded_jars:
                jar = _loaded_jars[path]
            else:
                jar = JarInfo(path)
                _loaded_jars[path] = jar
            try:
                class_ = jar.get_classinfo(class_file_name)
            except KeyError:
                continue
            else:
                _loaded_class_data[class_name] = class_
                return class_
        full_path = path.joinpath(class_file_name)
        if full_path.is_file():
            class_ = unpack_classfile(full_path)
            _loaded_class_data[class_name] = class_
            return class_
    return None


def repr_const(cpool: JavaConstantPool, index: int) -> str:
    type, value = cast(tuple[int, Any], cpool.consts[index])
    if type in (CONST_Utf8, CONST_Integer, CONST_Double):
        return str(value)
    elif type == CONST_Float:
        return f'{value}F'
    elif type == CONST_Long:
        return f'{value}L'
    elif type == CONST_Class:
        return f'{repr_const(cpool, value)}.class'
    elif type == CONST_String:
        return f'"{repr_const(cpool, value)}"'
    return repr(value)


def prettify_member(member: JavaMemberInfo) -> str:
    if member.is_method:
        return prettify_method(member)
    return prettify_field(member)


def prettify_field(field: JavaMemberInfo) -> str:
    access_flags = ''.join(x + ' ' for x in field.pretty_access_flags())
    signature = field.pretty_signature()
    if signature is None:
        signature = field.pretty_type()
    const = field.get_constantvalue()
    if const is None:
        const = ''
    else:
        const = ' = ' + repr_const(field.cpool, const)
    return f'{access_flags}{signature} {field.get_name()}{const}'


def prettify_method(meth: JavaMemberInfo) -> str:
    access_flags = ''.join(x + ' ' for x in meth.pretty_access_flags())
    throws = ', '.join(meth.pretty_exceptions())
    if throws:
        throws = ' throws ' + throws
    return f'{access_flags}{meth.pretty_type()} {meth.get_name()}({", ".join(meth.pretty_arg_types())}){throws}'


if __name__ == '__main__':
    class_ = load_class_data('java.util.ArrayList')
    print(class_)
