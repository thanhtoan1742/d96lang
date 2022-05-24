'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from abc import ABC, abstractmethod
from Visitor import BaseVisitor
from Emitter import Emitter
from Frame import Frame
import AST




Type = AST.Type
IntType = AST.IntType
FloatType = AST.FloatType
BoolType = AST.BoolType
StringType = AST.StringType
VoidType = AST.VoidType
ArrayType = AST.ArrayType

class ClassType(Type):
    def __init__(self, className: str):
        self.className = className

class MethodType(Type):
    def __init__(self, parTypes, retType) -> None:
        self.parTypes = parTypes
        self.retType = retType





class CodeGenerator:
    def __init__(self):
        self.libName = "io"

    def init(self):
        # return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
        #         Symbol("putInt", MType([IntType()],
        #                VoidType()), CName(self.libName)),
        #         Symbol("putIntLn", MType([IntType()],
        #                VoidType()), CName(self.libName))

        #         ]
        return []

    def gen(self, ast, path):
        #ast: AST
        #dir_: String
        gl = self.init()
        gc = CodeGenVisitor(ast, gl, path)
        gc.visit(ast, None)




class CodeGenVisitor(BaseVisitor):
    def __init__(self, ast, env, path):
        #astTree: AST
        #env: List[Symbol]
        #path: str
        self.ast = ast
        self.env = env
        self.className = "D96Class"
        self.path = path
        self.emit = Emitter(self.path + "/" + self.className + ".j")

