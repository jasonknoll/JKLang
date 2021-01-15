# The start of the JK domain-specific language! 
# Use it for math programming and functional programming

# Just will be a command line-based interpreter for now.
# - Arithmetic: (1 + 1), (2*2), (3**2 = 9) etc.
# - Functions: (lambdas for now) '\' used for lambda symbol
#  + \x. \y. x + y -> lambda(x,y) = return x + y
#
# FUTURE ADDITIONS
# - Solving for variables: (3x+2=11, x = 3)
# - Lists:
# - Saving variables: (var = 123), (num + 1, 124)
# - Naming functions: (func f x. x*x), (f 2, 4)
#  + Recursion
#  + Higher order functions: (func f x. x*x), (\x. f(x) * 2. 2), (f(2)*2, 8)

# Type/operator Constants
T_INT = 'INT'
T_PLUS = 'PLUS'
T_MINUS = 'MINUS'
T_MUL = 'MUL'
T_DIV = 'DIV'
T_LPAREN = 'LPAREN'
T_RPAREN = 'RPAREN'
T_LAMBDA = 'LAMBDA'

DIGITS = '0123456789'

# Token have a type, and value (the character)
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


class Error:
    def __init__(self, posStart, posEnd, errorName, details): 
        self.posStart = posStart
        self.posEnd = posEnd
        self.errorName = errorName
        self.details = details

    def asString(self):
        result = f'{self.errorName}:{self.details}'
        result += f'File {self.posStart.fileName}, line {self.posEnd.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, posStart, posEnd, details):
        super().__init__(posStart, posEnd, 'Illegal Character', details)

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fileName = fn
        self.fileText = ftxt

    def advance(self,currentChar): 
        self.idx += 1
        self.col += 1
        
        if currentChar == '\n':
            self.ln += 1
            self.col = 0
        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fileName, self.fileText)

# Splits all chars into tokens
class Lexer:
    def __init__(self, fn, text):
        self.fileName = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar in ' \t':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNum())
            elif self.currentChar == "+":
                tokens.append(Token(T_PLUS))
                self.advance()
            elif self.currentChar == "-":
                tokens.append(Token(T_MINUS))
                self.advance()
            elif self.currentChar == "*":
                tokens.append(Token(T_MUL))
                self.advance()
            elif self.currentChar == "/":
                tokens.append(Token(T_DIV))
                self.advance()
            elif self.currentChar == "(":
                tokens.append(Token(T_LPAREN))
                self.advance()
            elif self.currentChar == ")":
                tokens.append(Token(T_RPAREN))
                self.advance()
            elif self.currentChar == "\\":
                tokens.append(Token(T_LAMBDA))
                self.advance()
            else:
                posStart = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(posStart, self.pos, "'" + char + "'")
        return tokens, None

    # Turn string into integer
    def makeNum(self):
        numStr = ''
        while self.currentChar != None and self.currentChar in DIGITS:
            numStr += self.currentChar
            self.advance()

        return Token(T_INT, int(numStr))

# Nodes for parser

class NumberNode:
    def __init__(self, tok):
        self.token = tok

    def __repr__(self):
        return f'{self.token}'

class BinOpNode:
    def __init__(self, lNode, opTok, rNode):
        self.leftNode = lNode
        self.rightNode = rNode
        self.opToken = opTok

    def __repr__(self):
        return f'({self.leftNode}, {self.opToken}, {self.rightNode})'


def run(fn, text):
    lex = Lexer(fn, text)
    tokens, error = lex.makeTokens()
    return tokens, error

while True:
    text = input("JK > ")
    result, error = run('<stdin>', text)
    if error != None: print(error.asString())
    else: print(result)
