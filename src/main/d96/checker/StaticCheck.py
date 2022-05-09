from copy import deepcopy
from abc import ABC
from typing import List

import AST
from Visitor import *
import StaticError as SE

"""
what happens when a method returns multiple time and the return types are diffrent?
-> TypeMismatchError
what happens when a method is a recursive loop with no end point?
"""


class MethodDeclRet(AST.MethodDecl):
    def __init__(self, retType: AST.Type = AST.VoidType(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retType = retType


class Symbol(ABC):
    """
    Symbol(name, kind):
    ClassSymbol()
    MethodSymbol(statically_evaluable, param_types, ret_type)
    ValueSymbol(is_constant, type):
        VariableSymbol()
        ConstantSymbol()
        AttributeSymbol()
        ParameterSymbol()

    store all kind of symbol: class, variable, const, method,...
    kind: StaticError's kind
    type: if kind is variable or constant, this is the type.
    If kind is function, this is an array of [return type, params' type].
    store_kind: 'val' | 'var' | None
    """

    kind: SE.Kind

    def __init__(self, name: str) -> None:
        self.name = name


class ValueSymbol(Symbol):
    def __init__(self, name: str, is_constant: bool, mtype: AST.Type) -> None:
        super().__init__(name)
        self.is_constant = is_constant
        self.mtype = mtype


class VariableSymbol(ValueSymbol):
    kind = SE.Variable()


class AttributeSymbol(ValueSymbol):
    kind = SE.Attribute()


class ParameterSymbol(ValueSymbol):
    kind = SE.Parameter()


class ConstantSymbol(ValueSymbol):
    kind = SE.Constant()


class ClassSymbol(Symbol):
    kind = SE.Class()


class MethodSymbol(Symbol):
    kind = SE.Method()

    def __init__(
        self, name: str,
        statically_evaluable: bool,
        param_types: List[AST.Type],
        ret_type: AST.Type
    ) -> None:
        super().__init__(name)
        self.statically_evaluable = statically_evaluable
        self.param_types = param_types
        self.ret_types = ret_type


class SymbolPool:
    def __init__(self) -> None:
        self.scope = 0
        self.pools = {}
        self.pools[self.scope] = {}

    def inc_scope(self):
        self.scope += 1
        self.pools[self.scope] = {}

    def dec_scope(self):
        self.pools.pop(self.scope)
        self.scope -= 1

    def is_declared_in_current_scope(self, name):
        return name in self.pools[self.scope]

    def add_symbol(self, sym: Symbol):
        self.pools[self.scope][sym.name] = sym

    def get_symbol(self, name):
        for s in range(self.scope, -1, -1):
            if name in self.pools[s]:
                return self.pools[s][name]
        return None


def clone_ast(ast):
    "deep copy the ast"
    return ast


# The static checker should starting checking at AST.Program, otherwise
# it will produce undefined behavior.
class StaticChecker(BaseVisitor):
    def __init__(self, ast: AST.AST):
        self.ast = clone_ast(ast)

    def check(self):
        return self.visit(self.ast, {})

    def visitClassDecl(self, ast: AST.ClassDecl, visit_param: dict):
        pass

    def visitProgram(self, ast: AST.Program, visit_param: dict):
        for d in ast.decl:
            self.visit(d, visit_param)

        found_entry = False
        for c in ast.decl:
            if c.classname == 'Program':
                for m in c.memlist:
                    if isinstance(m, MethodDeclRet) \
                    and m.name == 'main' \
                    and m.param == [] \
                    and m.retType == AST.VoidType():
                        found_entry = True
                        break
        if not found_entry:
            raise SE.NoEntryPoint()
