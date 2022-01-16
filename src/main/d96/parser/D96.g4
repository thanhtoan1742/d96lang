grammar D96;

options {
	language = Python3;
}

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    token = super().emit()
    typ = token.type

    if typ == self.ERROR_TOKEN:
        raise ErrorToken(token.text)
    if typ == self.UNCLOSE_STRING:
        raise UncloseString(token.text.strip()[1:])
    if typ == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(token.text[1:])

    # statement tells not to do unterminated comment
    # if typ == self.UNTERMINATED_COMMENT:
    #     raise UnterminatedComment()

    if typ == self.COMMENT:
        token.text = token.text[2:-2]
    if typ == self.INT_LIT or typ == self.FLOAT_LIT:
        token.text = token.text.replace('_', '')
    if typ == self.STR_LIT:
        token.text = token.text[1:-1]
    return token
}

// PARSER
program: ;

exp
    : array
    | BOOLEAN_LITERAL
    | NULL
    | INT_LIT
    | FLOAT_LIT
    | STR_LIT
    | ID
    ;

// TODO: test this
comma_exps: (exp (COMMA exp)*)?;

array: ARR LP comma_exps RP;



// LEXER
ADD_OP: '+';
SUB_OP: '-';
MUL_OP: '*';
DIV_OP: '/';
MOD_OP: '%';
NOT_OP: '!';
AND_OP: '&&';
OR_OP: '||';
EQ_OP: '=';
EQEQ_OP: '==';
NOT_EQ_OP: '!=';
GT_OP: '>';
LT_OP: '<';
GE_OP: '>=';
LE_OP: '<=';
DOT_OP: '.';
EQEQ_DOT_OP: '==.';
ADD_DOT_OP: '+.';
COLON_COLON_OP: '::';
NEW_OP: 'new';

COLON: ':';
SEMI: ';';
COMMA: ',';
LB: '{';
RB: '}';
LP: '(';
RP: ')';
LK: '[';
RK: ']';
COMMENT_DELIM: '##';

BREAK: 'Break';
CONTINUE: 'Continue';
IF: 'If';
ELIF: 'Elseif';
ELSE: 'Else';
FOREACH: 'Foreach';
IN: 'IN';
RETURN: 'Return';
CLASS: 'Class';
VAL: 'Val';
VAR: 'Var';
CONSTRUCTOR: 'Constructor';
DESSTRUCTOR: 'Destructor';
NEW: 'New';
BY: 'By';

ARR: 'Array';
INT: 'Int';
FLOAT: 'Float';
BOOL: 'Boolean';
STR: 'String';

BOOLEAN_LITERAL: 'True' | 'False';

NULL: 'Null';

fragment COMMENT_BODY: (~'#' | '#' ~'#')*;
COMMENT: COMMENT_DELIM COMMENT_BODY COMMENT_DELIM;
UNTERMINATED_COMMENT: COMMENT_DELIM COMMENT_BODY;


fragment DEC_INT: [1-9] [0-9_]* [0-9];
fragment OCT_INT: '0' [0-9_]* [0-9];
fragment HEX_INT: '0' [xX] [0-9a-fA-F_]* [0-9a-fA-F];
fragment BIN_INT: '0' [bB] [01_]* [01];
INT_LIT: DEC_INT | OCT_INT | HEX_INT | BIN_INT;

fragment FLOAT_INT_PART: INT_LIT;
fragment FLOAT_DEC_PART: '.' FLOAT_INT_PART?;
fragment FLOAT_EXP_PART: [eE] [+-]? FLOAT_INT_PART;
FLOAT_LIT
    : FLOAT_INT_PART FLOAT_DEC_PART FLOAT_EXP_PART
    | FLOAT_INT_PART FLOAT_DEC_PART
    | FLOAT_INT_PART FLOAT_EXP_PART
    | FLOAT_DEC_PART FLOAT_EXP_PART
    ;

fragment NOT_ESC_SEQ: ~[\b\f\n\r\t\\];
fragment ESC_SEQ: '\\' [bfnrt'\\] | '\'"';
fragment ILLEGAL_ESC_SEQ: '\\' ~[bfnrt'\\] | '\'' ~["];
STR_LIT: '"' (ESC_SEQ | NOT_ESC_SEQ)* '"';
ILLEGAL_ESCAPE: '"' (ESC_SEQ | NOT_ESC_SEQ)* ILLEGAL_ESC_SEQ;
UNCLOSE_STRING: '"' (ESC_SEQ | NOT_ESC_SEQ)*;


// STATIC_MODIFIER: '$'; can attribute identifier = method identifier?
ID: '$'? [a-zA-Z_] ([a-zA-Z_] | [0-9])*;


// 3.1 '\n' is used as newline character by compiler.
WS: [ \t\r\n\b\f]+ -> skip; // skip spaces, tabs, newlines
// WS: [ \t\r\n\b\f]+;

ERROR_TOKEN: .;