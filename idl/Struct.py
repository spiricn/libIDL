from idl.Annotatable import Annotatable
from idl.Type import Type


class Struct(Type):
    class Field(Annotatable):
        def __init__(self, struct, fieldType, name):
            Annotatable.__init__(self)
            
            self.struct = struct
            self.type = fieldType
            self.name = name

    def __init__(self, module, info):
        Type.__init__(self, module, Type.STRUCTURE, info.name)

        self.info = info

        self.fields = []
        
    def _link(self):
        for field in self.info.fields:
            # Resolve field type
            fieldType = self.module._resolveType(field.typeInfo)
            
            if not fieldType:
                raise RuntimeError('Could not resolve field %r type %r of structure %r' % (field.name, field.typeInfo.name, self.name))
            
            newField = Struct.Field(self, fieldType, field.name)
            
            # Duplicate check
            for i in self.fields:
                if i.name == newField.name:
                    raise RuntimeError('Duplicate field name %r in structure %r' % (field.name, self.name))
                
            # Annotations
            newField._assignAnnotations(field.annotations)
                
            self.fields.append(newField)
