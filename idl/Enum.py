from idl.Annotatable import Annotatable
from idl.IDLSyntaxError import IDLSyntaxError
from idl.Type import Type


class Enum(Type):
    class Field(Annotatable):
        def __init__(self, enum, name, value):
            Annotatable.__init__(self)
            
            self._enum = enum
            
            self._name = name
            
            self._value = value
            
        @property
        def enum(self):
            '''
            Enumeration type this field is associated with.
            '''
            
            return self._enum
        
        @property
        def name(self):
            '''
            Field name.
            '''
            
            return self._name
        
        @property
        def value(self):
            '''
            Integer field value.
            '''
            
            return self._value
            
    def __init__(self, module, info):
        Type.__init__(self, module, Type.ENUM, info.name)

        self._info = info
        
        self._fields = []
        
        for field in self._info.fields:
            
            if field.value:
                # Evaluate value
                value = eval(field.value)
                
                # Duplicate value check
                for i in self._fields:
                    if i.value == value:
                        raise IDLSyntaxError(self.module, field.line, 'Enum %r duplicate explicit field value %d for field %r' % (self.name, value, field.name))
                
            else:
                value = self._generateFieldValue()
            
            newField = Enum.Field(self, field.name, value)
            
            # Duplicate name check
            if self.getField(newField.name):
                raise IDLSyntaxError(self.module, field.line, 'Enum %r duplicate field name %r' % (self.name, newField.name))
            
            # Annotations
            newField._assignAnnotations(field.annotations)
            
            self._fields.append(newField)
            
    def _generateFieldValue(self):
        # Assign value
        value = 0
        
        while True:
            taken = False
            
            for field in self._fields:
                if field.value == value:
                    taken = True
                    value += 1
                    break
                
            if not taken:
                break
            
        return value

    @property
    def fields(self):
        '''
        List of enumeration fields.
        '''
        
        return self._fields
    
    def getField(self, name):
        '''
        Gets a field with a specific name.
        
        @param name: Field name.
        
        @return: EnumField object or None.
        '''
        
        for field in self._fields:
            if field.name == name:
                return field
            
        return None
