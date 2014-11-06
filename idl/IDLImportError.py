from idl.IDLError import IDLError


class IDLImportError(IDLError):
    def __init__(self, module, line, message):
        IDLError.__init__(self, 'Import', message, module, line)
