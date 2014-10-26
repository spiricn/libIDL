class ParserError(Exception):
    def __init__(self, message, token):
        Exception.__init__(self)
        
        self._message = message
        self._token = token
        
    @property
    def token(self):
        return self._token
    
    @property
    def message(self):
        return self._message

