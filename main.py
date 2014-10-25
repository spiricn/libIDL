from idl.Environment import Environment
from idl.Type import Type


source = '''


interface TestIface{
    void test(in callback_register int32[53] arg1);
};


'''

'''






typedef Surface;
'''



# import re

# print([str(i) for i in re.compile('\s').finditer('Te 2s tE num')])

env = Environment()
#             
# 
module = env.compileSource(source)
# 
 
class Asdf:
    @property
    def x(self):
        return 3
    
    
print(Asdf().x)
# print('-'*80)
# print('Done')

