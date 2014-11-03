from idl.IDLError import IDLError


class IDLImportError(IDLError):
    def __init__(self, module, line, message):
        baseMessage = 'Import error in module %r %s, line %d\n%s' % (module.name if module else '', '(File "' + module.filePath + '")' if (module and module.filePath) else '', line+1, message)
        
        IDLError.__init__(self, baseMessage)
