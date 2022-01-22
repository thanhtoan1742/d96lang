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

    if typ == self.INT_LIT or typ == self.FLOAT_LIT:
        token.text = token.text.replace('_', '')

    if typ == self.STR_LIT:
        token.text = token.text[1:-1]
    return token
}


// PARSER
program: class_decl* EOF;

class_decl: CLASS MEMBER_ID (COLON MEMBER_ID)? LB class_mems RB;
class_mems: (method_decl | attr_decl)*;

attr_decl: mut_mod comma_member_ids COLON typ (EQ_OP comma_exps)? SEMI;
mut_mod: VAL | VAR;

method_decl: normal_method_decl | constuctor_decl | destuctor_decl;
normal_method_decl: MEMBER_ID LP semi_param_decls RP stmt_block;
constuctor_decl: CONSTRUCTOR LP semi_param_decls RP stmt_block;
destuctor_decl: DESTRUCTOR LP RP stmt_block;
semi_param_decls: (param_decl (SEMI param_decl)*)?;
param_decl: comma_member_ids COLON typ;

comma_member_ids: MEMBER_ID (COMMA MEMBER_ID)*;

// not finished
typ: INT | FLOAT | STR | BOOL;

stmt_block: LB stmt* RB;
stmt
    : var_decl_stmt
    | assign_stmt
    | if_stmt
    | for_stmt
    | break_stmt
    | continue_stmt
    | return_stmt
    | method_invoke_stmt
    ;


var_decl_stmt: mut_mod comma_var_ids COLON typ (EQ_OP comma_exps)? SEMI;
comma_var_ids: VAR_ID (COMMA VAR)*;

assign_stmt: lhs EQ_OP exp SEMI;

if_stmt: IF if_cond stmt_block (ELIF if_cond stmt_block)* (ELSE stmt_block)?;
if_cond: LP exp RP;

// VAR_ID should be a scalar variable (which couble be a MEMBER_ID)
for_stmt: FOREACH LP VAR_ID IN exp DOTDOT exp (BY exp)? RP stmt_block;

break_stmt: BREAK SEMI;
continue_stmt: CONTINUE SEMI;
return_stmt: RETURN exp? SEMI;

method_invoke_stmt: VAR_ID LP comma_exps RP;

exp returns [value]
    : array
    | BOOL_LIT
    | NULL
    | INT_LIT
    | FLOAT_LIT
    | STR_LIT
    | MEMBER_ID
    ;

// TODO: test this
comma_exps: (exp (COMMA exp)*)?;

array: ARR LP comma_exps RP;
lhs: ;



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
DOTDOT: '..';
NEW_OP: 'New';

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
DESTRUCTOR: 'Destructor';
BY: 'By';

ARR: 'Array';
INT: 'Int';
FLOAT: 'Float';
BOOL: 'Boolean';
STR: 'String';

BOOL_LIT: 'True' | 'False';

NULL: 'Null';

fragment COMMENT_BODY: (~'#' | '#' ~'#')*;
COMMENT: COMMENT_DELIM COMMENT_BODY COMMENT_DELIM;
UNTERMINATED_COMMENT: COMMENT_DELIM COMMENT_BODY;


fragment DEC_INT:            '0' | [1-9]    ('_'? [0-9]     )*   ;
fragment BIN_INT: '0' [bB]  ('0' | '1'      ('_'? [01]      )*  );
fragment OCT_INT: '0'       ('0' | [1-7]    ('_'? [0-7]     )*  );
fragment HEX_INT: '0' [xX]  ('0' | [1-9A-F] ('_'? [0-9A-F]  )*  );
INT_LIT
    : DEC_INT
    | BIN_INT
    | OCT_INT
    | HEX_INT
    ;


fragment FLOAT_INT_PART: DEC_INT;
fragment FLOAT_DEC_PART: '.' ([0-9] ('_'? [0-9])*)?;
fragment FLOAT_EXP_PART: [eE] [+-]? DEC_INT;
FLOAT_LIT
    : FLOAT_INT_PART FLOAT_DEC_PART FLOAT_EXP_PART
    | FLOAT_INT_PART FLOAT_DEC_PART
    | FLOAT_INT_PART FLOAT_EXP_PART
    | FLOAT_DEC_PART FLOAT_EXP_PART
    ;


fragment NOT_ESC_SEQ: ~[\b\f\n\r\t'\\"];
fragment ESC_SEQ: '\\' [bfnrt'\\] | '\'"';
fragment ILLEGAL_ESC_SEQ: '\\' ~[bfnrt'\\] | '\'' ~["];
STR_LIT: '"' (ESC_SEQ | NOT_ESC_SEQ)* '"';
ILLEGAL_ESCAPE: '"' (ESC_SEQ | NOT_ESC_SEQ)* ILLEGAL_ESC_SEQ;
UNCLOSE_STRING: '"' (ESC_SEQ | NOT_ESC_SEQ)*;


// STATIC_MODIFIER: '$'; can attribute identifier = method identifier?
MEMBER_ID: '$'? [a-zA-Z_] ([a-zA-Z_] | [0-9])*;
VAR_ID: [a-zA-Z_] ([a-zA-Z_] | [0-9])*;


// 3.1 '\n' is used as newline character by compiler.
WS: [ \t\r\n\b\f]+ -> skip; // skip spaces, tabs, newlines
// WS: [ \t\r\n\b\f]+;

ERROR_TOKEN: .;
