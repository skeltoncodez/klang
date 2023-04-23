from sly import Lexer, Parser


class KLexer(Lexer):
    tokens = {
        ID, IMPORT, FUNCTION,
        PRINT,
        IF, ELSE, WHILE,
        REFERENCE, VOID_TYPE, FLOAT_TYPE, INT_TYPE, BOOL_TYPE, STRING_TYPE,
        FLOAT, INT, STRING,
        TRUE, FALSE,
        PLUS, TIMES, MINUS, DIVIDE, MODULO, 
        INCREM, DECREM, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN, MODASSIGN,
        NEQ, EQ, ASSIGN, LPAREN, RPAREN, LBRACKET, RBRACKET,
        # LBRACE, RBRACE,
        COMMA, SEP
    }
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['import'] = IMPORT
    ID['funct'] = FUNCTION
    ID['print'] = PRINT  # me waiting for a way better way to do this
    ID['void'] = VOID_TYPE
    ID['ref'] = REFERENCE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['float'] = FLOAT_TYPE
    ID['int'] = INT_TYPE
    ID['string'] = STRING_TYPE
    ID['bool'] = BOOL_TYPE
    ID['true'] = TRUE
    ID['false'] = FALSE

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.', ','}

    # Special symbols
    PLUS = r'\+'
    INCREM = r'\+\+'
    DECREM = r'--'
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    MODASSIGN = r'%='
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MODULO = r'%'
    NEQ = r'!='
    EQ = r'=='
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    # LBRACE = r'\{'
    # RBRACE = r'\}'
    SEP = r';'
    COMMA = r','

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'0x[0-9a-fA-F]+', r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\"", "\"")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t

    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comments = r'\#.*'
    # Extra action for newlines

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
