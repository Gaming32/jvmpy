from typing import Union
from jvmpy.classparser.exceptions import ClassFormatException

from . import constants

CONSUMER_CHARS = [0]


def unwrap(t1: list[int]):
    return t1[0]


def wrap(t1: list[int], value: int):
    t1[0] = value


def compact_class_name(s: str, chopit_prefix: Union[bool, str] = None, chopit: bool = None):
    if chopit_prefix is None:
        prefix = 'java.lang.'
        chopit = True
    elif isinstance(chopit_prefix, bool):
        prefix = 'java.lang.'
        chopit = chopit_prefix
    else:
        prefix = chopit_prefix
    length = len(prefix)
    s = s.replace('/', '.')
    if chopit and s.startswith(prefix) and s[length:].find('.') == -1:
        s = s[length:]
    return s


def access_to_string(access_flags: int, for_class: bool = False) -> str:
    result = ''
    p = 0
    i = 0
    while p < constants.MAX_ACC_FLAG_I:
        p = 2 ** i
        if access_flags & p:
            if for_class and p in (constants.ACC_SUPER, constants.ACC_INTERFACE):
                continue
            result += f'{constants.get_access_name(i)} '
        i += 1
    return result.strip()


def type_signature_to_string(signature: str, chopit: bool) -> str:
    wrap(CONSUMER_CHARS, 1)
    try:
        c = signature[0]
        if c == 'B':
            return 'byte'
        elif c == 'C':
            return 'char'
        elif c == 'D':
            return 'double'
        elif c == 'F':
            return 'float'
        elif c == 'I':
            return 'int'
        elif c == 'J':
            return 'long'
        elif c == 'T':
            index = signature.find(';')
            if index < 0:
                raise ClassFormatException(f'Invalid type variable signature: {signature}')
            wrap(CONSUMER_CHARS, index + 1)
            return compact_class_name(signature[1:index], chopit)
        elif c == 'L':
            from_index = signature.find('<')
            if from_index < 0:
                from_index = 0
            else:
                from_index = signature.find('>', from_index)
                if from_index < 0:
                    raise ClassFormatException(f'Invalid signature: {signature}')
            index = signature.find(';', from_index)
            if index < 0:
                raise ClassFormatException(f'Invalid signature: {signature}')
            bracket_index = signature[:index].find('<')
            if bracket_index < 0:
                wrap(CONSUMER_CHARS, index + 1)
                return compact_class_name(signature[1:index], chopit)
            from_index = signature.find(';')
            if from_index < 0:
                raise ClassFormatException(f'Invalid signature: {signature}')
            if from_index < bracket_index:
                wrap(CONSUMER_CHARS, from_index + 1)
                return compact_class_name(signature[1:from_index], chopit)
            type = f'{compact_class_name(signature[1:bracket_index], chopit)}<'
            consumed_chars = bracket_index + 1
            if signature[consumed_chars ] == '+':
                type += '? extends '
                consumed_chars += 1
            elif signature[consumed_chars] == '-':
                type += '? super '
                consumed_chars += 1
            if signature[consumed_chars] == '*':
                type += '?'
                consumed_chars += 1
            else:
                type += type_signature_to_string(signature[consumed_chars:], chopit)
                consumed_chars += unwrap(CONSUMER_CHARS)
                wrap(CONSUMER_CHARS, consumed_chars)
            while signature[consumed_chars] != '>':
                type += ', '
                if signature[consumed_chars] == '+':
                    type += '? extends '
                    consumed_chars += 1
                elif signature[consumed_chars] == '-':
                    type += '? super '
                    consumed_chars += 1
                if signature[consumed_chars] == '*':
                    type += '?'
                    consumed_chars += 1
                else:
                    type += type_signature_to_string(signature[consumed_chars:], chopit)
                    consumed_chars += unwrap(CONSUMER_CHARS)
                    wrap(CONSUMER_CHARS, consumed_chars)
            consumed_chars += 1
            type += '>'
            if signature[consumed_chars] == '.':
                type += '.'
                type += type_signature_to_string('L' + signature[consumed_chars + 1:], chopit)
                consumed_chars += unwrap(CONSUMER_CHARS) + consumed_chars
                wrap(CONSUMER_CHARS, consumed_chars)
                return type
            if signature[consumed_chars] != ';':
                raise ClassFormatException(f'Invalid signature: {signature}')
            wrap(CONSUMER_CHARS, consumed_chars + 1)
            return type
        elif c == 'S':
            return 'short'
        elif c == 'Z':
            return 'boolean'
        elif c == '[':
            brackets = ''
            n = 0
            while n == '[':
                brackets += '[]'
                n += 1
            consumed_chars = n
            type = type_signature_to_string(signature[n:], chopit)
            _temp = unwrap(CONSUMER_CHARS) + consumed_chars
            wrap(CONSUMER_CHARS, _temp)
            return type + brackets
        elif c == 'V':
            return 'void'
        else:
            raise ClassFormatException(f'Invalid signature: `{signature}`')
    except IndexError as e:
        raise ClassFormatException(f'Invalid signature: {signature}') from e


def signature_to_string(signature: str, chopit: bool = True) -> str:
    type = ''
    type_params = ''
    index = 0
    if signature[0] == '<':
        type_params = type_param_types_to_string(signature, chopit)
        index += unwrap(CONSUMER_CHARS)
    if signature[index] == '(':
        type = type_params + type_signatures_to_string(signature[index:], chopit, ')')
        index += unwrap(CONSUMER_CHARS)
        type += type_signature_to_string(signature[index:], chopit)
        index += unwrap(CONSUMER_CHARS)
        return type
    type = type_signature_to_string(signature[index:], chopit)
    index += unwrap(CONSUMER_CHARS)
    if not type_params and index == len(signature):
        return type
    type_class = type_params
    type_class += f' extends {type}'
    if index < len(signature):
        type_class += f' implements {type_signature_to_string(signature[index:], chopit)}'
        index += unwrap(CONSUMER_CHARS)
    while index < len(signature):
        type_class += f', {type_signature_to_string(signature[index:], chopit)}'
        index += unwrap(CONSUMER_CHARS)
    return type_class
