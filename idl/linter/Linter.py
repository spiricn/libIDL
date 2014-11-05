from idl.lexer.Tokenizer import Tokenizer
from idl.parser.Parser import Parser
import os


class Linter:
    @staticmethod
    def verifyModulePackage(sourceTree, path):
        # We need absolute paths for this
        path = os.path.abspath(path)
        
        sourceTree = os.path.abspath(sourceTree)
        
        relPath = path[len(sourceTree) + 1:]
        
        # Get correct package from path
        packagePath = os.path.dirname(relPath).split(os.sep)
        
        with open(path, 'r') as fileObj:
            source = fileObj.read()
            
            # Get declared package from file
            parser = Parser(Tokenizer.tokenize(source))
        
            packageInfo = parser.eatPackageInfo()
            
            # Verify
            return packageInfo.package == packagePath
