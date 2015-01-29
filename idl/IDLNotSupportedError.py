from idl.IDLError import IDLError


class IDLNotSupportedError(IDLError):
    def __init__(self, module, line, message):
        IDLError.__init__(self, 'Support', message, module, line)
