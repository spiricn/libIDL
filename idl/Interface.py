from idl.IDLType import IDLType
from idl.Utils import *
from idl.FragmentType import FragmentType
from idl.IDLMethod import IDLMethod

import re

class IDLInterface(IDLType):
    def __init__(self, module, fragments):
        IDLType.__init__(self, IDLType.INTERFACE)
        
        self.module = module
        
        header = fragments.pop(0)
        # Sanity check
        assert(header.type == FragmentType.INTERFACE_BEGIN)
        
        # Parse interface name
        r = re.compile(WHITESPACE_MATCH + 'interface' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        self.name = r.search(header.body).group(1)
        
        self.methods = []
        
        while fragments:
            fragment = fragments[0]
            
            if fragment.type == FragmentType.METHOD:
                method = self.createMethod(fragments)
                
                self.methods.append( method )
            
            elif fragment.type == FragmentType.CLOSING_BRACKET:
                fragments.pop(0)
                break
            
            else:
                raise RuntimeError('Unexpected fragment type found while parsing interface: "%s"' % fragment.body)
            
    def getMethod(self, name):
        for i in self.methods:
            if i.name == name:
                return i
            
        return None
        
    def createMethod(self, fragments):
        fragment = fragments.pop(0)
        
        # Sanity check
        assert(fragment.type == FragmentType.METHOD)
        
        method = IDLMethod(self, self.module, fragment)
        
        return method 
    
    def create(self):
        for method in self.methods:
            method.create()
            
    def createVariable(self):
        return self.parent.createVariable()