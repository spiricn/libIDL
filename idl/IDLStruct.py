from idl.RawStruct import RawStruct
from idl.IDLType import IDLType

class IDLStruct(IDLType):
    def __init__(self, parent, header, fields):
        IDLType.__init__(self, IDLType.STRUCTURE)
        
        self.parent = parent
        self.rawStruct = RawStruct(header, fields) 

        self.name = self.rawStruct.name
        
    def create(self):
        self.fields = []
        
        for rawField in self.rawStruct.fields:
            var = self.parent.createVariable(rawField)
            
            if var == None:
                raise RuntimeError('Could not resolve structure field type "%s"' % rawField.type)
            
            self.fields.append(var)
