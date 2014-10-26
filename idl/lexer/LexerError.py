class LexerError(Exception):
    def __init__(self, token):
        Exception.__init__(self, 'Unrecognized token encountered\n%s' % token.locationStr)
        
        self._token = token
        
    @property
    def token(self):
        '''
        Offending token.
        '''
        
        return self._token
