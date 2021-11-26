import sys
from pprint import pp

from javatools import JavaMemberInfo

from jvmpy.utils import load_class_data, prettify_field, prettify_method


def main():
    class_name = sys.argv[1]
    class_data = load_class_data(class_name)
    if class_data is None:
        print('Class', class_name, 'not found')
        return
    print('Found', class_data.get_sourcefile())
    print('Fields:')
    for field in class_data.fields:
        assert isinstance(field, JavaMemberInfo)
        print('  ', prettify_field(field))
    print('Methods:')
    for method in class_data.methods:
        assert isinstance(method, JavaMemberInfo)
        print('  ', prettify_method(method))


if __name__ == '__main__':
    main()
