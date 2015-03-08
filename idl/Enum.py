from idl.Annotatable import Annotatable
from idl.IDLSyntaxError import IDLSyntaxError
from idl.Type import Type


class EnumField(Annotatable):
    '''
    Object that represents a single enumeration field.
    '''
    
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
        
class Enum(Type):
    def __init__(self, module, desc):
        Type.__init__(self, module, Type.ENUM, desc.name)

        self._desc = desc
        
        self._fields = []
        
        for field in self._desc.fields:
            
            if field.value:
                # Evaluate value
                value = eval(field.value)
                
                # Duplicate value check
                for i in self._fields:
                    if i.value == value:
                        raise IDLSyntaxError(self.module,
                                             field.line,
                                             'Duplicate explicit field value %d given for field %r in enumeration %r' % (value, field.name, self.pathStr)
                        )
                
            else:
                value = self._generateFieldValue()
            
            newField = EnumField(self, field.name, value)
            
            # Duplicate name check
            if self.getField(newField.name):
                raise IDLSyntaxError(self.module,
                                     field.line,
                                     'Duplicate field name %r in enumeration %r' % (newField.name, self.pathStr)
                )
            
            # Annotations
            newField._assignAnnotations(field.annotations)
            
            self._fields.append(newField)
            
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
