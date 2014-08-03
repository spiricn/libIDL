import re

class TokenType(object):
    # Token types
    METHOD, \
    PARAMETER, \
    STRUCT_BEGIN, \
    CLOSING_BRACKET, \
    STRUCT_FIELD, \
    INTERFACE_BEGIN, \
    ARG_LIST_BEGIN, \
    ARG, \
    ARG_LIST_END, \
    = range(9)
    
    def __init__(self, pattern, tokenType, fragmentClass):
        self.pattern = re.compile(pattern)
        self.patternString = pattern
        self.type = tokenType
        self.fragmentClass = fragmentClass
    
    def matches(self, string):
        return self.pattern.match(string)
    
    def instantiate(self, body):
        return self.fragmentClass(self.type, body)
    
    def __eq__(self, other):
        if isinstance(other, TokenType):
            return self == other.type
        
        elif isinstance(other, int):
            return self.type == other
        
        elif other is None:
            return False
        
        else:
            raise NotImplementedError()
    
    def __str__(self):
        return '<TokenType pattern="%s">' % self.patternString
