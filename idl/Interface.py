from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLNotSupportedError import IDLNotSupportedError
from idl.IDLTypeError import IDLTypeError
from idl.Method import Method
from idl.Type import Type


class Interface(Type):
    def __init__(self, module, info):
        Type.__init__(self, module, Type.INTERFACE, info.name)

        self._info = info

        self._methods = []
        
        # Iterate over all method informations received from the parser
        for methodInfo in info.methods:
            # Add it to the list
            self._methods.append( Method(self, methodInfo) )
            
        if self._info.bases and not self.module.package.env.config.inheritance:
            raise IDLNotSupportedError(self.module, self._info.line, 'Interface inheritance not enabled')
            
            
        self._bases = []
        
    @property
    def bases(self):
        return self._bases

    @property
    def dependencies(self):
        res = []
        
        for method in self._methods:
            # Return type
            if method.ret.type not in res and not method.ret.type.isPrimitive:
                res.append( method.ret.type )
            
            # Arguments
            for arg in method.args:
                if arg.type not in res and not arg.type.isPrimitive:
                    res.append( arg.type )

        return res
            
    @property
    def methods(self):
        '''
        List of methods defined in this interface.
        '''
        
        return self._methods
        
    def _link(self):
        '''
        Link all method return types/arguments.
        '''
        
        for method in self._methods:
            method._link()
            
        # Duplicate method names check
        for index, method1 in enumerate(self.methods):
            for method2 in self.methods[index+1:]:
                if method1.name == method2.name:
                    if not self.module.package.env.config.operatorOverload:
                        raise IDLNotSupportedError(self.module, self._info.methods[index].line, 'Operator overloading not enabled')
                    else:
                        if len(method1.args) == len(method2.args):
                            same = True
                            
                            for argIndex, arg in enumerate(method1.args):
                                if arg != method2.args[argIndex]:
                                    same = False
                                    break
                                
                            if same:
                                raise IDLTypeError(self.module, self._info.line, 'Duplicate method detected %s::%s' % (self.name, method1.name))

        # Resolve bases
        for baseTypeInfo in self._info.bases:
            try:
                baseType  = self.module._resolveType(baseTypeInfo)
                
                if baseType == None:
                    raise IDLTypeError(self.module, self._info.line, 'Could not resolve interface base interface %r' % '.'.join(baseTypeInfo.path))
                
                elif baseType.id != Type.INTERFACE:
                    raise IDLTypeError(self.module, self._info.line, 'Interface %r can\'t extend type %r only other interfaces.' % (self._info.name, baseType.name))
                
                else:
                    # Duplicate inheritance check
                    for i in self._bases:
                        if i == baseType:
                            raise IDLTypeError(self.module, self._info.line, 'Duplicate interface inheritance %r' % ('.'.join(i.path)))
                        
                    self._bases.append( baseType )

            except IDLSyntaxError as e:
                # Re-raise exception with module/line information
                raise IDLSyntaxError(self.module, self._info.line, e.message)
