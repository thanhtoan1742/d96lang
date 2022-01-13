grammar D96;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:
        raise UncloseString(result.text.strip()[1:])
    if tk == self.ILLEGAL_ESCAPE_STRING_LITERAL:
        raise IllegalEscape(result.text[1:])
    if tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    if tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    if tk == self.INT_LITERAL or tk == self.FLOAT_LITERAL:
        result.text = result.text.replace('_', '')
    if tk == self.STRING_LITERAL:
        result.text = result.text[1:-1]
    return result
}

options {
	language = Python3;
}

program:;

expression
    : TRUE
	| FALSE
	| NULL
	| INT_LITERAL
	| FLOAT_LITERAL
	| STRING_LITERAL
    | IDENTIFIER
    ;

EQUAL: '=';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';
CURLY_BRACKET_OPEN: '{';
CURLY_BRACKET_CLOSE: '}';
ROUND_BRACKET_OPEN: '(';
ROUND_BRACKET_CLOSE: ')';
BLOCK_COMENT_DELIMITER: '##';

CLASS: 'Class';
VAL: 'Val';
VAR: 'Var';

BREAK: 'Break';
CONTINUE: 'Continue';
IF: 'If';
ELSEIF: 'Elseif';
ELSE: 'Else';
FOREACH: 'Foreach';

ARRAY: 'Array';
INT: 'Int';
FLOAT: 'Float';
BOOLEAN: 'Boolean';
STRING: 'String';

TRUE: 'True';
FALSE: 'False';

NULL: 'Null';

fragment DEC_INTEGER: [1-9] [0-9_]* [0-9];
fragment OCT_INTEGER: '0' [0-9_]* [0-9];
fragment HEX_INTEGER: '0' [xX] [0-9a-fA-F_]+ [0-9a-fA-F];
fragment BIN_INTEGER: '0' [bB] [01_]* [01];
INT_LITERAL
    : DEC_INTEGER
	| OCT_INTEGER
	| HEX_INTEGER
	| BIN_INTEGER
    ;

fragment FLOAT_INTEGER_PART: INT_LITERAL;
fragment FLOAT_DECIMAL_PART: '.' FLOAT_INTEGER_PART?;
fragment FLOAT_EXPONENT_PART: [eE] [+-]? FLOAT_INTEGER_PART;
FLOAT_LITERAL
    : FLOAT_INTEGER_PART FLOAT_DECIMAL_PART FLOAT_EXPONENT_PART
	| FLOAT_INTEGER_PART FLOAT_DECIMAL_PART
	| FLOAT_INTEGER_PART FLOAT_EXPONENT_PART
	| FLOAT_DECIMAL_PART FLOAT_EXPONENT_PART
    ;

fragment NOT_ESCAPE_SEQUENCE: ~[\n\r\f\\];
fragment ESCAPE_SEQUENCE: '\\' [bfnrt'\\] | '\'"';
STRING_LITERAL: '"' (ESCAPE_SEQUENCE | NOT_ESCAPE_SEQUENCE)* '"';
fragment ILLEGAL_ESCAPE_SEQUENCE: '\\' ~[bfnrt'\\] | '\'' ~["];
ILLEGAL_ESCAPE_STRING_LITERAL: '"' (ESCAPE_SEQUENCE | NOT_ESCAPE_SEQUENCE)* ILLEGAL_ESCAPE_SEQUENCE;
UNCLOSE_STRING: '"' (ESCAPE_SEQUENCE | NOT_ESCAPE_SEQUENCE)*;

// STATIC_MODIFIER: '$'; can attribute identifier = method identifier?
IDENTIFIER: '$'? [a-zA-Z_] ([a-zA-Z_] | [0-9])*;

// 3.1 '\n' is used as newline character by compiler.
WS: [ \t\r\n\b\f]+ -> skip; // skip spaces, tabs, newlines

ERROR_CHAR: .;
UNTERMINATED_COMMENT: .;