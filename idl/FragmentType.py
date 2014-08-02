import re

class FragmentType(object):
    # Fragment types
    METHOD, \
    PARAMETER, \
    = range(2)
    
    def __init__(self, pattern, fragmentType, fragmentClass):
        self.pattern = re.compile(pattern)
        self.patternString = pattern
        self.type = fragmentType
        self.fragmentClass = fragmentClass
    
    def matches(self, string):
        return self.pattern.match(string)
    
    def instantiate(self, body):
        return self.fragmentClass(self.type, body)
    
    def __str__(self):
        return '<FragmentType pattern="%s">' % self.patternString
