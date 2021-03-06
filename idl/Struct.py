from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
from idl.Type import Type
from idl.Variable import Variable

class StructField(Variable):
    def __init__(self, struct, fieldType, name, mods, arraySize):
        Variable.__init__(self, fieldType, name, mods, arraySize)
        
        self._struct = struct
        
    @property
    def struct(self):
        '''
        Structure type this field is associated with.
        '''
        
        return self._struct
        
class Struct(Type):
    def __init__(self, module, desc):
        Type.__init__(self, module, Type.STRUCTURE, desc.name)

        self._desc = desc

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
            if field.type not in res and not field.type.isPrimitive:
                res.append(field.type)
                
        return res
    
    def _link(self):
        for field in self._desc.fields:
            # Resolve field type
            try:
                fieldType = self.module._resolveType(field.typeDesc)
            except IDLSyntaxError as e:
                # Re-raise exception with module/line information
                raise IDLSyntaxError(self.module, field.line, e.message)
            
            if not fieldType:
                raise IDLTypeError(self.module, field.line, 'Could not resolve field %r type %r of structure %r' % (field.name, field.typeDesc.pathStr, self.name))
            
            newField = StructField(self, fieldType, field.name, Variable._resolveModifiers(fieldType, field.typeDesc.mods), field.typeDesc.arraySize)
            
            # Duplicate check
            for i in self._fields:
                if i.name == newField.name:
                    raise IDLSyntaxError(self.module, field.line, 'Duplicate field name %r in structure %r' % (field.name, self.name))
                
            # Annotations
            newField._assignAnnotations(field.annotations)
                
            self._fields.append(newField)
