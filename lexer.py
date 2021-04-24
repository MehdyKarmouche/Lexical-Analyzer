import re
import string

#######################################
# CONSTANTS
#######################################

ALPHABET = string.ascii_letters
DIGITS = string.digits
DELIM = string.whitespace
ARITHMETIC_OPERATORS = '+-*/%'
RELOP = '<>='
PUNCTUATION = '[]\{\}(),.'

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


# LITERAL TYPES
TT_ADDR = 'ADDR'  # 8231
TT_INT = 'INT'  # 123
TT_CHAR = 'CHAR'  # 'a'
TT_VEC_INT = 'VEC_INT'  # [1,2,3]
TT_VEC_CHAR = 'VEC_CHAR'  # "ABC"
TT_CONST = 'CONST'  # 3
TT_FUNC = 'FUNC'

# TYPES
TT_ADDR_T = 'ADDR_TYPE'  # ind
TT_INT_T = 'INT_TYPE'  # int
TT_CHAR_T = 'CHAR_TYPE'  # car
TT_VEC_T = 'VEC_TYPE'  # vettore
TT_CONST_T = 'CONST_TYPE'  # costante
TT_FUNC_T = 'FUNC_TYPE'  # func
TT_VOID_T = 'VOID_TYPE'  # vuoto

# ARITHMETIC OPERATORS
TT_PLUS = 'PLUS'  # +
TT_MINUS = 'MINUS'  # -
TT_MUL = 'MUL'  # *
TT_DIV = 'DIV'  # /
TT_MOD = 'MOD'  # %

# COMPARISON OPERATORS (relop)
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

# IDENTIFIER
TT_ID = 'ID'

# ASSIGNMENT
TT_ASN = 'ASN'  # :=

# RESERVED WORDS
TT_IF = 'IF'  # se
TT_ELSE = 'ELSE'  # altro
TT_RET = 'RET'  # return
TT_INIT = 'INIT'  # inizio
TT_WHILE = 'WHILE'  # mentre


reservedWords = {
    "se": TT_IF,
    "altro": TT_ELSE,
    "mentre": TT_WHILE,
    "costante": TT_CONST,
    "ind": TT_ADDR_T,
    "int": TT_INT_T,
    "car": TT_CHAR_T,
    "vuoto": TT_VOID_T,
    "vettore": TT_VEC_T,
    "func": TT_FUNC_T,
    "non": TT_NOT,
    "e": TT_AND,
    "o": TT_OR,
    "inizio": TT_INIT,
    "return": TT_RET,
}

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
TT_COL = 'COL'  # :

