import unittest
from TestUtils import TestAST
from LexerSuite import write_wrong_answer
import AST

class ASTGenSuite(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        ASTGenSuite.counter = 1999

    def _test(self, testcase, expect):
        ASTGenSuite.counter += 1
        try:
            self.assertTrue(TestAST.test(testcase, expect, ASTGenSuite.counter))
        except AssertionError:
            write_wrong_answer(expect, self.counter)
            raise AssertionError(f"ast gen failed at test {ASTGenSuite.counter}")

    # sample test from BKeL
    def test_sample_0(self):
        testcase = "Class Program {}"
        expect = "Program([ClassDecl(Id(Program),[])])"
        self._test(testcase, expect)

    def test_sample_1(self):
        testcase = "Class Rectangle : Shape {}"
        expect = "Program([ClassDecl(Id(Rectangle),Id(Shape),[])])"
        self._test(testcase, expect)

    def test_sample_2(self):
        testcase = \
"""Class Rectangle {
    Var length: Int;
}"""
        expect = "Program([ClassDecl(Id(Rectangle),[AttributeDecl(Instance,VarDecl(Id(length),IntType))])])"
        self._test(testcase, expect)

    def test_sample_3(self):
        testcase = \
"""Class Rectangle {
    Val $x: Int = 10;
}"""
        expect = "Program([ClassDecl(Id(Rectangle),[AttributeDecl(Static,ConstDecl(Id($x),IntType,IntLit(10)))])])"
        self._test(testcase, expect)


    # my test
    def test_class_decl_0(self):
        testcase = "Class Program{}"
        expect = str(AST.Program([AST.ClassDecl(AST.Id("Program"), [])]))
        self._test(testcase, expect)

    def test_class_decl_1(self):
        testcase = "Class Program{} Class Program2{}"
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), []),
            AST.ClassDecl(AST.Id("Program2"), [])
        ]))
        self._test(testcase, expect)


    def test_class_mems_0(self):
        testcase = \
"""Class Program {
    Var i: Int = 10;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance() ,AST.VarDecl(
                    AST.Id("i"),
                    AST.IntType(),
                    AST.IntLiteral(10)
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_class_mems_1(self):
        testcase = \
"""Class Program {
    Var $i: Int = 10;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Static() ,AST.VarDecl(
                    AST.Id("$i"),
                    AST.IntType(),
                    AST.IntLiteral(10)
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_class_mems_2(self):
        testcase = \
"""Class Program {
    Var a, $b: Int = 10;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance() ,AST.VarDecl(
                    AST.Id("a"),
                    AST.IntType(),
                    AST.IntLiteral(10)
                )),
                AST.AttributeDecl(AST.Static() ,AST.VarDecl(
                    AST.Id("$b"),
                    AST.IntType(),
                ))
            ]),
        ]))
        self._test(testcase, expect)

