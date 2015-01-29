from idl.Environment import Environment
import unittest

from idl.IDLNotSupportedError import IDLNotSupportedError
from idl.LangConfig import LangConfig
from test.TestBase import TestBase


class PreprocessorTest(TestBase):
    def test_if(self):
        '''
        Basic #ifdef test
        '''
        
        src = '''\
        package com.test;
        
        #ifdef ( DEFINE_NAME )
        
        interface IfdefedInterface{
        
        };

        #endif

        '''
        
        env = Environment()
        
        env.define('DEFINE_NAME')
        
        module = env.compileSource(src, 'module')
        
        self.assertTrue(len(module.types), 1)
        
    def test_elif(self):
        '''
        Basic #ifdef test
        '''
        
        src = '''\
        package com.test;
        
        #ifdef ( DEFINE_NAME_1 )
        
        interface IfdefedInterface{
        
        };
        
        #elif ( DEFINE_NAME_2 )
        
        interface ElifdefedInterface{
        
        };

        #endif

        '''
        
        env = Environment()
        
        env.define('DEFINE_NAME_2')
        
        module = env.compileSource(src, 'module')
        
        self.assertTrue(len(module.types), 1)
        
        self.assertEqual(module.types[0].name, 'ElifdefedInterface')
        
    def test_else(self):
        '''
        Basic #else test
        '''
        
        src = '''\
        package com.test;
        
        #ifdef ( DEFINE_NAME_1 )
        
        interface IfdefedInterface{
        
        };
        
        #elif ( DEFINE_NAME_2 )
        
        interface ElifdefedInterface{
        
        };
        
        #else
        
        interface ElsedInterface{
        
        };

        #endif

        '''
        
        env = Environment()
        
        module = env.compileSource(src, 'module')
        
        self.assertTrue(len(module.types), 1)
        
        self.assertEqual(module.types[0].name, 'ElsedInterface')
        
if __name__ == '__main__':
    unittest.main()
