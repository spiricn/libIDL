import re
from idl.Utils import *
from idl.RawVariable import RawVariable

class RawStruct(object):
    def __init__(self, header, fields):
        # Parse struct name
        r = re.compile(WHITESPACE_MATCH + 'struct' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        self.name = r.search(header.body).group(1)

        # Parse struct fields        
        self.fields = []
        
        for fragment in fields:
            fieldType, fieldName = [i for i in fragment.body.replace('\t', '').replace(';', '').split(' ') if i]
            
            self.fields.append( RawVariable(fieldType, fieldName) )
