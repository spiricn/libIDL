from idl.Annotatable import Annotatable
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
                try:
                    value = eval(field.value)
                except Exception as e:
                    raise RuntimeError('Could not evaluate field %r value %r of enum %r: %s' % (field.name, field.value, self.name, str(e)))
                
            else:
                # Assign value
                value = 0
                while True:
                    taken = False
                    
                    for i in self._fields:
                        if i.value == value:
                            taken = True
                            value += 1
                            break
                        
                    if not taken:
                        break
            
            newField = Enum.Field(self, field.name, value)
            
            # Duplicate check
            if self.getField(newField.name):
                raise RuntimeError('Enum %s duplicate field name %r' % (self.name, newField.name))
            
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
        for field in self._fields:
            if field.name == name:
                return field
            
        return None
    
    def _link(self):
        pass
