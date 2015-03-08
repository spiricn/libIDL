class InterfaceDesc:
    '''
    Interface description.
    '''
    
    def __init__(self, name='', methods=[], bases=[], line=-1):
        # Interface name
        self.name = name
        
        # List of method descriptions
        self.methods = methods if methods else []
        
        # List of base interface names this interface is extending
        self.bases = bases if bases else []
        
        # Line at which this interface was declared
        self.line = line
        
class MethodDesc:
    '''
    Interface method description.
    '''
    
    def __init__(self, name='', args=[], returnType=None, line=-1):
        # Method name
        self.name = name
        
        # List of argument descriptions
        self.args = args if args else []
        
        # Method return type description
        self.returnTypeDesc = returnType
        
        # Line at which this method was declared
        self.line = line
        
class MethodArgDesc:
    '''
    Method argument description.
    '''
    
    def __init__(self, varDesc=None, line=-1):
        # Variable description (e.g. name + type)
        self.varDesc = varDesc
        
        # Line at which this argument was declared
        self.line = line

class EnumFieldDesc:
    '''
    Enumeration field description.
    '''
    
    def __init__(self, name='', value='', line=-1):
        # Field name
        self.name = name
        
        # Field value string (may be hex or decimal base)
        self.value = value
        
        # Line at which this field was declared
        self.line = line
            
class EnumDesc(object):
    '''
    Enumeration description.
    '''
    
    def __init__(self, name='', fields=None, line=-1):
        # Enumeration name
        self.name = name
        
        # List of enumeration field descriptions
        
        self.fields = [] if fields == None else fields
        
        
        # Line at which this enumeration was declared
        self.line = line
        
    
class TypeDesc:
    '''
    Type description.
    '''
    
    def __init__(self, path=[], mods=[], arraySize=None):
        # Path string of this type (i.e. package + name or just name)
        self.path = path if path else []
        
        # List of type modifiers strings (e.g. in, out, inout)
        self.mods = mods if mods else []
        
        # Array size of this type (may be None if type is not an array)
        self.arraySize = arraySize
        
    @property
    def pathStr(self):
        '''
        Path string.
        '''
        
        return '.'.join(self.path)
        
class VariableDesc:
    '''
    Variable description (i.e. type + name).
    '''
    
    def __init__(self, name='', typeDesc=None):
        # Variable name
        self.name = name
        
        # Variable type description
        self.typeDesc = typeDesc
        
class AnnotationDesc:
    '''
    Annotation description.
    '''
    
    def __init__(self, name='', value='', isComment=False):
        # Annotation name
        self.name = name
        
        # Annotation value
        self.value = value
        
        # Comment indicator
        self.isComment = isComment
        
class PackageDesc:
    '''
    Package description.
    '''
    
    def __init__(self, package=''):
        # Package description string
        self.package = package
        
class ImportDesc:
    '''
    Single import description.
    '''
    
    def __init__(self, path='', line=-1):
        # Path this statement is importing
        self.path = path
        
        # Line at which this import statement is declared
        self.line = line
        
    @property
    def pathStr(self):
        '''
        Import path string.
        '''
        return '.'.join(self.path)
        
class ImportsDesc:
    '''
    Module imports description.
    '''
    
    def __init__(self, imports=[]):
        # List of import descriptions
        self.imports = imports if imports else []
        
class StructFieldDesc:
    '''
    Structure field description.
    '''
    
    def __init__(self, typeDesc=None, name='', line=-1):
        # Field type description
        self.typeDesc = typeDesc
        
        # Field name description
        self.name = name
        
        # Line at which this field was declared
        self.line = line

class StructDesc:
    '''
    Structure description.
    '''
    
    def __init__(self, name='', fields=[]):
        # Structure name
        self.name = name
        
        # Structure field descriptions
        self.fields = fields if fields else []

class TypedefDesc:
    '''
    Typedef description.
    '''
    
    def __init__(self, typeName=''):
        # Typedef name
        self.typeName = typeName
