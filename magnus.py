#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'

#######################################
# ERRORS
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################


# TYPES
TT_ADDR = 'ADDR'  # ind
TT_INT = 'INT'  # int
TT_CHAR = 'CHAR'  # car
TT_VOID = 'VOID'  # vuoto
TT_VEC = 'VEC'  # vettore
TT_CONST = 'CONST'  # costante
TT_FUNC = 'FUNC'  # func

# ARITHMETIC OPERATORS
TT_PLUS = 'PLUS'  # +
TT_MINUS = 'MINUS'  # -
TT_MUL = 'MUL'  # *
TT_DIV = 'DIV'  # /
TT_MOD = 'MOD'  # %

# COMPARISON OPERATORS
TT_EQ = 'EQ'  # =
TT_NEQ = 'NEQ'  # non =
TT_LT = 'LT'  # <
TT_GT = 'GT'  # >
TT_LTEQ = 'LTEQ'  # <=
TT_GTEQ = 'GTEQ'  # >=

# BOOLEAN OPERATORS
TT_NOT = 'NOT'  # non
TT_AND = 'AND'  # e
TT_OR = 'OR'  # o

# RESERVED WORDS
TT_IF = 'IF'  # se
TT_ELSE = 'ELSE'  # altro
TT_RET = 'RET'  # return
TT_INIT = 'INIT'  # inizio
TT_WHILE = 'WHILE'  # mentre

reservedWords = {"se": TT_IF,
                 "altro": TT_ELSE,
                 "mentre": TT_WHILE,
                 "costante": TT_CONST,
                 "ind": TT_ADDR,
                 "int": TT_INT,
                 "car": TT_CHAR,
                 "vettore": TT_VEC,
                 "func": TT_FUNC,
                 "non": TT_NOT,
                 "e": TT_AND,
                 "o": TT_OR,
                 "inizio": TT_INIT,
                 "vuoto": TT_VOID}


# PUNCTUATION
TT_LPAREN = 'LPAREN'  # (
TT_RPAREN = 'RPAREN'  # )
TT_LCBRAC = 'LCBRAC'  # {
TT_RCBRAC = 'RCBRAC'  # }
TT_LSBRAC = 'LSBRAC'  # [
TT_RSBRAC = 'RSBRAC'  # ]
TT_SQUOT = 'SQUOT'  # '
TT_DQUOT = 'DQUOT'  # "
TT_COMMA = 'COMMA'  # ,
TT_END = 'END'  # .
TT_COMMENT = 'COMMENT'

# OTHER OPERATORS
TT_ASSIGN = 'ASSIGN'  # :=


class Token:
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.getChar()

    def getChar(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t\n':
                self.getChar()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.getChar()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.getChar()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.getChar()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.getChar()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD))
                self.getChar()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.getChar()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.getChar()
            elif self.current_char == '{':
                tokens.append(Token(TT_LCBRAC))
                self.getChar()
            elif self.current_char == '}':
                tokens.append(Token(TT_RCBRAC))
                self.getChar()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSBRAC))
                self.getChar()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSBRAC))
                self.getChar()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.getChar()
            elif self.current_char == '.':
                tokens.append(Token(TT_END))
                self.getChar()
            elif self.current_char == '#':
                tokens.append(Token(TT_COMMENT))
                self.getChar()
            elif self.current_char == '\'':
                tokens.append(Token(TT_SQUOT))
                self.getChar()
            elif self.current_char == '\"':
                tokens.append(Token(TT_DQUOT))
                self.getChar()
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ))
                self.getChar()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.getChar()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.getChar()

        return Token(TT_INT, int(num_str))

    def make_identifier(self):
        pass

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
