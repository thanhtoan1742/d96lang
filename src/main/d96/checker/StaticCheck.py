
import AST
from Visitor import *
from Utils import Utils
from StaticError import *
from dataclasses import dataclass

"""
what happens when a method returns multiple time and the return types are diffrent?
what happens when a method is a recursive loop with no end point?
"""


@dataclass
class MethodDeclRet(AST.MethodDecl):
    retType: AST.Type = AST.VoidType()



class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype


class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value


class SymbolPool:
    def __init__(self) -> None:
        self.scope = 0
        self.pools[self.scope] = {}

    def inc_scope(self):
        self.scope += 1
        self.pools[self.scope] = {}

    def dec_scope(self):
        self.pools.pop(self.scope)
        self.scope -= 1

    def is_declared_in_current_scope(self, id):
        return id in self.pools[self.scope]

    def get_symbol(self, id):
        for s in range(self.scope, -1, -1):
            if id in self.pools[s]:
                return self.pools[s][id]
        return None




class StaticChecker(BaseVisitor, Utils):
    def __init__(self, ast):
        self.ast = ast

    def check(self):
        ast = FirstPassChecker().visit(self.ast, {})
        SecondPassChecker().visit(ast, {})


# visit the given AST then return a new AST where all type a resolved.
# do some memantic check also
class FirstPassChecker(BaseVisitor, Utils):
    def visitAST(self, ctx, visit_params):
        pass

    def visitInst(self, ctx, visit_params):
        pass

    def visitStmt(self, ctx, visit_params):
        pass

    def visitExpr(self, ctx, visit_params):
        pass

    def visitLHS(self, ctx, visit_params):
        pass

    def visitType(self, ctx, visit_params):
        pass

    def visitMemDecl(self, ctx, visit_params):
        pass

    def visitId(self, ctx, visit_params):
        pass

    def visitBinaryOp(self, ctx, visit_params):
        pass

    def visitUnaryOp(self, ctx, visit_params):
        pass

    def visitCallExpr(self, ctx, visit_params):
        pass

    def visitNewExpr(self, ctx, visit_params):
        pass

    def visitArrayCell(self, ctx, visit_params):
        pass

    def visitFieldAccess(self, ctx, visit_params):
        pass

    def visitLiteral(self, ctx, visit_params):
        pass

    def visitIntLiteral(self, ctx, visit_params):
        pass

    def visitFloatLiteral(self, ctx, visit_params):
        pass

    def visitStringLiteral(self, ctx, visit_params):
        pass

    def visitBooleanLiteral(self, ctx, visit_params):
        pass

    def visitNullLiteral(self, ctx, visit_params):
        pass

    def visitSelfLiteral(self, ctx, visit_params):
        pass

    def visitArrayLiteral(self, ctx, visit_params):
        pass

    def visitDecl(self, ctx, visit_params):
        pass

    def visitStoreDecl(self, ctx, visit_params):
        pass

    def visitAssign(self, ctx, visit_params):
        pass

    def visitIf(self, ctx, visit_params):
        pass

    def visitFor(self, ctx, visit_params):
        pass

    def visitBreak(self, ctx, visit_params):
        pass

    def visitContinue(self, ctx, visit_params):
        pass

    def visitReturn(self, ctx, visit_params):
        pass

    def visitCallStmt(self, ctx, visit_params):
        pass

    def visitVarDecl(self, ctx, visit_params):
        pass

    def visitBlock(self, ctx, visit_params):
        pass

    def visitConstDecl(self, ctx, visit_params):
        pass

    def visitClassDecl(self, ctx, visit_params):
        pass

    def visitSIKind(self, ctx, visit_params):
        pass

    def visitInstance(self, ctx, visit_params):
        pass

    def visitStatic(self, ctx, visit_params):
        pass

    def visitMethodDecl(self, ctx, visit_params):
        pass

    def visitAttributeDecl(self, ctx, visit_params):
        pass

    def visitIntType(self, ctx, visit_params):
        pass

    def visitFloatType(self, ctx, visit_params):
        pass

    def visitBoolType(self, ctx, visit_params):
        pass

    def visitStringType(self, ctx, visit_params):
        pass

    def visitArrayType(self, ctx, visit_params):
        pass

    def visitClassType(self, ctx, visit_params):
        pass

    def visitVoidType(self, ctx, visit_params):
        pass

    def visitProgram(self, ctx, visit_params):
        for d in ctx.decl:
            self.visit(d, visit_params)



class SecondPassChecker(BaseVisitor, Utils):
    pass