class EnumField(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __str__(self):
        return  '<EnumField %s; %s>' % (self.name, self.value)
