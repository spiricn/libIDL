from idl.Type import Type


class TypeGetter(object):
    '''
    Helper class used for type filtering
    '''
    
    def __init__(self):
        pass

    def getTypes(self, objType):
        '''
        Gets a list of all the objects of specific type
        '''
        
        return [i for i in self.types if i.id == objType]

    def getType(self, name, typeID=-1):
        '''
        Gets object with given type ID and name.
        Helper function used by getXY()
        If 'typeID' param is set to -1, type checks are not performed
        '''
        
        for i in self.types:
            if i.name == name and (typeID == -1 or i.id == typeID):
                return i
            
        return None

    def getEnum(self, name):
        '''
        Gets the enum object with given name.
        '''
        
        return self.getType(name, Type.ENUM)
    
    def getInterface(self, name):
        '''
        Gets the interface object with given name.
        '''
        
        return self.getType(name, Type.INTERFACE)
        
    def getStructure(self, name):
        '''
        Gets structure object with given name.
        '''
        
        return self.getType(name, Type.STRUCTURE)
    
    def getTypedef(self, name):
        '''
        Gets typedef object with given name.
        '''
        
        return self.getType(name, Type.TYPEDEF)
