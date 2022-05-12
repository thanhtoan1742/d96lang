from copy import deepcopy
from abc import ABC
from typing import List
from functools import reduce


import AST
from Visitor import *
import StaticError as SE

"""
what happens when a method returns multiple time and the return types are diffrent?
-> TypeMismatchError
what happens when a method is a recursive loop with no end point?
-> No rescursive
Use self in static method?
-> IllegalMemberAccess
Inheritance?
-> No inheritance


Class A {
    Val $s: Int = 10;
}

Class Program {
    main() {
        Val x: Int;
        Var A: A = new A();
        x = A::$A;
        x = A.$s.
    }
}

notId Id
Id Id ->
Id $Id -> static
notId $Id // never, illegal
"""

class Symbol(ABC):
    """
    Symbol:
        kind: SE.Kind
        name: str

    ClassSymbol(Symbol):
        parent: str

    ValueSymbol(Symbol):
        is_constant: bool
        mtype: AST.Type
    VariableSymbol(ValueSymbol):
    ConstantSymbol(ValueSymbol):
    ParameterSymbol(ValueSymbol):

    ClassMemberSymbol(Symbol):
        class_name: str
        is_static: bool
    MethodSymbol(ClassMemberSymbol):
        param_types: [AST.Type]
        ret_type: AST.Type

    AttributeSymbol(ClassMemberSymbol, ValueSymbol):
    """
    kind: SE.Kind

    def __init__(self, name: str) -> None:
        self.name = name


class ClassSymbol(Symbol):
    """
    Object class is the root of all class.
    """
    kind = SE.Class()

    def __init__(self, name: str, parent: str = 'Object') -> None:
        super().__init__(name)
        self.parent = parent


class ValueSymbol(Symbol):
    def __init__(self, name: str, is_constant: bool, mtype: AST.Type) -> None:
        super().__init__(name)
        self.is_constant = is_constant
        self.mtype = mtype

class VariableSymbol(ValueSymbol):
    kind = SE.Variable()

class ConstantSymbol(ValueSymbol):
    kind = SE.Constant()

class ParameterSymbol(ValueSymbol):
    kind = SE.Parameter()



class ClassMemberSymbol(Symbol):
    def __init__(self, name: str, class_name: str, is_static: bool) -> None:
        super().__init__(name)
        self.class_name = class_name
        self.is_static = is_static

class MethodSymbol(ClassMemberSymbol):
    kind = SE.Method()

    def __init__(
        self,
        name: str,
        class_name: str,
        is_static: bool,
        is_constant: bool,
        param_types: list[AST.Type],
        ret_type: AST.Type = None
    ) -> None:
        super().__init__(name, class_name, is_static)
        self.is_constant = is_constant
        self.param_types = param_types
        self.ret_type = ret_type


class AttributeSymbol(ClassMemberSymbol, ValueSymbol):
    kind = SE.Attribute()

    def __init__(self, name: str, class_name:str , is_static: bool, is_constant: bool, mtype: AST.Type) -> None:
        ClassMemberSymbol.__init__(self, class_name, is_static)
        ValueSymbol.__init__(self, name, is_constant, mtype)



