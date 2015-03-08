from idl.IDLError import IDLError


class IDLSyntaxError(IDLError):
    NAME = 'Syntax'
    
    def __init__(self, module, line, message):
        IDLError.__init__(self, IDLSyntaxError.NAME, message, module, line)
