from idl.IDLType import IDLType
from idl.Utils import *
import re

class IDLInterface(IDLType):
    def __init__(self, header):
        IDLType.__init__(self, IDLType.INTERFACE)
        
        # Parse interface name
        r = re.compile(WHITESPACE_MATCH + 'interface' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        self.name = r.search(header.body).group(1)
        
        self.methods = []
        
    def create(self):
        # We're just a collection of methods, so there's nothing really to create
        pass