class SymbolPool:
    """
    Classes go to class pool.
    Attributes got to attribute pool.
    Method go to method pool.
    Variable, constant, parameter go to scope pool.
    """

    def __init__(self) -> None:
        self.scope = 0
        self.scope_pools = {}
        self.scope_pools[self.scope] = {}

        self.class_pool = {}
        self.method_pool = {}
        self.attribute_pool = {}

    def inc_scope(self) -> None:
        self.scope += 1
        self.scope_pools[self.scope] = {}

    def dec_scope(self) -> None:
        self.scope_pools.pop(self.scope)
        self.scope -= 1

    def is_declared(self, sym: Symbol) -> bool:
        """
        Check if a symbol is declared.
        """
        if isinstance(sym, ClassSymbol):
            return sym.name in self.class_pool
        elif isinstance(sym, MethodSymbol):
            return sym.name in self.method_pool[sym.class_name]
        elif isinstance(sym, AttributeSymbol):
            return sym.name in self.attribute_pool[sym.class_name]
        else:
            return sym.name in self.scope_pools[self.scope]

    def add_symbol(self, sym: Symbol) -> None:
        """
        Add symbol to their coresponding pool.
        raise Redeclared if symbol is declared.
        """
        if self.is_declared(sym):
            raise SE.Redeclared(sym.kind, sym.name)

        if isinstance(sym, ClassSymbol):
            self.class_pool[sym.name] = sym
        elif isinstance(sym, MethodSymbol):
            self.method_pool[sym.class_name][sym.name] = sym
        elif isinstance(sym, AttributeSymbol):
            self.attribute_pool[sym.class_name][sym.name] = sym
        else:
            self.scope_pools[self.scope][sym.name] = sym

    def update_method(self, sym: MethodSymbol) -> None:
        """
        Update method return type (overwrite, no check).
        Update if method is still constant (is_constant &= sym.is_constant).
        """
        method: MethodSymbol = self.get_symbol(sym)
        assert method, \
            f'method "{sym.class_name}.{sym.name}"not found when try to update method'

        method.ret_type = sym.ret_type
        if not sym.is_constant:
            method.is_constant = False
        self.method_pool[method.class_name][method.name] = method

    def get_symbol(self, name: str, kind: SE.Kind, class_name: str = None) -> Symbol:
        """
        Lookup symbol, class_name is required if kind is Method or Attribute.
        If symbol is not found, return None.
        """
        if isinstance(kind, SE.Class):
            return self.class_pool.get(name, None)
        elif isinstance(kind, SE.Method):
            assert class_name != None
            return self.method_pool[class_name].get(name, None)
        elif isinstance(kind, SE.Attribute):
            assert class_name != None
            return self.attribute_pool[class_name].get(name, None)
        else:
            for s in range(self.scope, -1, -1):
                if name in self.scope_pools[s]:
                    return self.scope_pools[s][name]
            return None



class Context:
    """
    Tell if:
    - We are in a class?
    - We are in a method?
    - We are in a for loop?
    - We are in a while loop?
    """

    def __init__(self) -> None:
        self.in_loop = False
        self.class_name = None
        self.method_name = None

    def enter_class(self, class_name: str) -> None:
        self.class_name = class_name

    def exit_class(self) -> None:
        self.class_name = None

    def enter_method(self, method_name: str) -> None:
        self.method_name = method_name

    def exit_method(self) -> None:
        self.method_name = None

    def enter_loop(self) -> None:
        self.in_loop = True

    def exit_loop(self) -> None:
        self.in_loop = False


def clone_ast(ast: AST.AST) -> AST.AST:
    "deep copy the ast"
    return ast


def coercible(t1: AST.Type, t2: AST.Type) -> bool:
    """
    Return true if t1 can be coerced to t2.

    Array has to be exactly the same.
    IntType can be coerced into  FloatType.
    ClassType check for name.
    """
    if type(t1) == AST.ArrayType and type(t2) == AST.ArrayType:
        return t1.size == t2.size and coercible(t1.eleType, t2.eleType)
    if type(t1) == AST.IntType and type(t2) == AST.FloatType:
        return True
    if type(t1) == AST.ClassType and type(t2) == AST.ClassType:
        return t1.classname == None or t1.classname.name == t2.classname.name
    if type(t1) == type(t2):
        return True
    return False

def general(t1: AST.Type, t2: AST.Type) -> AST.Type:
    """
    Return the more general type.
    Return None if t1 can not be coerced into t2 and
    t2 can not be coerced into t1.
    Return t1 if t1 and t2 can be coerced into each other.
    """
    c1 = coercible(t2, t1)
    c2 = coercible(t1, t2)
    if not c1 and not c2:
        return None
    if not c1 and c2:
        return t2
    return t1


