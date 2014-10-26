class IDLSyntaxError(Exception):
    def __init__(self, module, line, message):
        # Exception message
        baseMessage = 'Syntax error in module %s %s, line %d\n%s' % (module.name if module else '', '(File "' + module.filePath + '")' if (module and module.filePath) else '', line+1, message)
         
        Exception.__init__(self, baseMessage)
        
        self._module = module
        
        self._message = message
        
        self._line = line
        
    @property
    def module(self):
        '''
        Offending module.
        '''
        
        return self._module
    
    @property
    def line(self):
        '''
        Line of the syntax error.
        '''
        
        return self._line

    @property
    def message(self):
        return self._message
