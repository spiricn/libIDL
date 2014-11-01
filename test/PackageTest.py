from idl.Environment import Environment 
from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
import os
import unittest

from idl.IDLError import IDLError
from test.TestBase import TestBase


class PackageTest(TestBase):
    def test_basic(self):
        '''
        Basic imports tests.
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
        
        # Double import
        src1 = '''\
        package com.test;
        
        import com.unexisting;
        '''
        
        src2 = '''
        package com.test2;
        
        import com.test;
        import com.test;
        '''
        
        try:
            env = Environment()
            env.compileSource(src1, 'test1')
            env.compileSource(src2, 'test2')
            
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
    
if __name__ == '__main__':
    unittest.main()
