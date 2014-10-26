class IDLSyntaxError(Exception):
    def __init__(self, module, token):
        Exception.__init__(self,'Syntax error in module %r %s, line %d\n%s' % (module.name,'(File "' + module.filePath + '")' if module.filePath else '', token.location[0] + 1, token.locationStr))
        
        self._module = module
        self._token = token
        
    @property
    def module(self):
        '''
        Offending module.
        '''
        
        return self._module
    
    @property
    def location(self):
        '''
        Line/column of the syntax error.
        '''
        
        return self._token.location
