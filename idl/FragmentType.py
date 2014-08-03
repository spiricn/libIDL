import re

class FragmentType(object):
    # Fragment types
    METHOD, \
    PARAMETER, \
    STRUCT_BEGIN, \
    CLOSING_BRACKET, \
    STRUCT_FIELD, \
    INTERFACE_BEGIN, \
    = range(6)
    
    def __init__(self, pattern, fragmentType, fragmentClass):
        self.pattern = re.compile(pattern)
        self.patternString = pattern
        self.type = fragmentType
        self.fragmentClass = fragmentClass
    
    def matches(self, string):
        return self.pattern.match(string)
    
    def instantiate(self, body):
        return self.fragmentClass(self.type, body)
    
    def __eq__(self, other):
        if isinstance(other, FragmentType):
            return self == other.type
        
        elif isinstance(other, int):
            return self.type == other
        
        elif other is None:
            return False
        
        else:
            raise NotImplementedError()
    
    def __str__(self):
        return '<FragmentType pattern="%s">' % self.patternString
