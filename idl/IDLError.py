class IDLError(Exception):
    def __init__(self, name, baseMessage, module, line):
        
        message = '%s error' % name
        
        if module:
            message += ' in module %r' % module.name
            
            if module.filePath:
                message += ' (File %r )' % module.filePath
                
        if line != None:
            message += ', line %d' % (line + 1)
            
        message += ':\n%s' % baseMessage
        
        Exception.__init__(self, message)
        
        self._module = module
        
        self._line = line
        
    @property
    def line(self):
        '''
        Offending line (may be None)
        '''
        
        return self._line
    
    @property
    def module(self):
        '''
        Offending module (may be None)
        '''
        
        return self._module
