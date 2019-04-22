from ply import yacc
from pascal_lexer import PascalLexer


class SyntaxNode(object):

    def __init__(self, type, value, children):
        self.children = children
        self.type = type
        self.value = value

    def __str__(self):
        if self.value is not None:
            return "{}: {}".format(self.type, self.value)
        else:
            return "{}: ".format(self.type)

    def __repr__(self):
        if self.value is not None:
            return "{}: {}".format(self.type, self.value)
        else:
            return "{}: ".format(self.type)

    def prettify(self, indent=0):
        tree = " " * indent + str(self) + "\n"
        for child in self.children:
            if isinstance(child, SyntaxNode):
                tree += child.prettify(indent + 6)
            else:
                tree += " " * (indent + 6) + str(child) + '\n'
        return tree


class PascalParser(PascalLexer):

    pascal_functions = {
        "writeln": {"type": "function", "parameters": ["string"]},
        "write": {"type": "function", "parameters": ["string"]},
        "readln": {"type": "function", "parameters": []},
        "read": {"type": "function", "parameters": []},
    }

    def __init__(self):
        super(PascalParser, self).__init__()
        self.syntax_errors = []
        self.semantic_errors = []
        self.identifiers = self.pascal_functions.copy()

    def p_error(self, p):
        self.syntax_errors.append(p)

    def p_pascal_program(self, p):
        """
        pascal_program : program_declaration declarations program_body
        """
        p[0] = SyntaxNode("pascal_program", None, p[1:])

    def p_program_declaration(self, p):
        """
        program_declaration : program identifier semicolon
                            |
        """
        p[0] = SyntaxNode("program_declaration", None, [])
        if len(p) == 4:
            p[2] = SyntaxNode("identifier", p[2], [])
            p[0].children.append(p[2])

    def p_declarations(self, p):
        """
        declarations : variable_declarations function_declarations
                     | variable_declarations
                     | function_declarations
                     |
        """
        p[0] = SyntaxNode("declarations", None, p[1:])

    def p_function_declarations(self, p):
        """
        function_declarations : function_declarations function_declaration
                              | function_declaration
        """
        if len(p) == 2:
            p[0] = SyntaxNode("function_declarations", None, [p[1]])
        else:
            p[1].children.append(p[2])
            p[0] = p[1]

    def p_function_declaration(self, p):
        """
        function_signature : function identifier open_parenthesis\
                             parameters_declaration close_parenthesis\
                             colon variable_type semicolon

        function_declaration : function_signature declarations block semicolon
        """
        if len(p) == 9:
            parameters = [param.children[0].value for param in p[4].children]
            self.identifiers[p[2]] = {"type": "function", "parameters": parameters}
            p[2] = SyntaxNode("name", p[2], [])
            p[0] = SyntaxNode("function_signature", None, [p[2], p[4], p[7]])
        else:
            p[0] = SyntaxNode("function_declaration", None, [p[1], p[2]])

    def p_variable_declarations(self, p):
        """
        variable_declarations : variable_declarations variable_declaration semicolon
                              | var variable_declaration semicolon
        """
        if p[1] == "var":
            p[0] = SyntaxNode("variable_declarations", None, [p[2]])
        else:
            p[1].children.append(p[2])
            p[0] = p[1]

    def p_parameters_declaration(self, p):
        """
        parameters_declaration : parameters_declaration semicolon variable_declaration
                               | variable_declaration
                               |
        """
        if len(p) == 1:
            p[0] = SyntaxNode("parameters_declarations", None, [])
        elif len(p) == 2:
            p[0] = SyntaxNode("parameters_declarations", None, [p[1]])
        elif len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]

    def p_variable_declaration(self, p):
        """
        variable_type : integer_type
                      | real_type
                      | extended_type
                      | string_type

        variable_declaration : identifier colon variable_type
        """
        if len(p) == 2:
            p[0] = SyntaxNode("type", p[1], [])
        else:
            if p[1] not in self.identifiers:
                self.identifiers[p[1]] = {"type": p[3].value}
            p[1] = SyntaxNode("name", p[1], [])
            p[0] = SyntaxNode("variable_declaration", None, [p[1], p[3]])

    def p_program_body(self, p):
        """
        program_body : begin statements_block end dot
        """
        p[0] = SyntaxNode("program_body", None, [p[2]])

    def p_statements_block(self, p):
        """
        statements_block : statements_block semicolon statement
                         | statements_block semicolon
                         | block
                         | statement
                         |
        """
        if len(p) == 1:
            p[0] = SyntaxNode("statements_block", None, ["empty"])
        if len(p) == 2:
            p[0] = SyntaxNode("statements_block", None, [p[1]])
        elif len(p) == 3:
            p[0] = p[1]
        elif len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]

    def p_block(self, p):
        """
        block : begin statements_block end
              | statement
        """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_statement(self, p):
        """
        statement : condition
                  | loop_with_parameter
                  | loop_with_condition
                  | function_call
                  | assignment
        """
        p[0] = p[1]

    def p_loop_with_parameter(self, p):
        """
        loop_with_parameter : for assignment to expression do block
                            | for assignment downto expression do block
        """
        p[1] = SyntaxNode("for", None, [p[2]])
        p[3] = SyntaxNode(p[3], None, [p[4]])
        p[5] = SyntaxNode("do", None, [p[6]])
        p[0] = SyntaxNode("loop_with_parameter", None, [p[1], p[3], p[5]])

    def p_loop_with_condition(self, p):
        """
        loop_with_condition : while expression do block
        """
        p[1] = SyntaxNode("while", None, [p[2]])
        p[3] = SyntaxNode("do", None, [p[4]])
        p[0] = SyntaxNode("loop_with_condition", None, [p[1], p[3]])

    def p_condition(self, p):
        """
        condition : if expression then block else block
                  | if expression then block
        """
        p[1] = SyntaxNode("if", None, [p[2]])
        p[3] = SyntaxNode("then", None, [p[4]])
        p[0] = SyntaxNode("condition", None, [p[1], p[3]])
        if len(p) == 7:
            p[5] = SyntaxNode("else", None, [p[6]])
            p[0].children.append(p[5])

    def p_assignment(self, p):
        """
        assignment : identifier assign expression
                   | identifier assign unary_expression
                   | identifier assign operand
        """
        if p[1] not in self.identifiers:
            error_format = "Error in line {}: Identifier '{}' is not declared"
            self.semantic_errors.append(error_format.format(p.slice[1].lineno, p[1]))
        p[1] = SyntaxNode("variable", p[1], [])
        p[0] = SyntaxNode("assignment", None, [p[1], p[3]])


    def p_expression(self, p):
        """
        expression : open_parenthesis expression close_parenthesis
                   | expression operator expression
                   | expression operator function_call
                   | expression operator operand
                   | function_call
                   | operand
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4 and p[1] == "(" and p[3] == ")":
            p[0] = p[2]
        else:
            p[0] = SyntaxNode("expression", None, [p[1], p[2], p[3]])

    def p_unary_expression(self, p):
        """
        unary_expression : logical_not operand
                         | subtract operand
                         | add operand
        """
        p[1] = SyntaxNode("operator", p[1], [])
        p[0] = SyntaxNode("unary_expression", None, [p[1], p[2]])

    def p_function_call(self, p):
        """
        function_call : identifier open_parenthesis parameters close_parenthesis
        """
        if p[1] not in self.identifiers:
            error_format = "Error in line {}: Identifier '{}' is not declared"
            self.semantic_errors.append(error_format.format(p.slice[1].lineno, p[1]))
        elif self.identifiers[p[1]]["type"] != "function":
            error_format = "Error in line {}: Identifier '{}' is not a function"
            self.semantic_errors.append(error_format.format(p.slice[1].lineno, p[1]))
        elif len(p[3]) != len(self.identifiers[p[1]]["parameters"]):
            error_format = "Error in line {}: Wrong number of parameters for function '{}'"
            self.semantic_errors.append(error_format.format(p.slice[1].lineno, p[1]))
        p[0] = SyntaxNode("function_call", p[1], p[3])

    def p_function_parameters(self, p):
        """
        parameters : parameters comma expression
                   | expression
                   |
        """
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]

    def p_operator(self, p):
        """
        operator : multiply
                 | divide
                 | subtract
                 | add
                 | greater
                 | lower
                 | greater_or_equal
                 | lower_or_equal
                 | logical_or
                 | logical_and
                 | logical_xor
                 | equal
                 | module
        """
        p[0] = SyntaxNode('operator', p[1], [])

    def p_operand(self, p):
        """
        operand : float_number
                | integer_number
                | string
                | identifier
        """
        p[0] = SyntaxNode(p.slice[1].type, p[1], [])
        if p.slice[1].type == "identifier" and p[1] not in self.identifiers:
            error_format = "Error in line {}: Identifier '{}' is not declared"
            self.semantic_errors.append(error_format.format(p.slice[1].lineno, p[1]))

    def syntax_check(self, code):
        parser = yacc.yacc(module=self, check_recursion=False)
        syntax_tree = parser.parse(code)
        if self.syntax_errors or self.semantic_errors:
            raise RuntimeError()
        else:
            return syntax_tree.prettify()


if __name__ == '__main__':
    with open("tests/code.pas", "r") as code:
        pascal_parser = PascalParser()
        try:
            print pascal_parser.syntax_check(code.read())
        except RuntimeError as e:
            for error in pascal_parser.syntax_errors:
                print "Unexpected token '{}' in line {}".format(error.value, error.lineno)
            for error in pascal_parser.semantic_errors:
                print error