# The static checker should starting checking at AST.Program, otherwise
# it will produce undefined behavior.
class StaticChecker(BaseVisitor):
    """
    Check shit at compile time.

    General rules:
    - Id returns a str (maybe change in the future).
    - Expression returns a ValueSymbol (may be without name).
    - Declaration returns a ValueSymbol (with name).
    - Statement returns None.

    All class types in AST (AST.ClassType) is inherited from
    class Object.
    int, float, bool, string, array are not class type.

    Type checking should be done with coercible function.
    Getting a SymbolValue from Expr should be done with visit_expr.
    Assert everywhere for safety.
    """
    def __init__(self, ast: AST.AST) -> None:
        self.ast = clone_ast(ast)

    def check(self):
        return self.visit(self.ast, {})

    def visit_expr(self, ast: AST.Expr, visit_param: dict) -> ValueSymbol:
        """
        Return a value symbol.
        If ast is an Id, lookup from scope pool, raise Undeclared(Id) if not found.
        """
        e = self.visit(ast, visit_param)
        if isinstance(ast, AST.Id):
            sym = self.pool.get_symbol(e, SE.Variable())
            if not sym:
                raise SE.Undeclared(SE.Identifier(), e)
            return sym
        return e

    def check_assign_args_to_param(self, args: List[AST.Expr], param_types: List[AST.Type], visit_param: dict) -> bool:
        """
        Check type of args and param.
        Return true if args can be assigned to params, return false otherwise.
        """
        if len(args) != len(param_types):
            return False
        for arg, pt in zip(args, param_types):
            sym: ValueSymbol = self.visit_expr(arg, visit_param)
            if not coercible(sym.mtype, pt):
                return False
        return True

    def visit_class_member(self, ast: AST.CallExpr | AST.CallStmt | AST.FieldAccess, visit_param: dict) -> MethodSymbol | AttributeSymbol:
        """
        Try to get a MethodSymbol for CallExpr, CallStmt.
        Try to get a AttributeSymbol for FieldAccess.

        If accessing/calling an instance attribute/method using static syntax
        or accessing/calling a static attribute/method using instance syntax,
        raise IllegalMemberAccess.

        If method or attribute not found, raise Undeclared.
        """
        if type(ast) == AST.FieldAccess:
            name: str = self.visit(ast.fieldname)
            kind = SE.Attribute()
        else:
            name: str = self.visit(ast.method)
            kind = SE.Method()
        if type(ast) == AST.CallStmt:
            exception = SE.TypeMismatchInStatement(ast)
        else:
            exception = SE.TypeMismatchInExpression(ast)


        has_class = False
        has_instance = False
        if type(ast.obj) == AST.Id:
            csn = self.visit(ast.obj, visit_param)
            has_class = self.pool.get_symbol(csn, SE.Class()) != None
            sym: ValueSymbol = self.pool.get_symbol(csn, SE.Variable())
            has_instance = sym and type(sym.mtype) == AST.ClassType
        else:
            sym: ValueSymbol = self.visit_expr(ast.obj, visit_param)
            has_instance = sym and type(sym.mtype) == AST.ClassType

        if name.startswith('$'):
            if has_class:
                class_name = csn
            elif has_instance:
                raise SE.IllegalMemberAccess(ast)
            else:
                raise exception
        else:
            if has_instance:
                class_name = sym.mtype.classname.name
            elif has_class:
                raise SE.IllegalMemberAccess(ast)
            else:
                raise exception

        sym = self.pool.get_symbol(name, kind, class_name)
        if not sym:
            raise SE.Undeclared(kind, name)
        return sym




    def visitIntLiteral(self, ast: AST.IntLiteral, visit_param: dict) -> ValueSymbol:
        return ValueSymbol(None, True, AST.IntType())

    def visitFloatLiteral(self, ast: AST.FloatLiteral, visit_param: dict) -> ValueSymbol:
        return ValueSymbol(None, True, AST.FloatType())

    def visitStringLiteral(self, ast: AST.StringLiteral, visit_param: dict) -> ValueSymbol:
        return ValueSymbol(None, True, AST.StringType())

    def visitBooleanLiteral(self, ast: AST.BooleanLiteral, visit_param: dict) -> ValueSymbol:
        return ValueSymbol(None, True, AST.BoolType())

    def visitNullLiteral(self, ast: AST.NullLiteral, visit_param: dict) -> ValueSymbol:
        """
        Class type of None (special marking).
        """
        return ValueSymbol(None, True, AST.ClassType(None))

    def visitSelfLiteral(self, ast: AST.SelfLiteral, visit_param: dict) -> ValueSymbol:
        """
        Self literal has the type of current class.
        """
        return ValueSymbol(None, True, AST.ClassType(AST.Id(self.context.class_name)))

    def visitArrayLiteral(self, ast: AST.ArrayLiteral, visit_param: dict) -> ValueSymbol:
        """
        All elements in array must have the same type

        TEST: elements in array do not have the same type.
        TEST: array size = 0.
        TEST: array elements are not constant.
        """
        size = len(ast.value)
        # if not size:
        #     raise SE.IllegalArrayLiteral(ast)

        eles: List[ValueSymbol] = [self.visit_expr(e) for e in ast.value]
        ele_type = eles[0].mtype
        # type has to be the same, not coercible.
        if not reduce(lambda acc, e: acc and type(e.mtype) == type(ele_type), eles):
            raise SE.IllegalArrayLiteral(ast)
        if not reduce(lambda acc, e: acc and e.is_constant, eles):
            raise SE.IllegalConstantExpression(ast)
        mtype = AST.ArrayType(size, ele_type)
        return ValueSymbol(None, True, mtype)


    def visitId(self, ast: AST.Id, visit_param: dict) -> str:
        return ast.name



    def visitUnaryOp(self, ast: AST.UnaryOp, visit_param: dict) -> ValueSymbol:
        value: ValueSymbol = self.visit_expr(ast.body, visit_param)
        if ast.op == '-' and not type(value.mtype) in [AST.IntType, AST.FloatType]:
            raise SE.TypeMismatchInExpression(ast)
        if ast.op == '!' and type(value.mtype) != AST.BoolType:
            raise SE.TypeMismatchInExpression(ast)
        value.name = None
        return value

    def visitBinaryOp(self, ast: AST.BinaryOp, visit_param: dict) -> ValueSymbol:
        left = self.visit_expr(ast.left, visit_param)
        right = self.visit_expr(ast.right, visit_param)
        if ast.op in ['+', '-', '*', '/', '>', '<', '>=', '<=']:
            opr_type = general(left.mtype, right.mtype)
            res_type = opr_type
        elif ast.op == '%':
            opr_type = AST.IntType()
            res_type = AST.IntType()
        elif ast.op in ['==', '!=']:
            if type(left.mtype) in [AST.IntType, AST.BoolType]:
                opr_type = left.mtype
            else:
                opr_type = AST.BoolType()
            res_type = AST.BoolType()
        elif ast.op in ['&&' , '||']:
            opr_type = AST.BoolType()
            res_type = AST.BoolType()
        elif ast.op == '==.':
            opr_type = AST.StringType()
            res_type = AST.BoolType()
        elif ast.op == '+.':
            opr_type = AST.StringType()
            res_type = AST.StringType()
        else:
            assert False, 'operator not defined'
        if not coercible(left.mtype, opr_type) or not coercible(right.mtype, opr_type):
            raise SE.TypeMismatchInExpression(ast)
        return ValueSymbol(None, left.is_constant and right.is_constant, res_type)

    def visitNewExpr(self, ast: AST.NewExpr, visit_param: dict) -> ValueSymbol:
        """
        ValueSymbol from new Expr is not constant by default.

        TEST: class is not defined.
        TEST: constructor is not called correctly.
        """
        class_name: str = self.visit(ast.classname, visit_param)
        if not self.pool.get_symbol(class_name, SE.Class()):
            raise SE.Undeclared(SE.Class(), class_name)
        constructor: MethodSymbol = self.pool.get_symbol('Constructor', SE.Method(), class_name)
        assert constructor, f'Constructor not found for class {class_name}'
        if not self.check_assign_args_to_param(ast.param, constructor.param_types, visit_param):
            raise SE.TypeMismatchInExpression(ast)
        return ValueSymbol(None, False, AST.ClassType(ast.classname))

    def visitArrayCell(self, ast: AST.ArrayCell, visit_param: dict) -> ValueSymbol:
        """
        ArrayType: size and eleType
        ArrayCell: arr and indexes
        -> recursive access array type.

        TEST: arr must be array type.
        TEST: indexes must be int type.
        TEST: index out of bound. // don't check
        TEST: dimension out of bound? // don't check

        This works with 1-D array.
        """
        idxs = [self.visit_expr(e, visit_param) for e in ast.idx]
        if not reduce(lambda acc, v: acc and type(v.mtype) == AST.IntType, idxs):
            raise SE.TypeMismatchInExpression(ast)

        arr: ValueSymbol = self.visit_expr(ast.arr, visit_param)
        mtype = arr.mtype
        for _ in range(len(idxs)):
            if type(mtype) != AST.ArrayType:
                raise SE.TypeMismatchInExpression(ast)
            mtype = mtype.eleType

        is_constant = reduce(lambda acc, id: acc and id.is_constant, idxs, arr.is_constant)
        return ValueSymbol(None, is_constant, mtype)

    def visitCallExpr(self, ast: AST.CallExpr, visit_param: dict) -> ValueSymbol:
        """
        TEST: must not return void
        TEST: arg type must ok with param type
        """
        sym: MethodSymbol = self.visit_class_member(ast, visit_param)
        if type(sym.ret_type) == SE.VoidType:
            raise SE.TypeMismatchInStatement(ast)
        if not self.check_assign_args_to_param(ast.param, sym.param_types, visit_param):
            raise SE.TypeMismatchInStatement(ast)
        return ValueSymbol(None, sym.is_constant, sym.ret_type)

    def visitFieldAccess(self, ast: AST.FieldAccess, visit_param: dict) -> AttributeSymbol:
        sym: AttributeSymbol = self.visit_class_member(ast, visit_param)
        if type(sym) != AST.ClassType:
            raise SE.TypeMismatchInExpression(ast)
        return sym


    def visitVarDecl(self, ast: AST.VarDecl, visit_param: dict) -> ValueSymbol:
        name: str = self.visit(ast.variable, visit_param)
        if ast.varInit:
            value = self.visit_expr(ast.varInit, visit_param)
            if not coercible(value.mtype, ast.varType):
                raise SE.TypeMismatchInStatement(ast)

        return ValueSymbol(name, False, ast.varType)

    def visitConstDecl(self, ast: AST.ConstDecl, visit_param: dict) -> ValueSymbol:
        """
        TEST: const value type is nor coercible to const type.
        TEST: value is not constant.
        TEST: no init value.
        """
        name: str = self.visit(ast.constant, visit_param)
        if not value:
            raise SE.IllegalConstantExpression(ast.value)
        value = self.visit_expr(ast.value, visit_param)
        if not value.is_constant:
            raise SE.IllegalConstantExpression(ast.value)
        if type(ast.constType) == AST.VoidType or not coercible(value.mtype, ast.constType):
            raise SE.TypeMismatchInConstant(ast)
        return ValueSymbol(name, True, ast.constType)

    def visitAttributeDecl(self, ast: AST.AttributeDecl, visit_param: dict) -> None:
        """
        from BKeL:
        [About declaring method and attribute in the same class]
        Method and attribute can have the same name in the same class.

        TEST: A method is not count as an attribute (if we declared A.func(), we can
        not access it as A.func)
        """
        # receive symbol from ConstDecl or VarDecl
        sym: ValueSymbol = self.visit(ast.decl, visit_param)
        sym = AttributeSymbol(
            name=sym.name,
            class_name=self.context.class_name,
            is_static=isinstance(ast.kind, AST.Static),
            is_constant=sym.is_constant,
            mtype=sym.mtype
        )
        self.pool.add_symbol(sym)





    def visitAssign(self, ast: AST.Assign, visit_param: dict) -> None:
        """
        assignment in for loop: the count variable in for loop is constant,
        raise the CannotAssignToConstant with Assignment ast.

        TEST: lsh is not of type LHS.
        TEST: in for loop.
        """
        rhs: ValueSymbol = self.visit_expr(ast.rhs, visit_param)
        lhs: ValueSymbol = self.visit_expr(ast.lhs, visit_param)
        if type(lhs.mtype) == AST.VoidType or not coercible(rhs.mtype, lhs.mtype):
            raise SE.TypeMismatchInStatement(ast)
        if lhs.is_constant:
            raise SE.CannotAssignToConstant(ast)

    def visitIf(self, ast: AST.If, visit_param: dict) -> None:
        """
        TEST: check if condition can be converted into boolean.
        """
        expr: ValueSymbol = self.visit(ast.expr, visit_param)
        if not coercible(expr.mtype, AST.BoolType()):
            raise SE.TypeMismatchInStatement(ast)
        self.visit(ast.thenStmt, visit_param)
        if ast.elseStmt:
            self.visit(ast.elseStmt, visit_param)

    def visitFor(self, ast: AST.For, visit_param: dict) -> None:
        """
        TEST: type of expr1, expr2, expr3 is not int.
        """
        exprs = [ast.expr1, ast.expr2]
        if ast.expr3:
            exprs.append(ast.expr3)
        es = [self.visit_expr(e, visit_param) for e in exprs]
        if not reduce(lambda acc, e: acc and type(e.mtype) == AST.IntType, es):
            raise SE.TypeMismatchInStatement(ast)

        self.visit(AST.Assign(ast.id, ast.expr1))
        self.context.enter_loop()
        self.visit(ast.loop, visit_param)
        self.context.exit_loop()

    def visitBreak(self, ast: AST.Break, visit_param: dict) -> None:
        """
        TEST: break in loop.
        """
        if not self.context.in_loop:
            raise SE.MustInLoop(ast)

    def visitContinue(self, ast: AST.Continue, visit_param: dict) -> None:
        """
        TEST: continue in loop.
        """
        if not self.context.in_loop:
            raise SE.MustInLoop(ast)

    def visitReturn(self, ast: AST.Return, visit_param: dict) -> None:
        """
        Infer the type of method.
        In Program.main(), constructor or destructor, If return something is not
        void, raise TypeMismatchInStatement

        TEST: return not in method
        TEST: type of method has already been inferred and is
        not the current type.
        TEST: main return not void
        TEST: constructor return not void
        TEST: destructor return not void
        """
        if ast.expr:
            expr: ValueSymbol = self.visit_expr(ast.expr, visit_param)
        else:
            expr: ValueSymbol = ValueSymbol(None, True, AST.VoidType())
        sym: MethodSymbol = self.pool.get_symbol(
            self.context.method_name,
            SE.Method(),
            self.context.class_name,
        )
        assert sym, 'return is not in a method'
        if sym.ret_type and not coercible(expr.mtype, sym.ret_type):
            raise SE.TypeMismatchInStatement(ast)
        sym.ret_type = expr.mtype
        sym.is_constant = expr.is_constant
        self.pool.update_method(sym)

    def visitCallStmt(self, ast: AST.CallStmt, visit_param: dict) -> None:
        """
        Get method from self or global symbol table.
        Assign arguments to parameters using AST.Assign()

        TEST: static call on instance method.
        TEST: instance call on static method.
        TEST: return not void.
        TEST: len(params) != len(args).
        TEST: assignment of args to params.
        """
        sym: MethodSymbol = self.visit_class_member(ast, visit_param)
        if type(sym.ret_type) != SE.VoidType:
            raise SE.TypeMismatchInStatement(ast)
        if not self.check_assign_args_to_param(ast.param, sym.param_types, visit_param):
            raise SE.TypeMismatchInStatement(ast)




    def visitBlock(self, ast: AST.Block, visit_param: dict) -> None:
        param: List[AST.VarDecl] = visit_param.get('param', None)
        visit_param['param'] = None

        self.pool.inc_scope()
        if param:
            for e in param:
                sym: ValueSymbol = self.visit(e, visit_param)
                self.pool.add_symbol(ParameterSymbol(sym.name, sym.is_constant, sym.mtype))

        for e in ast.inst:
            sym = self.visit(e, visit_param)
            # if is VarDecl or ConstDecl
            if sym and isinstance(sym, ValueSymbol):
                if sym.is_constant:
                    self.pool.add_symbol(VariableSymbol(sym.name, sym.is_constant, sym.mtype))
                else:
                    self.pool.add_symbol(ConstantSymbol(sym.name, sym.is_constant, sym.mtype))
        self.pool.dec_scope()

    def visitMethodDecl(self, ast: AST.MethodDecl, visit_param: dict) -> None:
        """
        A method has to be declared before using.

        TEST: calling undeclared method.
        TEST: calling undeclared method at this point (declared later).

        from BKeL:
        [About declaring method and attribute in the same class]
        Method and attribute can have the same name in the same class.
        """
        name = self.visit(ast.name, visit_param)
        ret_type = None
        # for some special methods, return type is determined
        if self.context.class_name == 'Program' and name == 'main':
            ret_type = AST.VoidType()
        if name == 'Constructor' or name == 'Destructor':
            ret_type = AST.VoidType()
        # the method is constant by default, if in any return statement, the return
        # expression is not constant then the method is not constant.
        sym = MethodSymbol(
            name=name,
            class_name=self.context.class_name,
            is_static=isinstance(ast.kind, AST.Instance),
            is_constant=True,
            param_types=[e.varType for e in ast.param],
            ret_type=ret_type
        )
        self.pool.add_symbol(sym)

        self.context.enter_method(name)
        visit_param['param'] = ast.param
        self.visit(ast.body, visit_param)
        self.context.exit_method()



    def visitClassDecl(self, ast: AST.ClassDecl, visit_param: dict) -> None:
        """
        A class can inherit another class.
        A method or attribute look up should look into the parrent class if
        it can't find the method or attribute at the current class.

        If there is no constructor, generate empty constructor.
        If there is no destructor, generate empty destructor.

        TEST: call a method defined in parent using child class.
        TEST: parent class is not defined.
        """
        name: str = self.visit(ast.classname, visit_param)
        parent: str = self.visit(ast.parentname, visit_param)
        if not self.pool.is_declared(ClassSymbol(parent)):
            raise SE.Undeclared(SE.Class(), parent)

        sym = ClassSymbol(name, parent)
        self.pool.add_symbol(sym)

        self.context.enter_class(name)
        self.pool.inc_scope()

        for e in ast.memlist:
            self.visit(e, visit_param)

        # no constructor, generate empty
        if not self.pool.get_symbol('Constructor', SE.Method(), name):
            self.visit(AST.MethodDecl(
                AST.Instance(),
                AST.Id('Constructor'),
                [],
                AST.Block([])
            ), visit_param)
        # no destructor, generate empty
        if not self.pool.get_symbol('Destructor', SE.Method(), name):
            self.visit(AST.MethodDecl(
                AST.Instance(),
                AST.Id('Destructor'),
                [],
                AST.Block([])
            ), visit_param)

        self.pool.dec_scope()
        self.context.exit_class()

    def visitProgram(self, ast: AST.Program, visit_param: dict) -> None:
        """
        TEST: no Program class.
        TEST: no main method.
        TEST: main method is not static.
        TEST: main method accepts parameters.
        TEST: main method return something (not void).
        TEST: main method can be static or not.

        from BKeL
        [Error raised for function "main" in class Program]
        a. In case the function "main" takes no parameters, and has a return type other than void, the TypeMismatchInStatement error will be raised.
        b. In case the function "main" has parameter(s), the NoEntryPoint error will be raised.
        """
        self.pool = SymbolPool()
        self.context = Context()

        for e in ast.decl:
            self.visit(e, visit_param)

        entry_point: MethodSymbol = self.pool.get_symbol('main', SE.Method(), 'Program')
        if not entry_point or entry_point.param_types != []:
            raise SE.NoEntryPoint()

