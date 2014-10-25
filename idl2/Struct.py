from idl.Type import Type


class Struct(Type):
    class Field:
        def __init__(self, struct, fieldType, name):
            self.struct = struct
            self.fieldType = fieldType
            self.name = name

    def __init__(self, module, info):
        Type.__init__(self, module, Type.STRUCTURE, info.name)

        self.info = info

        self.fields = []
        
    def _link(self):
        for field in self.info.fields:
            # Resolve field type
            fieldType = self.module.env.resolveType(field.typeName)
            
            if not fieldType:
                raise RuntimeError('Could not resolve field %r type %r of structure %r' % (field.name, field.typeName, self.name))
            
            newField = Struct.Field(self, fieldType, field.name)
            
            # Duplicate check
            for i in self.fields:
                if i.name == newField.name:
                    raise RuntimeError('Duplicate field name %r in structure %r' % (field.name, self.name))
                
            self.fields.append(newField)
