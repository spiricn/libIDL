from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.Parser import Parser

from idl.IDLNotSupportedError import IDLNotSupportedError


class Node:
    def __init__(self, proc, parent, tokens):
        self._parent = parent
        self._parser = Parser(tokens)
        self._tokens = tokens
        self._proc = proc
        
    @property
    def proc(self):
        return self._proc
        
    @property
    def parser(self):
        return self._parser
    
    @property
    def tokens(self):
        return self._tokens
    
    def process(self):
        raise RuntimeError('Not implemented')
    
class Condition:
    def __init__(self, expr, body, keyword):
        self.body = body
        self.expr = expr
        self.keyword = keyword

class TokensNode(Node):
    def __init__(self, proc, parent, tokens):
        Node.__init__(self, proc, parent, tokens)
        
        self._consumedTokens = []
        
        while self.tokens:
            if self.parser.next.id == Token.KEYWORD and self.parser.next.body in [Lang.KEYWORD_IFDEF, Lang.KEYWORD_ELSE, Lang.KEYWORD_ELIF, Lang.KEYWORD_ENDIF]:
                # Done consuming
                break
                
            else:
                self._consumedTokens.append( self.parser.pop() )
                
    def process(self):
        return self._consumedTokens
                
class ConditionalNode(Node):
    def __init__(self,  proc, parent, tokens):
        Node.__init__(self, proc, parent, tokens)
        
        self._conditions = []
        
        currCondition = self._parseCondition()
        
        processedEnd = False
        
        while not processedEnd:
            if not tokens:
                # TODO
                assert(0)
            
            token = tokens[0]
            
            conditionEnd = False
            
            if currCondition.keyword == Lang.KEYWORD_IFDEF and token.body in [Lang.KEYWORD_ENDIF, Lang.KEYWORD_ELSE, Lang.KEYWORD_ELIF]:
                conditionEnd = True
                processedEnd = (token.body == Lang.KEYWORD_ENDIF)
                
            elif currCondition.keyword == Lang.KEYWORD_ELIF and token.body in [Lang.KEYWORD_ENDIF, Lang.KEYWORD_ELSE]:
                processedEnd = (token.body == Lang.KEYWORD_ENDIF)
                conditionEnd = True
                    
            elif currCondition.keyword == Lang.KEYWORD_ELSE and token.body in [Lang.KEYWORD_ENDIF]:
                processedEnd = True
                conditionEnd = True
                
            if conditionEnd:
                # Reached condition end
                self._conditions.append( currCondition )
                
                # New header and body
                currCondition = self._parseCondition()
                
            elif processedEnd:
                self.parser.eat(Token.KEYWORD, Lang.KEYWORD_ENDIF)
                
            else:
                # Consume condition body
                currCondition.body.addChild()
        
    def _parseCondition(self):
        body = ContainerNode(self.proc, self, self.tokens)
        
        # Header
        header = self.parser.pop()
        
        if header.body == Lang.KEYWORD_ENDIF:
            return None
        
        
        elif header.body in [Lang.KEYWORD_IFDEF, Lang.KEYWORD_ELIF]:
            # Openning bracket
            self.parser.eat(Token.PUNCTUATION, '(')
            
            expr = self.parser.eat(Token.ID).body
            
            # Closing bracket
            self.parser.eat(Token.PUNCTUATION, ')')
            
        else:
            expr = None
        
        return Condition(expr, body, header.body)
    
    def process(self):
        passed = None
        
        for condition in self._conditions:
            if condition.keyword == Lang.KEYWORD_ENDIF:
                # None of the conditions passed
                break
            
            elif condition.keyword == Lang.KEYWORD_ELSE:
                # Reached else..
                passed = condition
                break
            
            else:
                # TODO Evaluate a condition
                if self.proc.env.isDefined(condition.expr):
                    passed = condition

                    break

        if passed == None:
            return []
        
        else:
            return passed.body.process()
                
class ContainerNode(Node):
    def __init__(self, proc, parent, tokens):
        Node.__init__(self, proc, parent, tokens)
        
        self._children = []
        
    def addChild(self):
        if self.parser.next.id == Token.KEYWORD and self.parser.next.body == Lang.KEYWORD_IFDEF:
            self._children.append( ConditionalNode(self.proc, self, self.tokens) )
            
        elif self.parser.next.id == Token.KEYWORD and self.parser.next.body in [Lang.KEYWORD_ELSE, Lang.KEYWORD_ELIF, Lang.KEYWORD_ENDIF]:
            # TODO Shouldn't happen
            assert(0)
            
        else:
            self._children.append( TokensNode(self.proc, self, self.tokens) )
            
    def process(self):
        res = []
        
        for child in self._children:
            res += child.process()
            
        return res

class Preprocessor:
    def __init__(self, env, tokens):
        self._tokens = tokens
        self._env = env
        
        # Check if preprocessor is enabled
        if not self._env.config.preprocessor:
            # Check for preprocesor tokens if not
            for token in tokens:
                if token.id == Token.KEYWORD and token.body in [Lang.KEYWORD_IFDEF, Lang.KEYWORD_ELIF, Lang.KEYWORD_ELSE, Lang.KEYWORD_ENDIF]:
                    raise IDLNotSupportedError(None, token.location[0], 'Preprocessor not enabled')
        
    @staticmethod
    def process(env, tokens):
        return Preprocessor(env, tokens)._process()
    
    @staticmethod
    def env(self):
        return self._env
    
    def _process(self):
        tokens = [i for i in self._tokens]
        
        root = ContainerNode(self._env, None, tokens)
        
        while tokens:
            root.addChild()
            
        return root.process()