class Token:
    def __init__(self, _type, value=None, pos=None):
        self.type = _type
        self.value = value
        self.pos = pos

    def __repr__(self):
        line = self.pos.ln + 1
        if self.value:
            return f'[Line {line}] token {self.type}: {self.value}'
        return f'[Line {line}] token {self.type}'

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
            if self.current_char in DELIM:
                self.getChar()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in ALPHABET + '_':
                tokens.append(self.make_word())
            elif self.current_char in ARITHMETIC_OPERATORS:
                tokens.append(self.make_arithmetic_op())
                self.getChar()
            elif self.current_char in RELOP:
                tokens.append(self.make_relop())
            elif self.current_char in PUNCTUATION:
                tokens.append(self.make_punctuation())
                self.getChar()
            elif self.current_char == '\'':
                pos_start = self.pos.copy()
                char = self.current_char
                try:
                    tokens.append(self.make_char())
                except Exception as e:
                    return [], IllegalCharError(pos_start, self.pos, "'" + str(e)[-1] + "'")
            elif self.current_char == '\"':
                pos_start = self.pos.copy()
                char = self.current_char
                try:
                    tokens.append(self.make_string())
                except Exception as e:
                    return [], IllegalCharError(pos_start, self.pos, "'" + str(e)[-1] + "'")
            elif self.current_char == '#':
                tokens.append(self.make_comment())
            elif self.current_char == ':':
                tokens.append(self.make_assign())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.getChar()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    # Construct number
    def make_number(self):
        pos_start = self.pos.copy()
        num_str = ''
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.getChar()

        return Token(TT_INT, int(num_str), pos_start)

    # Construct word
    def make_word(self):
        pos_start = self.pos.copy()
        word = ''
        while self.current_char != None and re.match("[_a-zA-Z0-9]", self.current_char):
            word += self.current_char
            self.getChar()

        # Check if word exists in the map of reserved words
        if word in reservedWords.keys():
            return Token(reservedWords[word], word, pos_start)

        # Check if word is a valid identifier
        if(re.match("[_a-zA-Z]([_a-zA-Z0-9])*", word)):
            return Token(TT_ID, word, pos_start)

    # Arithmetic Operators
    def make_arithmetic_op(self):
        pos_start = self.pos.copy()
        if self.current_char == '+':
            return Token(TT_PLUS, self.current_char, pos_start)
        elif self.current_char == '-':
            return Token(TT_MINUS, self.current_char, pos_start)
        elif self.current_char == '*':
            return Token(TT_MUL, self.current_char, pos_start)
        elif self.current_char == '/':
            return Token(TT_DIV, self.current_char, pos_start)
        else:
            return Token(TT_MOD, self.current_char, pos_start)

    # Relational Operators
    def make_relop(self):
        pos_start = self.pos.copy()
        if self.current_char == '=':
            self.getChar()
            return Token(TT_EQ, '=', pos_start)
        elif self.current_char == '<':
            self.getChar()
            if self.current_char == '=':
                self.getChar()
                return Token(TT_LTEQ, '<=', pos_start)
            else:
                return Token(TT_LT, '<', pos_start)
        else:
            self.getChar()
            if self.current_char == '=':
                self.getChar()
                return Token(TT_GTEQ, '>=', pos_start)
            else:
                return Token(TT_GT, '>', pos_start)

    # Punctuation
    def make_punctuation(self):
        pos_start = self.pos.copy()
        if self.current_char == '(':
            return Token(TT_LPAREN, self.current_char, pos_start)
        elif self.current_char == ')':
            return Token(TT_RPAREN, self.current_char, pos_start)
        elif self.current_char == '{':
            return Token(TT_LCBRAC, self.current_char, pos_start)
        elif self.current_char == '}':
            return Token(TT_RCBRAC, self.current_char, pos_start)
        elif self.current_char == '[':
            return Token(TT_LSBRAC, self.current_char, pos_start)
        elif self.current_char == ']':
            return Token(TT_RSBRAC, self.current_char, pos_start)
        elif self.current_char == ',':
            return Token(TT_COMMA, self.current_char, pos_start)
        elif self.current_char == '.':
            return Token(TT_END, self.current_char, pos_start)

    # Assignment
    def make_assign(self):
        pos_start = self.pos.copy()
        self.getChar()
        if(self.current_char == '='):
            self.getChar()
            return Token(TT_ASN, ':=', pos_start)
        else:
            return Token(TT_COL, ':', pos_start)

    # Construct character
    def make_char(self):
        pos_start = self.pos.copy()
        char = '\''
        self.getChar()
        if self.current_char != None:
            char += self.current_char
            # If empty character
            if self.current_char == '\'':
                self.getChar()
                return Token(TT_CHAR, char, pos=pos_start)
            else:
                self.getChar()
                char += self.current_char
                if self.current_char == '\'':
                    self.getChar()
                    return Token(TT_CHAR, char, pos=pos_start)
                else:
                    raise Exception(char)

    # Vector char (string)
    def make_string(self):
        pos_start = self.pos.copy()
        string = '\"'
        self.getChar()
        while self.current_char != None and self.current_char != '\"':
            string += self.current_char
            self.getChar()
        if self.current_char == '\"':
            string += self.current_char
            self.getChar()
            return Token(TT_VEC_CHAR, string, pos_start)
        else:
            raise Exception(string)

    def make_comment(self):
        pos_start = self.pos.copy()
        comment = ''
        while self.current_char != None and self.current_char != '\n':
            comment += self.current_char
            self.getChar()
        return Token(TT_COMMENT, comment, pos=pos_start)
#######################################
# RUN
#######################################


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
