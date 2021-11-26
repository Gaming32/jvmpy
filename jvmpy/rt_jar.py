import os
from pathlib import Path
from shutil import copyfile, which
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from _typeshed import StrPath

JAVA_HOME = os.getenv('JAVA_HOME')
if JAVA_HOME is not None:
    JAVA_HOME = Path(JAVA_HOME)


def follow_symlinks(p: 'StrPath') -> Path:
    p = Path(p)
    while p.is_symlink():
        p = p.readlink()
    return p


def is_valid_dir(dir: Path) -> Optional[Path]:
    return next(dir.glob('rt.jar'), None)


def is_valid_java(dir: Path) -> Optional[Path]:
    return next(dir.glob('lib/rt.jar'), None)


def check_java_home(java_home: Optional[Path]) -> Optional[Path]:
    if java_home is not None:
        if rt := is_valid_java(java_home):
            return rt
        jre8 = next(java_home.parent.glob('jre1.8*'), None)
        if jre8 is not None:
            if rt := is_valid_java(jre8):
                return rt
    return None


def find_rt_jar(allow_assets_dir: bool = True) -> Optional[Path]:
    if allow_assets_dir:
        if rt := is_valid_dir(Path(__file__).parent):
            return rt
    if rt := check_java_home(JAVA_HOME):
        return rt
    java = which('java')
    if java is not None:
        java = follow_symlinks(java)
        if rt := check_java_home(java.parent.parent):
            return rt
    return None


def main() -> None:
    rt = find_rt_jar(False)
    if rt is None:
        print('Found no valid rt.jar')
        exit(1)
    print('Found rt.jar:', rt)

    dest = Path(__file__).parent.joinpath('rt.jar')
    print('Copying', rt, '->', dest)
    copyfile(rt, dest)
    print('Copied', rt, '->', dest)


if __name__ == '__main__':
    main()
