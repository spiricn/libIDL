from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
from idl.Type import Type
from idl.Variable import Variable


class Struct(Type):
    class Field(Variable):
        def __init__(self, struct, fieldType, name, mods, arraySize):
            Variable.__init__(self, fieldType, name, mods, arraySize)
            
            self._struct = struct
            
        @property
        def struct(self):
            '''
            Structure type this field is associated with.
            '''
            
            return self._struct

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
    
    @property
    def dependencies(self):
        res = []
        
        for field in self._fields:
            if field.type not in res and not field.type.isPrimitive and not field.isArray:
                res.append(field.type)
                
        return res
    
    def _link(self):
        for field in self._info.fields:
            # Resolve field type
            try:
                fieldType = self.module._resolveType(field.typeInfo)
            except IDLSyntaxError as e:
                # Re-raise exception with module/line information
                raise IDLSyntaxError(self.module, field.line, e.message)
            
            if not fieldType:
                raise IDLTypeError(self.module, field.line, 'Could not resolve field %r type %r of structure %r' % (field.name, field.typeInfo.pathStr, self.name))
            
            newField = Struct.Field(self, fieldType, field.name, Variable._resolveModifiers(fieldType, field.typeInfo.mods), field.typeInfo.arraySize)
            
            # Duplicate check
            for i in self._fields:
                if i.name == newField.name:
                    raise IDLSyntaxError(self.module, field.line, 'Duplicate field name %r in structure %r' % (field.name, self.name))
                
            # Annotations
            newField._assignAnnotations(field.annotations)
                
            self._fields.append(newField)
