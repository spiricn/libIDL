from idl.IDLError import IDLError


class IDLImportError(IDLError):
    def __init__(self, module, line, message):
        baseMessage = 'Import error in module %r %s, line %d\n%s' % (module.name if module else '', '(File "' + module.filePath + '")' if (module and module.filePath) else '', line+1, message)
        
        IDLError.__init__(self, baseMessage)

        self._line = line
        
        self._module = module
        
        
    @property
    def line(self):
        return self._line
    
    @property
    def module(self):
        return self._module
