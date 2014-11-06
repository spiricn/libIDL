from idl.IDLError import IDLError


class IDLSyntaxError(IDLError):
    def __init__(self, module, line, message):
        IDLError.__init__(self, 'Syntax', message, module, line)
