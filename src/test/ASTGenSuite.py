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

    def test_method_decl_7(self):
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

    def test_method_decl_8(self):
        testcase = \
"""Class Agent{
    Constructor(name: String) {}
    Destructor() {}
    takeBlind(blindDuration, blindRadius: Int; blindType: BlindType) {}
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Agent"), [
                AST.MethodDecl(AST.Instance(), AST.Id("Constructor"), [
                    AST.VarDecl(AST.Id("name"), AST.StringType()),
                ], AST.Block([])),
                AST.MethodDecl(AST.Instance(), AST.Id("Destructor"), [], AST.Block([])),
                AST.MethodDecl(AST.Instance(), AST.Id("takeBlind"), [
                    AST.VarDecl(AST.Id('blindDuration'), AST.IntType()),
                    AST.VarDecl(AST.Id('blindRadius'), AST.IntType()),
                    AST.VarDecl(AST.Id('blindType'), AST.ClassType(AST.Id('BlindType'))),
                ], AST.Block([])),
            ]),
        ]))
        self._test(testcase, expect)


    # test assign stmt
    def test_assign_stmt_0(self):
        testcase = \
"""Class Program{
    main() {
        i = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Assign(AST.Id("i"), AST.IntLiteral(1))
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_assign_stmt_1(self):
        testcase = \
"""Class Program{
    main() {
        arr[0][1][2] = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Assign(
                        AST.ArrayCell(AST.Id("arr"), [
                            AST.IntLiteral(0),
                            AST.IntLiteral(1),
                            AST.IntLiteral(2),
                        ]),
                        AST.IntLiteral(1),
                    )
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_assign_stmt_2(self):
        testcase = \
"""Class Program{
    main() {
        Self.i = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Assign(
                        AST.FieldAccess(AST.SelfLiteral(), AST.Id('i')),
                        AST.IntLiteral(1),
                    )
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_assign_stmt_3(self):
        testcase = \
"""Class Program{
    main() {
        Program::$i = 1;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Assign(
                        AST.FieldAccess(AST.Id('Program'), AST.Id('$i')),
                        AST.IntLiteral(1),
                    )
                ])),
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

    def test_var_decl_stmt_5(self):
        testcase = \
"""Class Program{
    main() {
        Var a, b, c, d, e: Int = 1, 2, 3;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.VarDecl(AST.Id("a"), AST.IntType(), AST.IntLiteral(1)),
                    AST.VarDecl(AST.Id("b"), AST.IntType(), AST.IntLiteral(2)),
                    AST.VarDecl(AST.Id("c"), AST.IntType(), AST.IntLiteral(3)),
                    AST.VarDecl(AST.Id("d"), AST.IntType()),
                    AST.VarDecl(AST.Id("e"), AST.IntType()),
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_var_decl_stmt_6(self):
        testcase = \
"""Class Program{
    main() {
        Var a, b, c, d, e: Int = 1, 2, 3;
        Val x, y, z: String = "text";
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.VarDecl(AST.Id("a"), AST.IntType(), AST.IntLiteral(1)),
                    AST.VarDecl(AST.Id("b"), AST.IntType(), AST.IntLiteral(2)),
                    AST.VarDecl(AST.Id("c"), AST.IntType(), AST.IntLiteral(3)),
                    AST.VarDecl(AST.Id("d"), AST.IntType()),
                    AST.VarDecl(AST.Id("e"), AST.IntType()),
                    AST.ConstDecl(AST.Id("x"), AST.StringType(), AST.StringLiteral("text")),
                    AST.ConstDecl(AST.Id("y"), AST.StringType()),
                    AST.ConstDecl(AST.Id("z"), AST.StringType()),
                ])),
            ]),
        ]))
        self._test(testcase, expect)



    # if stmt
    def test_if_stmt_0(self):
        testcase = \
"""Class Program{
    main() {
        If (1) {
            Return 1;
        }
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.If(AST.IntLiteral(1), AST.Block([AST.Return(AST.IntLiteral(1))]))
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_if_stmt_1(self):
        testcase = \
"""Class Program{
    main() {
        If (1) {
            Return 1;
        } Else {
            Return 0;
        }
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.If(
                        AST.IntLiteral(1),
                        AST.Block([AST.Return(AST.IntLiteral(1))]),
                        AST.Block([AST.Return(AST.IntLiteral(0))])
                    )
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_if_stmt_2(self):
        testcase = \
"""Class Program{
    main() {
        If (1) {
            Return 1;
        }
        Elseif (2) {
            Return 2;
        } Else {
            Return 0;
        }
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.If(
                        AST.IntLiteral(1),
                        AST.Block([AST.Return(AST.IntLiteral(1))]),
                        AST.If(
                            AST.IntLiteral(2),
                            AST.Block([AST.Return(AST.IntLiteral(2))]),
                            AST.Block([AST.Return(AST.IntLiteral(0))]),
                        )
                    )
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_if_stmt_3(self):
        testcase = \
"""Class Program{
    main() {
        If (1) {
            Return 1;
        }
        Elseif (2) {
            Return 2;
        }
        Elseif (3) {
            Return 3;
        }
        Elseif (4) {
            Return 4;
        }
        Else {
            Return 0;
        }
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.If(
                        AST.IntLiteral(1),
                        AST.Block([AST.Return(AST.IntLiteral(1))]),
                        AST.If(
                            AST.IntLiteral(2),
                            AST.Block([AST.Return(AST.IntLiteral(2))]),
                            AST.If(
                                AST.IntLiteral(3),
                                AST.Block([AST.Return(AST.IntLiteral(3))]),
                                AST.If(
                                    AST.IntLiteral(4),
                                    AST.Block([AST.Return(AST.IntLiteral(4))]),
                                    AST.Block([AST.Return(AST.IntLiteral(0))]),
                                )
                            )
                        )
                    )
                ])),
            ]),
        ]))
        self._test(testcase, expect)




    # return stmt
    def test_return_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Return;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return()
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_return_stmt_1(self):
        testcase = \
"""Class Program {
    main() {
        Return 0;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(AST.IntLiteral(0))
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # for stmt
    def test_for_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Foreach(i In 1 .. 100) {
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
                        AST.Block([]),
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_for_stmt_1(self):
        testcase = \
"""Class Program {
    main() {
        Foreach(i In 1 .. 100 By 2) {
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
                        AST.Block([]),
                        AST.IntLiteral(2),
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_for_stmt_3(self):
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


    # continue stmt
    def test_continue_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Foreach(i In 1 .. 100 By 2) {
            Continue;
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
                            AST.Continue()
                        ]),
                        AST.IntLiteral(2),
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # break stmt
    def test_break_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Foreach(i In 1 .. 100 By 2) {
            Break;
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
                            AST.Break()
                        ]),
                        AST.IntLiteral(2),
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)



    # method invoke stmt
    def test_method_invoke_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
        Out.printInt(1);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.CallStmt(AST.Id("Out"), AST.Id("printInt"), [AST.IntLiteral(1)])
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_invoke_stmt_1(self):
        testcase = \
"""Class Program {
    main() {
        Out.printInt(1, 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.CallStmt(AST.Id("Out"), AST.Id("printInt"), [
                        AST.IntLiteral(1),
                        AST.IntLiteral(2),
                    ])
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_invoke_stmt_2(self):
        testcase = \
"""Class Program {
    main() {
        Humanity::$getPopulation();
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.CallStmt(AST.Id("Humanity"), AST.Id("$getPopulation"), [])
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_method_invoke_stmt_3(self):
        testcase = \
"""Class Program {
    main() {
        Humanity::$getPopulation(True);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.CallStmt(AST.Id("Humanity"), AST.Id("$getPopulation"), [
                        AST.BooleanLiteral(True)
                    ])
                ]))
            ]),
        ]))
        self._test(testcase, expect)



    # block stmt
    def test_block_stmt_0(self):
        testcase = \
"""Class Program {
    main() {
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_block_stmt_1(self):
        testcase = \
"""Class Program {
    main() {
        Val a: Int = 2;
        If (a > 0) {
            a = 1;
        }
        Else {
            a = 0;
        }
        Return a;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("a"), AST.IntType(), AST.IntLiteral(2)),
                    AST.If(
                        AST.BinaryOp(">", AST.Id("a"), AST.IntLiteral(0)),
                        AST.Block([AST.Assign(AST.Id("a"), AST.IntLiteral(1))]),
                        AST.Block([AST.Assign(AST.Id("a"), AST.IntLiteral(0))]),
                    ),
                    AST.Return(AST.Id('a'))
                ]))
            ]),
        ]))
        self._test(testcase, expect)



    # binary op
    def test_binary_op_0(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 > 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp(">", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_1(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 < 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("<", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_2(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 == 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("==", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_3(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 != 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("!=", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_4(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 <= 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("<=", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_5(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 >= 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp(">=", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_6(self):
        testcase = \
"""Class Program {
    main() {
        Return ("1" +. "2");
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("+.", AST.StringLiteral("1"), AST.StringLiteral("2"))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_7(self):
        testcase = \
"""Class Program {
    main() {
        Return ("1" ==. "2");
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("==.", AST.StringLiteral("1"), AST.StringLiteral("2"))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_8(self):
        testcase = \
"""Class Program {
    main() {
        Return (True && False);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("&&", AST.BooleanLiteral(True), AST.BooleanLiteral(False))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_9(self):
        testcase = \
"""Class Program {
    main() {
        Return (True || False);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("||", AST.BooleanLiteral(True), AST.BooleanLiteral(False))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_10(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 + 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("+", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_11(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 - 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("-", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_12(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 * 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("*", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_13(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 / 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("/", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_binary_op_14(self):
        testcase = \
"""Class Program {
    main() {
        Return (1 % 2);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.BinaryOp("%", AST.IntLiteral(1), AST.IntLiteral(2))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # test unary op
    def test_unary_op_0(self):
        testcase = \
"""Class Program {
    main() {
        Return (!True);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.UnaryOp('!', AST.BooleanLiteral(True))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_unary_op_1(self):
        testcase = \
"""Class Program {
    main() {
        Return (-1);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.UnaryOp('-', AST.IntLiteral(1))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # member access
    def test_member_access_0(self):
        testcase = \
"""Class Program {
    main() {
        Return Self.i;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.FieldAccess(AST.SelfLiteral(), AST.Id("i"))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_member_access_1(self):
        testcase = \
"""Class Program {
    main() {
        Return Self.i();
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.CallExpr(AST.SelfLiteral(), AST.Id("i"), [])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_member_access_2(self):
        testcase = \
"""Class Program {
    main() {
        Return Self.i(1, False, "a");
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.CallExpr(AST.SelfLiteral(), AST.Id("i"), [
                            AST.IntLiteral(1),
                            AST.BooleanLiteral(False),
                            AST.StringLiteral("a"),
                        ])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_member_access_3(self):
        testcase = \
"""Class Program {
    main() {
        Return Program::$i;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.FieldAccess(AST.Id("Program"), AST.Id("$i"))
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_member_access_4(self):
        testcase = \
"""Class Program {
    main() {
        Return Program::$i();
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.CallExpr(AST.Id("Program"), AST.Id("$i"), [])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_member_access_5(self):
        testcase = \
"""Class Program {
    main() {
        Return Program::$i(1, False, "a");
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.CallExpr(AST.Id("Program"), AST.Id("$i"), [
                            AST.IntLiteral(1),
                            AST.BooleanLiteral(False),
                            AST.StringLiteral("a"),
                        ])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # index op
    def test_index_op_0(self):
        testcase = \
"""Class Program {
    main() {
        Return arr[0];
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.ArrayCell(AST.Id("arr"), [
                            AST.IntLiteral(0)
                        ])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_index_op_1(self):
        testcase = \
"""Class Program {
    main() {
        Return arr[0][1][2][3];
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.ArrayCell(AST.Id("arr"), [
                            AST.IntLiteral(0),
                            AST.IntLiteral(1),
                            AST.IntLiteral(2),
                            AST.IntLiteral(3),
                        ])
                    )
                ]))
            ]),
        ]))

    def test_index_op_2(self):
        testcase = \
"""Class Program {
    main() {
        Return arr[i][i + 1][i + 2][i + 3];
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.ArrayCell(AST.Id("arr"), [
                            AST.Id("i"),
                            AST.BinaryOp("+", AST.Id("i"), AST.IntLiteral(1)),
                            AST.BinaryOp("+", AST.Id("i"), AST.IntLiteral(2)),
                            AST.BinaryOp("+", AST.Id("i"), AST.IntLiteral(3)),
                        ])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # new op
    def test_new_op_0(self):
        testcase = \
"""Class Program {
    main() {
        Return New Program();
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.NewExpr(AST.Id("Program"), [])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_new_op_1(self):
        testcase = \
"""Class Program {
    main() {
        Return New Program(1, False, "a");
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.NewExpr(AST.Id("Program"), [
                            AST.IntLiteral(1),
                            AST.BooleanLiteral(False),
                            AST.StringLiteral("a"),
                        ])
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # self
    def test_self_0(self):
        testcase = \
"""Class Program {
    main() {
        Return Self;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(
                        AST.SelfLiteral()
                    )
                ]))
            ]),
        ]))
        self._test(testcase, expect)


    # type
    def test_type_0(self):
        testcase = \
"""Class Program {
    Var a: Int;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.IntType(),
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_type_1(self):
        testcase = \
"""Class Program {
    Var a: Float;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.FloatType(),
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_type_2(self):
        testcase = \
"""Class Program {
    Var a: Boolean;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.BoolType(),
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_type_3(self):
        testcase = \
"""Class Program {
    Var a: String;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.StringType(),
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_type_4(self):
        testcase = \
"""Class Program {
    Var a: Array[Int, 2];
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.ArrayType(2, AST.IntType()),
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_type_5(self):
        testcase = \
"""Class Program {
    Var a: Array[Array[Array[Int, 4], 3], 2];
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.ArrayType(2, AST.ArrayType(3, AST.ArrayType(4, AST.IntType()))),
                ))
            ]),
        ]))
        self._test(testcase, expect)

    def test_type_6(self):
        testcase = \
"""Class Program {
    Var a: Human;
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(
                    AST.Id("a"),
                    AST.ClassType(AST.Id("Human")),
                ))
            ]),
        ]))
        self._test(testcase, expect)

