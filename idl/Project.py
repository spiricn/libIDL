from idl.IDLModule import IDLModule

class Project:
    def __init__(self):
        self.modules = {}
    
    def addModule(self, path):
        # Read the source from a file
        try:
            file = open(path, 'r')
        except:
            raise RuntimeError('Error oppening IDL file for reading "%s"' % path)
        
        source = file.read()
        
        file.close()
        
        # Try to parse it
        try:
            module = IDLModule(source)
        except Exception as e:
            raise RuntimeError('Error parsing IDL file "%s"; reason "%s"' % (path, str(e)))
        
        if module.interfaceName in self.modules:
            raise RuntimeError('Interface with name "%s" already added to the project' % module.interfaceName)
        
        # Save the parsed module
        self.modules[module.interfaceName] = module
