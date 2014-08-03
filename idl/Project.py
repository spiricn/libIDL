from idl.Module import Module

class Project:
    def __init__(self):
        self.modules = {}
    
    def addModule(self, name, path):
        # Read the source from a file
        try:
            file = open(path, 'r')
        except:
            raise RuntimeError('Error oppening IDL file for reading "%s"' % path)
        
        source = file.read()
        
        file.close()
        
        # Try to parse it
        try:
            module = Module(source)
        except Exception as e:
            raise RuntimeError('Error parsing IDL file "%s"; reason "%s"' % (path, str(e)))
        
        if name in self.modules:
            raise RuntimeError('Interface with name "%s" already added to the project' % name)
        
        # Save the parsed module
        self.modules[name] = module
