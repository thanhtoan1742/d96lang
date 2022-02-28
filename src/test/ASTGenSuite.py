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
    # class decl
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


    # class attr decl
    def test_attr_decl_0(self):
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


    def test_attr_decl_1(self):
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

    def test_attr_decl_2(self):
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

    def test_attr_decl_3(self):
        testcase = \
"""Class Program {
    Var a, $b: Int = 10;
    Val s: String = "text";
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
                )),
                AST.AttributeDecl(AST.Instance() ,AST.ConstDecl(
                    AST.Id("s"),
                    AST.StringType(),
                    AST.StringLiteral("text")
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_attr_decl_4(self):
        testcase = \
"""Class Program {
    Var a, $b: Int = 10;
    Val s, t: String = "text";
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
                )),
                AST.AttributeDecl(AST.Instance() ,AST.ConstDecl(
                    AST.Id("s"),
                    AST.StringType(),
                    AST.StringLiteral("text")
                )),
                AST.AttributeDecl(AST.Instance() ,AST.ConstDecl(
                    AST.Id("t"),
                    AST.StringType(),
                ))
            ]),
        ]))
        self._test(testcase, expect)



    def test_method_decl_0(self):
        testcase = \
"""Class Program {
    main() {
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_1(self):
        testcase = \
"""Class Program {
    $main() {
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Static(), AST.Id("$main"), [], AST.Block([]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_2(self):
        testcase = \
"""Class Program {
    main() {}
    $staticMethod() {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([])),
                AST.MethodDecl(AST.Static(), AST.Id("$staticMethod"), [], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_3(self):
        testcase = \
"""Class Program {
    Constructor() {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("Constructor"), [], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_4(self):
        testcase = \
"""Class Program {
    Constructor(arg: String) {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("Constructor"), [
                    AST.VarDecl(AST.Id("arg"), AST.StringType())
                ], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_5(self):
        testcase = \
"""Class Program {
    Destructor() {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("Destructor"), [], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_6(self):
        testcase = \
"""Class Agent{
    takeDamage(damage: Int; damageType: DamageType) {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Agent"), [
                AST.MethodDecl(AST.Instance(), AST.Id("takeDamage"), [
                    AST.VarDecl(AST.Id('damage'), AST.IntType()),
                    AST.VarDecl(AST.Id('damageType'), AST.ClassType(AST.Id('DamageType'))),
                ], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_decl_6(self):
        testcase = \
"""Class Agent{
    takeBlind(blindDuration, blindRadius: Int; blindType: BlindType) {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Agent"), [
                AST.MethodDecl(AST.Instance(), AST.Id("takeBlind"), [
                    AST.VarDecl(AST.Id('blindDuration'), AST.IntType()),
                    AST.VarDecl(AST.Id('blindRadius'), AST.IntType()),
                    AST.VarDecl(AST.Id('blindType'), AST.ClassType(AST.Id('BlindType'))),
                ], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)


    # var decl stmt test

    def test_var_decl_stmt_0(self):
        testcase = \
"""Class Program{
    main() {
        Var i: Int;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.VarDecl(AST.Id("i"), AST.IntType()),
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_var_decl_stmt_1(self):
        testcase = \
"""Class Program{
    main() {
        Val i: Int;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("i"), AST.IntType()),
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_var_decl_stmt_2(self):
        testcase = \
"""Class Program{
    main() {
        Var i: Int = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.VarDecl(AST.Id("i"), AST.IntType(), AST.IntLiteral(1)),
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_var_decl_stmt_3(self):
        testcase = \
"""Class Program{
    main() {
        Val i: Int = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("i"), AST.IntType(), AST.IntLiteral(1)),
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_var_decl_stmt_4(self):
        testcase = \
"""Class Program{
    main() {
        Val i, j: Int = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("i"), AST.IntType(), AST.IntLiteral(1)),
                    AST.ConstDecl(AST.Id("j"), AST.IntType()),
                ])),
            ]),
        ]))
        self._test(testcase, expect)



    # block stmt
    def test_block_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Val a: Int = 2;
        Return a;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("a"), AST.IntType(), AST.IntLiteral(2)),
                    AST.Return(AST.Id('a'))
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # for stmt
    def test_for_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Foreach(i In 1 .. 100 By 2) {
            Out.printInt(i);
        }
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.For(
                        AST.Id('i'),
                        AST.IntLiteral(1),
                        AST.IntLiteral(100),
                        AST.Block([
                            AST.CallStmt(AST.Id('Out'), AST.Id('printInt'), [
                                AST.Id('i')
                            ])
                        ]),
                        AST.IntLiteral(2)
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)



