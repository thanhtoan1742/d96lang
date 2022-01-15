grammar D96;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STR:
        raise UncloseString(result.text)
    if tk == self.ILLEGAL_ESC_STR_LIT:
        raise IllegalEscape(result.text)
    if tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    if tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    return result
}

options {
	language = Python3;
}

program: exp EOF;

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

EQUAL: '=';
COLON: ':';
SEMI: ';';
COMMA: ',';
LB: '{';
RB: '}';
LP: '(';
RP: ')';
COMMENT_DELIM: '##';

CLASS: 'Class';
VAL: 'Val';
VAR: 'Var';

BREAK: 'Break';
CONTINUE: 'Continue';
IF: 'If';
ELIF: 'Elseif';
ELSE: 'Else';
FOREACH: 'Foreach';

ARR: 'Array';
INT: 'Int';
FLOAT: 'Float';
BOOL: 'Boolean';
STR: 'String';

BOOLEAN_LITERAL: 'True' | 'False';

NULL: 'Null';

fragment DEC_INT: [1-9] [0-9_]* [0-9];
fragment OCT_INT: '0' [0-9_]* [0-9];
fragment HEX_INT: '0' [xX] [0-9a-fA-F_]+ [0-9a-fA-F];
fragment BIN_INT: '0' [bB] [01_]* [01];
INT_LIT
    : DEC_INT
    | OCT_INT
    | HEX_INT
    | BIN_INT
    {self.text = self.text.replace('_', '')}
    ;

fragment FLOAT_INT_PART: INT_LIT;
fragment FLOAT_DEC_PART: '.' FLOAT_INT_PART?;
fragment FLOAT_EXP_PART: [eE] [+-]? FLOAT_INT_PART;
FLOAT_LIT
    : FLOAT_INT_PART FLOAT_DEC_PART FLOAT_EXP_PART
	| FLOAT_INT_PART FLOAT_DEC_PART
	| FLOAT_INT_PART FLOAT_EXP_PART
	| FLOAT_DEC_PART FLOAT_EXP_PART
    {self.text = self.text.replace('_', '')}
    ;

fragment NOT_ESC_SEQ: ~[\b\f\n\r\t\\];
fragment ESC_SEQ: '\\' [bfnrt'\\] | '\'"';
fragment ILLEGAL_ESC_SEQ: '\\' ~[bfnrt'\\] | '\'' ~["];
ILLEGAL_ESC_STR_LIT
    : '"' (ESC_SEQ | NOT_ESC_SEQ)* ILLEGAL_ESC_SEQ
    {self.text = self.text[1:]}
    ;
UNCLOSE_STR
    : '"' (ESC_SEQ | NOT_ESC_SEQ)*
    {self.text = self.text.strip()[1:]}
    ;
STR_LIT
    : '"' (ESC_SEQ | NOT_ESC_SEQ)* '"'
    {self.text = self.text[1:-1]}
    ;

// STATIC_MODIFIER: '$'; can attribute identifier = method identifier?
ID: '$'? [a-zA-Z_] ([a-zA-Z_] | [0-9])*;

// 3.1 '\n' is used as newline character by compiler.
WS: [ \t\r\n\b\f]+ -> skip; // skip spaces, tabs, newlines

ERROR_CHAR: .;
UNTERMINATED_COMMENT: .;
