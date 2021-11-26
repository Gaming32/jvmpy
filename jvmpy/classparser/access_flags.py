class AccessFlags:
    access_flags: int

    def __init__(self, a: int) -> None:
        self.access_flags = a
    
    def get_access_flags(self) -> int:
        return self.access_flags
