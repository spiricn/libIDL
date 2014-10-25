from idl.Annotatable import Annotatable
from idl.Type import Type


class Struct(Type):
    class Field(Annotatable):
        def __init__(self, struct, fieldType, name):
            Annotatable.__init__(self)
            
            self._struct = struct
            self._type = fieldType
            self._name = name
            
        @property
        def struct(self):
            '''
            Structure type this field is associated with.
            '''
            
            return self._struct
        
        @property
        def type(self):
            '''
            Field type.
            '''
            
            return self._type
        
        @property
        def name(self):
            '''
            Field name.
            '''
            
            return self._name

    def __init__(self, module, info):
        Type.__init__(self, module, Type.STRUCTURE, info.name)

        self._info = info

        self._fields = []
        
    @property
    def fields(self):
        '''
        List of fields defined in this structure.
        '''
        
        return self._fields
    
    def _link(self):
        for field in self._info.fields:
            # Resolve field type
            fieldType = self.module._resolveType(field.typeInfo)
            
            if not fieldType:
                raise RuntimeError('Could not resolve field %r type %r of structure %r' % (field.name, field.typeInfo.name, self.name))
            
            newField = Struct.Field(self, fieldType, field.name)
            
            # Duplicate check
            for i in self._fields:
                if i.name == newField.name:
                    raise RuntimeError('Duplicate field name %r in structure %r' % (field.name, self.name))
                
            # Annotations
            newField._assignAnnotations(field.annotations)
                
            self._fields.append(newField)
