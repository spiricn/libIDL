from idl.IDLError import IDLError


class IDLImportError(IDLError):
    NAME = 'Import'
    
    def __init__(self, module, line, message):
        IDLError.__init__(self, IDLImportError.NAME, message, module, line)
