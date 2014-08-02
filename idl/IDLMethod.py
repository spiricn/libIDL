from idl.Method import Method
from idl.IDLType import IDLType
from idl.IDLMethodArgument import IDLMethodArgument

class IDLMethod(object):
    TYPE_METHOD, \
    TYPE_CALLBACK_REGISTER, \
    TYPE_CALLBACK_UNREGISTER, \
    TYPE_CALLBACK_DECLARATION, \
    = range(4)
    
    MOD_CALLBACK_DECLARATION = 'callback'
    MOD_CALLBACK_REGISTER = 'callback_register'
    MOD_CALLBACK_UNREGISTER = 'callback_unregister'
    
    def __init__(self, parent, fragment):
        self.parent = parent
        
        # Create a method from the fragment
        try:
            rawMethod = Method(fragment)
        except Exception as e:
            raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (fragment.body, str(e)))
        
        # Determine method type
        if not rawMethod.mods:
            # No modifier, it's a regular method
            self.type = IDLMethod.TYPE_METHOD
            
        elif len(rawMethod.mods) > 1:
            raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (fragment.body, "Unrecognized method modifier"))
        
        else:
            mod = rawMethod.mods[0]
            
            if mod == IDLMethod.MOD_CALLBACK_DECLARATION:
                self.type = IDLMethod.TYPE_CALLBACK_DECLARATION
                
            elif mod == IDLMethod.MOD_CALLBACK_REGISTER:
                self.type = IDLMethod.TYPE_CALLBACK_REGISTER
                 
            elif mod == IDLMethod.MOD_CALLBACK_UNREGISTER:
                self.type = IDLMethod.TYPE_CALLBACK_UNREGISTER
                
            else:
                raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (fragment.body, "Unrecognized method modifier \"%s\"" % mod))
            
        # Method name
        self.name = rawMethod.name
        
        # Method return type
        self.returnType = IDLType(rawMethod.returnType)
        
        if self.returnType == IDLType.INVALID:
            raise RuntimeError('Invalid method return type "%s"' % rawMethod.returnType)
        
        self.rawMethod = rawMethod
        
        # Only valid if we're a callback register/unregister methods
        self.callbackType = None

    def createArgList(self):
        self.args = []
        
        for arg in self.rawMethod.args:
            argType = IDLType(arg.type)
            
            if argType == IDLType.INVALID:
                # Is it a callback?
                for method in self.parent.getMethods(IDLMethod.TYPE_CALLBACK_DECLARATION):
                    if method.name == arg.type:
                        # It's a callback
                        argType = IDLType(IDLType.CALLBACK, method)
                        break
               
                if argType == IDLType.INVALID:     
                    raise RuntimeError('Invalid method arrgument type method="%s"; argument="%s"' % (self.rawMethod.body, arg.type))
                
            self.args.append( IDLMethodArgument(argType, arg.name) )
    
        # Deduce callback type from method arguments
        if self.type in [IDLMethod.TYPE_CALLBACK_REGISTER, IDLMethod.TYPE_CALLBACK_UNREGISTER]:
            numCallbackTypes = 0
            
            for arg in self.args:
                if arg.type == IDLType.CALLBACK:
                    numCallbackTypes += 1
                    self.callbackType = arg.type.associatedMethod
                    
            if numCallbackTypes != 1:
                raise RuntimeError('Could not deduce callback type from arguments list in method "%s"' % self.rawMethod.body)
            
    def __str__(self):
        return '<IDLMethod name="%s" type=%d>' % (self.name, self.type)
