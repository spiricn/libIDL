from idl.Environment import Environment 
from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
import os
import unittest

from idl.IDLError import IDLError
from test.TestBase import TestBase


class PackageTest(TestBase):
    def test_package_import(self):
        '''
        Basic package import test.
        '''
        
        
        src1 = '''
        package com.test1;

        typedef Src1Type;
        
        '''
        
        
        src2 = '''
        package com.test2;
        
        import com.test1;
        
        interface  Test{
            void test(com.test1.module1.Src1Type arg1);
        };
        
        typedef Src2Type;
        '''
        
        src3 = '''
        package other.test;
        
        import com;
        
        struct Test{
            com.test1.module1.Src1Type field1;
            
            com.test2.module2.Src2Type field2;
        };
        
        '''
        
        env = Environment()
        
        env.compileSource(src1, 'module1')
        
        env.compileSource(src2, 'module2')
        
        env.compileSource(src3, 'module3')
        
    def test_module_import(self):
        '''
        Basic module import test.
        '''
        
        
        src1 = '''
        package com.test1;

        typedef Src1Type;
        
        '''
        
        
        src2 = '''
        package com.test2;
        
        import com.test1.module1;
        
        interface Test{
            void test(com.test1.module1.Src1Type arg1);
        };
        '''
        
        
        env = Environment()
        
        env.compileSource(src1, 'module1')
        
        env.compileSource(src2, 'module2')
        
    def test_type_import(self):
        '''
        Basic type import test.
        '''
        
        
        src1 = '''
        package com.test1;

        typedef Src1Type;
        
        '''
        
        
        src2 = '''
        package com.test2;
        
        from com.test1.module1 import Src1Type;
        
        interface  Test{
            void test(Src1Type arg1);
        };
        '''
        
        
        env = Environment()
        
        env.compileSource(src1, 'module1')
        
        env.compileSource(src2, 'module2')
        
    def test_errors(self):
        '''
        Package/import related errors test.
        '''
        
        # Missing package
        src = '''\
        package com.test;
        
        import com.unexisting;
        '''
        
        try:
            Environment().compileSource(src, 'test1')
            
            self.fail()
        except IDLError:
            pass
        
        # Missing package declaration
        src = '''\
        
        typedef test;
        '''
        
        try:
            Environment().compileSource(src, 'test1')
            
            self.fail()
        except IDLError:
            pass
        
        # Import type
        # Missing package declaration
        src1 = '''\
        package com.test;
        
        typedef Src1Type;
        '''
        
        src2 = '''\
        package com.test;
        
        import com.test.module1.Src1Type;
             
        '''

        try:        
            env = Environment() 
            env.compileSource(src1, 'module1')
            env.compileSource(src2, 'module2')
            
            self.fail()
        except:
            pass
    
if __name__ == '__main__':
    unittest.main()
