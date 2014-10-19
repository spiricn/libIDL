from idl.Annotatable import Annotatable


class EnumField(Annotatable):
    def __init__(self, name, value):
        Annotatable.__init__(self)
        
        self.name = name
        self.value = value
        
    def __str__(self):
        return  '<EnumField %s; %s>' % (self.name, self.value)
