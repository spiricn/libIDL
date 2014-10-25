from idl.Type import Type


class Enum(Type):
    class Field:
        def __init__(self, enum, name, value):
            self.enum = enum
            self.name = name
            self.value = value
            
    def __init__(self, module, info):
        Type.__init__(self, module, Type.ENUM, info.name)

        self.info = info
        
        self.fields = []
        
        for field in self.info.fields:
            
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
                    
                    for i in self.fields:
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
            
            self.fields.append(newField)

    def getField(self, name):
        for field in self.fields:
            if field.name == name:
                return field
            
        return None
    
    def _link(self):
        pass
