import re
from collections import defaultdict
from ply.lex import lex


class PascalLexer(object):

    _keywords = {
        "program": r"program",
        "var": r"var",
        "begin": r"begin",
        "end": r"end",
        "for": r"for",
        "while": r"while",
        "if": r"if",
        "then": r"then",
        "else": r"else",
        "do": r"do",
        "to": r"to",
        "downto": r"downto",
        "logical_and": r"and",
        "logical_or": r"or",
        "logical_xor": r"xor",
        "logical_not": r"not",
        "integer_type": r"integer",
        "real_type": r"real",
        "extended_type": r"extended",
        "string_type": r"string",
        "array_type": r"array",
        "function": r"function",
        "divide": r"div",
        "module": r"mod",
    }

    _numbers = {
        "float_number": r"\d*[\.]\d+",
        "integer_number": r"\d+",
    }

    _operators = {
        "equal": r"=",
        "add": r"\+",
        "subtract": r"\-",
        "multiply": r"\*",
        "greater": ">",
        "lower": "<",
        "greater_or_equal": ">=",
        "lower_or_equal": "<=",
        "assign": "\:\=",
    }

    _lexical_marks = {
        "semicolon": r";",
        "colon": r"\:",
        "dot": r"\.",
        "comma": r",",
        "open_parenthesis": r"\(",
        "close_parenthesis": r"\)",
        "open_bracket": r"\[",
        "close_bracket": r"\]",
        "open_brace": r"\{",
        "close_brace": r"\}",
        "double_quote": r"\"",
    }


    @property
    def token_patterns(self):
        patterns = {}
        patterns.update(self._operators)
        patterns.update(self._lexical_marks)
        return patterns

    @property
    def tokens(self):
        types = ["identifier", "string"]
        types.extend([name for name, pattern in self._keywords.iteritems()])
        types.extend([name for name, pattern in self._numbers.iteritems()])
        types.extend([name for name, pattern in self._lexical_marks.iteritems()])
        types.extend([name for name, pattern in self._operators.iteritems()])
        return types

    @staticmethod
    def token_error_handler(token):
        print "Illegal character {} in line {}".format(token.value[0], token.lineno)
        token.lexer.skip(1)

    @staticmethod
    def new_line_handler(token):
        """[\n]+"""
        token.lexer.lineno += len(token.value)

    @staticmethod
    def string_handler(token):
        """\'[^\'\']*\'"""
        token.type = "string"
        return token

    @staticmethod
    def identifier_handler(token):
        """[a-z_]\w*"""
        token.type = "identifier"
        for token_type, pattern in PascalLexer._keywords.iteritems():
            if re.match(pattern, token.value):
                token.type = token_type
        return token

    @staticmethod
    def number_handler(token):
        """\d*[\.]?\d+"""
        for token_type, pattern in PascalLexer._numbers.iteritems():
            if re.match(pattern, token.value):
                token.type = token_type
        return token

    def __init__(self):
        attrs = {'t_' + name: pattern for name, pattern in self.token_patterns.iteritems()}
        tokens_namespace = type("Tokens", (object, ), attrs)()
        tokens_namespace.tokens = self.tokens
        tokens_namespace.t_ignore = r" "
        tokens_namespace.t_newline = PascalLexer.new_line_handler
        tokens_namespace.t_string = PascalLexer.string_handler
        tokens_namespace.t_identifier = PascalLexer.identifier_handler
        tokens_namespace.t_number = PascalLexer.number_handler
        tokens_namespace.t_error = PascalLexer.token_error_handler
        self.lexer = lex(object=tokens_namespace)
        self.tokens_table = defaultdict(list)

    def parse_tokens(self, code):
        self.lexer.input(code)
        token = self.lexer.token()
        while token:
            self.tokens_table[token.value].append(token)
            token = self.lexer.token()

    def prettify_tokens_table(self):
        format_template = "| {:<10}| {:<15}| {:<20}| {:<10}|\n"
        delimiter = "+" + "-" * 62 + "+" + "\n"
        tokens_table = delimiter
        tokens_table += format_template.format("No", "Token:", "Type:", "Count:")
        tokens_table += delimiter
        for index, (token_value, tokens) in enumerate(self.tokens_table.iteritems()):
            tokens_table += format_template.format(index, token_value, tokens[0].type, len(tokens))
        tokens_table += delimiter
        return tokens_table


if __name__ == '__main__':
    with open("tests/code.pas", "r") as code:
        pascal_lexer = PascalLexer()
        pascal_lexer.parse_tokens(code.read())
        print pascal_lexer.prettify_tokens_table()
