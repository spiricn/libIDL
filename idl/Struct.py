from idl.Annotatable import Annotatable
from idl.Type import Type
from idl.Variable import Variable

from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError


class Struct(Type):
    class Field(Variable):
        def __init__(self, struct, fieldType, name, mods):
            Variable.__init__(self, fieldType, name, mods)
            
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
            
            newField = Struct.Field(self, fieldType, field.name, Variable._resolveModifiers(fieldType, field.typeInfo.mods))
            
            # Duplicate check
            for i in self._fields:
                if i.name == newField.name:
                    raise IDLSyntaxError(self.module, field.line, 'Duplicate field name %r in structure %r' % (field.name, self.name))
                
            # Annotations
            newField._assignAnnotations(field.annotations)
                
            self._fields.append(newField)
