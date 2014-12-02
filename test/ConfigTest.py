from idl.Environment import Environment
import unittest

from idl.IDLNotSupportedError import IDLNotSupportedError
from idl.LangConfig import LangConfig
from test.TestBase import TestBase


class ConfigTest(TestBase):
    def test_inheritance(self):
        '''
        Inheritance LangConfig test.
        '''
        
        src = ''' \
        package com.test;
        
        interface Base{
        };
        
        interface Derived extends Base{
        };
        '''
        
        
        try:
            Environment(LangConfig(inheritance=False)).compileSource(src, 'module1')
            self.fail()
            
        except IDLNotSupportedError:
            pass
        
    def test_overload(self):
        '''
        Operator overloading LangConfig test.
        '''
        
        src = ''' \
        package com.test;
        
        interface Test{
            void test(int32 arg1);
            
            void test();
        };
        '''
        
        
        try:
            Environment(LangConfig(operatorOverload=False)).compileSource(src, 'module1')
            self.fail()
            
        except IDLNotSupportedError:
            pass
        
    def test_preprocessor(self):
        '''
        Operator overloading LangConfig test.
        '''
        
        src = ''' \
        package com.test;
        
        #ifdef ( test )
        interface Test{
            void test(int32 arg1);
            
            void test();
        };
        #endif
        '''
        
        
        try:
            Environment(LangConfig(preprocessor=False)).compileSource(src, 'module1')
            self.fail()
            
        except IDLNotSupportedError:
            pass
        
if __name__ == '__main__':
    unittest.main()
