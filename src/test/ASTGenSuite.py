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

    def test_assign_stmt_4(self):
        testcase = \
"""Class Program{
    main() {
        Program::$i = Input.readInt();
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Assign(
                        AST.FieldAccess(AST.Id('Program'), AST.Id('$i')),
                        AST.CallExpr(AST.Id("Input"), AST.Id("readInt"), []),
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

    def test_return_stmt_2(self):
        testcase = \
"""Class Program {
    main() {
        Return New Shape();
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(AST.NewExpr(AST.Id("Shape"), []))
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_return_stmt_3(self):
        testcase = \
"""Class Program {
    main() {
        Return New Shape(1);
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.Return(AST.NewExpr(AST.Id("Shape"), [AST.IntLiteral(1)]))
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


    # full program
    def test_program_0(self):
        testcase = \
"""Class Program {
    main() {
        Out.print("Hello World!");
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.CallStmt(AST.Id("Out"), AST.Id("print"), [AST.StringLiteral("Hello World!")])
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_program_1(self):
        testcase = \
"""
Class Vector3 {
    Var x, y, z: Float = 0, 0, 0;
}

Class Program {
    main() {
        Val coord: Vector3;
    }
}
"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Vector3"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("x"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("y"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("z"), AST.FloatType(), AST.IntLiteral(0))),
            ]),
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("coord"), AST.ClassType(AST.Id("Vector3"))),
                ]))
            ]),
        ]))
        self._test(testcase, expect)

    def test_program_2(self):
        testcase = \
"""
Class Vector3 {
    Var x, y, z: Float = 0, 0, 0;
}

Class Program {
    triangleArea(a, b, c: Vector3) {

    }

    main() {
    }
}
"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Vector3"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("x"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("y"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("z"), AST.FloatType(), AST.IntLiteral(0))),
            ]),
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("triangleArea"), [
                    AST.VarDecl(AST.Id("a"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("b"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("c"), AST.ClassType(AST.Id("Vector3"))),
                ], AST.Block([
                ])),
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                ])),
            ]),
        ]))
        self._test(testcase, expect)


    def test_program_3(self):
        testcase = \
"""
Class Vector3 {
    Var x, y, z: Float = 0, 0, 0;
}

Class Program {
    triangleArea(a, b, c: Vector3) {
        Val S: Float = (a.x + b.x)*(a.y - b.y) + (b.x + c.x)*(b.y - c.y) + (c.x + a.x)*(c.y - a.y);
        Return Math::$abs(S) / 2;
    }

    main() {
    }
}
"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Vector3"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("x"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("y"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("z"), AST.FloatType(), AST.IntLiteral(0))),
            ]),
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("triangleArea"), [
                    AST.VarDecl(AST.Id("a"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("b"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("c"), AST.ClassType(AST.Id("Vector3"))),
                ], AST.Block([
                    AST.ConstDecl(AST.Id("S"), AST.FloatType(), AST.BinaryOp(
                        "+",
                        AST.BinaryOp(
                            "+",
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                ),
                            ),
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                ),
                            ),
                        ),
                        AST.BinaryOp(
                            "*",
                            AST.BinaryOp(
                                "+",
                                AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                            ),
                            AST.BinaryOp(
                                "-",
                                AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                            ),
                        ),
                    )),
                    AST.Return(AST.BinaryOp(
                        "/",
                        AST.CallExpr(
                            AST.Id("Math"),
                            AST.Id("$abs"),
                            [AST.Id("S")]
                        ),
                        AST.IntLiteral(2),
                    ))
                ])),
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                ])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_program_4(self):
        testcase = \
"""
Class Vector3 {
    Var x, y, z: Float = 0, 0, 0;
    Constructor(x, y, z: Float) {
        Self.x = x;
        Self.y = y;
        Self.z = z;
    }
}

Class Program {
    triangleArea(a, b, c: Vector3) {
        Val S: Float = (a.x + b.x)*(a.y - b.y) + (b.x + c.x)*(b.y - c.y) + (c.x + a.x)*(c.y - a.y);
        Return Math::$abs(S) / 2;
    }

    main() {
    }
}
"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Vector3"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("x"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("y"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("z"), AST.FloatType(), AST.IntLiteral(0))),
                AST.MethodDecl(AST.Instance(), AST.Id("Constructor"), [
                    AST.VarDecl(AST.Id("x"), AST.FloatType()),
                    AST.VarDecl(AST.Id("y"), AST.FloatType()),
                    AST.VarDecl(AST.Id("z"), AST.FloatType()),
                ], AST.Block([
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("x")), AST.Id("x")),
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("y")), AST.Id("y")),
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("z")), AST.Id("z")),
                ]))
            ]),
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("triangleArea"), [
                    AST.VarDecl(AST.Id("a"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("b"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("c"), AST.ClassType(AST.Id("Vector3"))),
                ], AST.Block([
                    AST.ConstDecl(AST.Id("S"), AST.FloatType(), AST.BinaryOp(
                        "+",
                        AST.BinaryOp(
                            "+",
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                ),
                            ),
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                ),
                            ),
                        ),
                        AST.BinaryOp(
                            "*",
                            AST.BinaryOp(
                                "+",
                                AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                            ),
                            AST.BinaryOp(
                                "-",
                                AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                            ),
                        ),
                    )),
                    AST.Return(AST.BinaryOp(
                        "/",
                        AST.CallExpr(
                            AST.Id("Math"),
                            AST.Id("$abs"),
                            [AST.Id("S")]
                        ),
                        AST.IntLiteral(2),
                    ))
                ])),
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                ])),
            ]),
        ]))
        self._test(testcase, expect)


    def test_program_5(self):
        testcase = \
"""
Class Vector3 {
    Var x, y, z: Float = 0, 0, 0;
    Constructor(x, y, z: Float) {
        Self.x = x;
        Self.y = y;
        Self.z = z;
    }

    $read() {
        Var x, y, z: Float;
        x = Input.readFloat();
        y = Input.readFloat();
        z = Input.readFloat();
        Return New Vector3(x, y, z);
    }
}

Class Program {
    triangleArea(a, b, c: Vector3) {
        Val S: Float = (a.x + b.x)*(a.y - b.y) + (b.x + c.x)*(b.y - c.y) + (c.x + a.x)*(c.y - a.y);
        Return Math::$abs(S) / 2;
    }

    main() {
    }
}
"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Vector3"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("x"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("y"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("z"), AST.FloatType(), AST.IntLiteral(0))),
                AST.MethodDecl(AST.Instance(), AST.Id("Constructor"), [
                    AST.VarDecl(AST.Id("x"), AST.FloatType()),
                    AST.VarDecl(AST.Id("y"), AST.FloatType()),
                    AST.VarDecl(AST.Id("z"), AST.FloatType()),
                ], AST.Block([
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("x")), AST.Id("x")),
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("y")), AST.Id("y")),
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("z")), AST.Id("z")),
                ])),
                AST.MethodDecl(AST.Static(), AST.Id("$read"), [], AST.Block([
                    AST.VarDecl(AST.Id("x"), AST.FloatType()),
                    AST.VarDecl(AST.Id("y"), AST.FloatType()),
                    AST.VarDecl(AST.Id("z"), AST.FloatType()),
                    AST.Assign(AST.Id("x"), AST.CallExpr(AST.Id("Input"), AST.Id("readFloat"), [])),
                    AST.Assign(AST.Id("y"), AST.CallExpr(AST.Id("Input"), AST.Id("readFloat"), [])),
                    AST.Assign(AST.Id("z"), AST.CallExpr(AST.Id("Input"), AST.Id("readFloat"), [])),
                    AST.Return(AST.NewExpr(AST.Id("Vector3"), [
                        AST.Id("x"),
                        AST.Id("y"),
                        AST.Id("z"),
                    ]))
                ])),
            ]),
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("triangleArea"), [
                    AST.VarDecl(AST.Id("a"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("b"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("c"), AST.ClassType(AST.Id("Vector3"))),
                ], AST.Block([
                    AST.ConstDecl(AST.Id("S"), AST.FloatType(), AST.BinaryOp(
                        "+",
                        AST.BinaryOp(
                            "+",
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                ),
                            ),
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                ),
                            ),
                        ),
                        AST.BinaryOp(
                            "*",
                            AST.BinaryOp(
                                "+",
                                AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                            ),
                            AST.BinaryOp(
                                "-",
                                AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                            ),
                        ),
                    )),
                    AST.Return(AST.BinaryOp(
                        "/",
                        AST.CallExpr(
                            AST.Id("Math"),
                            AST.Id("$abs"),
                            [AST.Id("S")]
                        ),
                        AST.IntLiteral(2),
                    ))
                ])),
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                ])),
            ]),
        ]))
        self._test(testcase, expect)


    def test_program_6(self):
        testcase = \
"""
Class Vector3 {
    Var x, y, z: Float = 0, 0, 0;
    Constructor(x, y, z: Float) {
        Self.x = x;
        Self.y = y;
        Self.z = z;
    }

    $read() {
        Var x, y, z: Float;
        x = Input.readFloat();
        y = Input.readFloat();
        z = Input.readFloat();
        Return New Vector3(x, y, z);
    }
}

Class Program {
    triangleArea(a, b, c: Vector3) {
        Val S: Float = (a.x + b.x)*(a.y - b.y) + (b.x + c.x)*(b.y - c.y) + (c.x + a.x)*(c.y - a.y);
        Return Math::$abs(S) / 2;
    }

    main() {
        Val a: Vector3 = Vector3::$read();
        Val b: Vector3 = Vector3::$read();
        Val c: Vector3 = Vector3::$read();
        Output.printFloat(Self.triangleArea(a, b, c));
    }
}
"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Vector3"), [
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("x"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("y"), AST.FloatType(), AST.IntLiteral(0))),
                AST.AttributeDecl(AST.Instance(), AST.VarDecl(AST.Id("z"), AST.FloatType(), AST.IntLiteral(0))),
                AST.MethodDecl(AST.Instance(), AST.Id("Constructor"), [
                    AST.VarDecl(AST.Id("x"), AST.FloatType()),
                    AST.VarDecl(AST.Id("y"), AST.FloatType()),
                    AST.VarDecl(AST.Id("z"), AST.FloatType()),
                ], AST.Block([
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("x")), AST.Id("x")),
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("y")), AST.Id("y")),
                    AST.Assign(AST.FieldAccess(AST.SelfLiteral(), AST.Id("z")), AST.Id("z")),
                ])),
                AST.MethodDecl(AST.Static(), AST.Id("$read"), [], AST.Block([
                    AST.VarDecl(AST.Id("x"), AST.FloatType()),
                    AST.VarDecl(AST.Id("y"), AST.FloatType()),
                    AST.VarDecl(AST.Id("z"), AST.FloatType()),
                    AST.Assign(AST.Id("x"), AST.CallExpr(AST.Id("Input"), AST.Id("readFloat"), [])),
                    AST.Assign(AST.Id("y"), AST.CallExpr(AST.Id("Input"), AST.Id("readFloat"), [])),
                    AST.Assign(AST.Id("z"), AST.CallExpr(AST.Id("Input"), AST.Id("readFloat"), [])),
                    AST.Return(AST.NewExpr(AST.Id("Vector3"), [
                        AST.Id("x"),
                        AST.Id("y"),
                        AST.Id("z"),
                    ]))
                ])),
            ]),
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("triangleArea"), [
                    AST.VarDecl(AST.Id("a"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("b"), AST.ClassType(AST.Id("Vector3"))),
                    AST.VarDecl(AST.Id("c"), AST.ClassType(AST.Id("Vector3"))),
                ], AST.Block([
                    AST.ConstDecl(AST.Id("S"), AST.FloatType(), AST.BinaryOp(
                        "+",
                        AST.BinaryOp(
                            "+",
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                ),
                            ),
                            AST.BinaryOp(
                                "*",
                                AST.BinaryOp(
                                    "+",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("x")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                ),
                                AST.BinaryOp(
                                    "-",
                                    AST.FieldAccess(AST.Id("b"), AST.Id("y")),
                                    AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                ),
                            ),
                        ),
                        AST.BinaryOp(
                            "*",
                            AST.BinaryOp(
                                "+",
                                AST.FieldAccess(AST.Id("c"), AST.Id("x")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("x")),
                            ),
                            AST.BinaryOp(
                                "-",
                                AST.FieldAccess(AST.Id("c"), AST.Id("y")),
                                AST.FieldAccess(AST.Id("a"), AST.Id("y")),
                            ),
                        ),
                    )),
                    AST.Return(AST.BinaryOp(
                        "/",
                        AST.CallExpr(
                            AST.Id("Math"),
                            AST.Id("$abs"),
                            [AST.Id("S")]
                        ),
                        AST.IntLiteral(2),
                    ))
                ])),
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([
                    AST.ConstDecl(AST.Id("a"), AST.ClassType(AST.Id("Vector3")), AST.CallExpr(AST.Id("Vector3"), AST.Id("$read"), [])),
                    AST.ConstDecl(AST.Id("b"), AST.ClassType(AST.Id("Vector3")), AST.CallExpr(AST.Id("Vector3"), AST.Id("$read"), [])),
                    AST.ConstDecl(AST.Id("c"), AST.ClassType(AST.Id("Vector3")), AST.CallExpr(AST.Id("Vector3"), AST.Id("$read"), [])),
                    AST.CallStmt(AST.Id("Output"), AST.Id("printFloat"), [
                        AST.CallExpr(AST.SelfLiteral(), AST.Id("triangleArea"), [
                            AST.Id("a"),
                            AST.Id("b"),
                            AST.Id("c"),
                        ])
                    ]),
                ])),
            ]),
        ]))
        self._test(testcase, expect)



    # expression evaluation order
    def test_exp_eval_order_0(self):
        testcase = \
"""Class Program{
    main() {
        Return 1 + 2 * 3;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.BinaryOp(
                        "+",
                        AST.IntLiteral(1),
                        AST.BinaryOp(
                            "*",
                            AST.IntLiteral(2),
                            AST.IntLiteral(3)
                        )
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_exp_eval_order_1(self):
        testcase = \
"""Class Program{
    main() {
        Return 1 + 2 + 3;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.BinaryOp(
                        "+",
                        AST.BinaryOp(
                            "+",
                            AST.IntLiteral(1),
                            AST.IntLiteral(2)
                        ),
                        AST.IntLiteral(3),
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_exp_eval_order_1(self):
        testcase = \
"""Class Program{
    main() {
        Return 1 + 2 - 3 + 4;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.BinaryOp(
                        "+",
                        AST.BinaryOp(
                            "-",
                            AST.BinaryOp(
                                "+",
                                AST.IntLiteral(1),
                                AST.IntLiteral(2),
                            ),
                            AST.IntLiteral(3)
                        ),
                        AST.IntLiteral(4),
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_exp_eval_order_2(self):
        testcase = \
"""Class Program{
    main() {
        Return 1 + - 2;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.BinaryOp(
                        "+",
                        AST.IntLiteral(1),
                        AST.UnaryOp("-", AST.IntLiteral(2)),
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_exp_eval_order_3(self):
        testcase = \
"""Class Program{
    main() {
        Return Self.arr[1];
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.ArrayCell(
                        AST.FieldAccess(AST.SelfLiteral(), AST.Id("arr")),
                        [AST.IntLiteral(1)]
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_exp_eval_order_4(self):
        testcase = \
"""Class Program{
    main() {
        Return Program::$arr[1];
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.ArrayCell(
                        AST.FieldAccess(AST.Id("Program"), AST.Id("$arr")),
                        [AST.IntLiteral(1)]
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)

    def test_exp_eval_order_5(self):
        testcase = \
"""Class Program{
    main() {
        Return !True && !False || True;
    }
}"""
        expect = str(AST.Program([
            AST.ClassDecl(AST.Id("Program"), [
                AST.MethodDecl(AST.Instance(), AST.Id("main"), [], AST.Block([AST.Return(
                    AST.BinaryOp(
                        "||",
                        AST.BinaryOp(
                            "&&",
                            AST.UnaryOp("!", AST.BooleanLiteral(True)),
                            AST.UnaryOp("!", AST.BooleanLiteral(False)),
                        ),
                        AST.BooleanLiteral(True),
                    )
                )])),
            ]),
        ]))
        self._test(testcase, expect)


    
    def test_phong_1(self):
        input = """
            Class Phong{

            }
        """
        expect = "Program([ClassDecl(Id(Phong),[])])"
        self._test(input, expect)
    
    def test_phong_2(self):
        input = """
            Class Phong: Ngan {

            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[])])"
        self._test(input, expect)
        
    def test_phong_3(self):
        input = """
            Class Phong: Ngan {

            }
            Class Vinh:Phong {

            }
            Class Em{

            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[]),ClassDecl(Id(Vinh),Id(Phong),[]),ClassDecl(Id(Em),[])])"
        self._test(input, expect)
        
    def test_phong_4(self):
        input = """
        Class Phong
        {
            Val x, $y, z: Int;
            Var a: String;
            Var b: Float;
            Var c: Boolean;
            Var d: Array[Int, 1_23];
            Val e: Ngan;
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),IntType,None)),AttributeDecl(Static,ConstDecl(Id($y),IntType,None)),AttributeDecl(Instance,ConstDecl(Id(z),IntType,None)),AttributeDecl(Instance,VarDecl(Id(a),StringType)),AttributeDecl(Instance,VarDecl(Id(b),FloatType)),AttributeDecl(Instance,VarDecl(Id(c),BoolType)),AttributeDecl(Instance,VarDecl(Id(d),ArrayType(123,IntType))),AttributeDecl(Instance,ConstDecl(Id(e),ClassType(Id(Ngan)),NullLiteral()))])])"
        self._test(input, expect)
        
    def test_phong_5(self):
        input = """
        Class Phong
        {
            Val x, $y: Int = 1_2_3_4, 0xA_F;
            Var a, b: Float = 123. , .0e00123;
            Val c: Boolean = False;
            main() {

            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),IntType,IntLit(1234))),AttributeDecl(Static,ConstDecl(Id($y),IntType,IntLit(175))),AttributeDecl(Instance,VarDecl(Id(a),FloatType,FloatLit(123.0))),AttributeDecl(Instance,VarDecl(Id(b),FloatType,FloatLit(0.0))),AttributeDecl(Instance,ConstDecl(Id(c),BoolType,BooleanLit(False))),MethodDecl(Id(main),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_6(self):
        input = """
        Class Phong
        {
            Val _Ngan:Int = (2*3+((4-5)%8))/7;
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(_Ngan),IntType,BinaryOp(/,BinaryOp(+,BinaryOp(*,IntLit(2),IntLit(3)),BinaryOp(%,BinaryOp(-,IntLit(4),IntLit(5)),IntLit(8))),IntLit(7))))])])"
        self._test(input, expect)
        
    def test_phong_7(self):
        input = """
        Class Phong
        {
            foo() {}
            goo(x, y: Int; z: Float) {}
            $zoo() {}
            $qoo(x, y: Int) {}
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(foo),Instance,[],Block([])),MethodDecl(Id(goo),Instance,[param(Id(x),IntType),param(Id(y),IntType),param(Id(z),FloatType)],Block([])),MethodDecl(Id($zoo),Static,[],Block([])),MethodDecl(Id($qoo),Static,[param(Id(x),IntType),param(Id(y),IntType)],Block([]))])])"
        self._test(input, expect)

    def test_phong_8(self):
        input = """
        Class Phong
        {
            Constructor(a, b : Float; c: Ngan) {}
            Constructor() {}
            Destrucctor() {}
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(Constructor),Instance,[param(Id(a),FloatType),param(Id(b),FloatType),param(Id(c),ClassType(Id(Ngan)))],Block([])),MethodDecl(Id(Constructor),Instance,[],Block([])),MethodDecl(Id(Destrucctor),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_9(self):
        input = """
        Class Phong
        {  
            Val x:Float = 10 % 2 + .2E-10 * 012 +  0xAC + 8.98;
            Var y:Boolean =  (True||False)&&True||False; 
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),FloatType,BinaryOp(+,BinaryOp(+,BinaryOp(+,BinaryOp(%,IntLit(10),IntLit(2)),BinaryOp(*,FloatLit(2e-11),IntLit(10))),IntLit(172)),FloatLit(8.98)))),AttributeDecl(Instance,VarDecl(Id(y),BoolType,BinaryOp(||,BinaryOp(&&,BinaryOp(||,BooleanLit(True),BooleanLit(False)),BooleanLit(True)),BooleanLit(False))))])])"
        self._test(input, expect)
        
    def test_phong_10(self):
        input = """
        Class Phong
        {  
            Val x:Array[Int, 3] = Array(1+1-5*3, (8-9/3)%2, 1-1+0);
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),ArrayType(3,IntType),[BinaryOp(-,BinaryOp(+,IntLit(1),IntLit(1)),BinaryOp(*,IntLit(5),IntLit(3))),BinaryOp(%,BinaryOp(-,IntLit(8),BinaryOp(/,IntLit(9),IntLit(3))),IntLit(2)),BinaryOp(+,BinaryOp(-,IntLit(1),IntLit(1)),IntLit(0))]))])])"
        self._test(input, expect)

    def test_phong_11(self):
        input = """
        Class Phong
        {  
            Val x:Array[Int, 3] = Array(x,y,z);
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),ArrayType(3,IntType),[Id(x),Id(y),Id(z)]))])])"
        self._test(input, expect)
    
    def test_phong_12(self):
        input = """
        Class Phong
        {
            main() {
                a = 1_000 % 2 + .2E-10 * 01_2 +  0xA_B_C + 8.98;
                b = (1 - 1) * 2 / 2 / 2 + 8 % 3 + ---10 * !!!True&&False;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),BinaryOp(+,BinaryOp(+,BinaryOp(+,BinaryOp(%,IntLit(1000),IntLit(2)),BinaryOp(*,FloatLit(2e-11),IntLit(10))),IntLit(2748)),FloatLit(8.98))),AssignStmt(Id(b),BinaryOp(&&,BinaryOp(+,BinaryOp(+,BinaryOp(/,BinaryOp(/,BinaryOp(*,BinaryOp(-,IntLit(1),IntLit(1)),IntLit(2)),IntLit(2)),IntLit(2)),BinaryOp(%,IntLit(8),IntLit(3))),BinaryOp(*,UnaryOp(-,UnaryOp(-,UnaryOp(-,IntLit(10)))),UnaryOp(!,UnaryOp(!,UnaryOp(!,BooleanLit(True)))))),BooleanLit(False)))]))])])"
        self._test(input, expect)
        
    def test_phong_13(self):
        input = """
        Class Phong
        {
            Val x: String = "To" +. "Phong";
            main() {
                Val y: Int = 10;
                If(x == "Ngan") {
                    Var z : Boolean = !y && y > -10  || (y == 100);
                }
                Else {
                    Val t: Int = 10;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),StringType,BinaryOp(+.,StringLit(To),StringLit(Phong)))),MethodDecl(Id(main),Instance,[],Block([ConstDecl(Id(y),IntType,IntLit(10)),If(BinaryOp(==,Id(x),StringLit(Ngan)),Block([VarDecl(Id(z),BoolType,BinaryOp(>,BinaryOp(&&,UnaryOp(!,Id(y)),Id(y)),BinaryOp(||,UnaryOp(-,IntLit(10)),BinaryOp(==,Id(y),IntLit(100)))))]),Block([ConstDecl(Id(t),IntType,IntLit(10))]))]))])])"
        self._test(input, expect)
        
    def test_phong_14(self):
        input = """
        Class Phong
        {
            Val x: String = "To" +. "Phong";
            main() {
                Val y: Int = 10;
                If(x == "Ngan") {
                    Var z : Boolean = !y && y > -10  || (y == 100);
                }
                Elseif(x == "Phong" +. "Ngan") {
                    Break;
                }
                Else {
                    Continue;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),StringType,BinaryOp(+.,StringLit(To),StringLit(Phong)))),MethodDecl(Id(main),Instance,[],Block([ConstDecl(Id(y),IntType,IntLit(10)),If(BinaryOp(==,Id(x),StringLit(Ngan)),Block([VarDecl(Id(z),BoolType,BinaryOp(>,BinaryOp(&&,UnaryOp(!,Id(y)),Id(y)),BinaryOp(||,UnaryOp(-,IntLit(10)),BinaryOp(==,Id(y),IntLit(100)))))]),If(BinaryOp(+.,BinaryOp(==,Id(x),StringLit(Phong)),StringLit(Ngan)),Block([Break]),Block([Continue])))]))])])"
        self._test(input, expect)
        
    def test_phong_15(self):
        input = """
        Class Phong
        {
            main(){
                Val x:Float = 10 % 2 + .2E-10 * 012 +  0xAC + 8.98;
                Var y:Boolean =  (True||False)&&True||False; 
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([ConstDecl(Id(x),FloatType,BinaryOp(+,BinaryOp(+,BinaryOp(+,BinaryOp(%,IntLit(10),IntLit(2)),BinaryOp(*,FloatLit(2e-11),IntLit(10))),IntLit(172)),FloatLit(8.98))),VarDecl(Id(y),BoolType,BinaryOp(||,BinaryOp(&&,BinaryOp(||,BooleanLit(True),BooleanLit(False)),BooleanLit(True)),BooleanLit(False)))]))])])"
        self._test(input, expect)
        
    def test_phong_16(self):
        input = """
        Class Phong
        {
            main(){
                Val x:Float = a::$b.c + X.Y + K::$T;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([ConstDecl(Id(x),FloatType,BinaryOp(+,BinaryOp(+,FieldAccess(FieldAccess(Id(a),Id($b)),Id(c)),FieldAccess(Id(X),Id(Y))),FieldAccess(Id(K),Id($T))))]))])])"
        self._test(input, expect)
        
    def test_phong_17(self):
        input = """
            Class Phong{
                Var a, $b: Int = 222*2+(xyz.idm.jkl[153]), 2;
                Val Ngan:Float=A::$x;
            }
        """
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,VarDecl(Id(a),IntType,BinaryOp(+,BinaryOp(*,IntLit(222),IntLit(2)),ArrayCell(FieldAccess(FieldAccess(Id(xyz),Id(idm)),Id(jkl)),[IntLit(153)])))),AttributeDecl(Static,VarDecl(Id($b),IntType,IntLit(2))),AttributeDecl(Instance,ConstDecl(Id(Ngan),FloatType,FieldAccess(Id(A),Id($x))))])])"
        self._test(input, expect)
        
    def test_phong_18(self):
        input = """
        Class Phong
        {
            main() {
                a = x[1][2][3][4][5] + 10000 ;
                b = y[New A(1) + New B(2) + New C(3)][1.89];
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),BinaryOp(+,ArrayCell(Id(x),[IntLit(1),IntLit(2),IntLit(3),IntLit(4),IntLit(5)]),IntLit(10000))),AssignStmt(Id(b),ArrayCell(Id(y),[BinaryOp(+,BinaryOp(+,NewExpr(Id(A),[IntLit(1)]),NewExpr(Id(B),[IntLit(2)])),NewExpr(Id(C),[IntLit(3)])),FloatLit(1.89)]))]))])])"
        self._test(input, expect)
        
    def test_phong_19(self):
        input = """
        Class Phong
        {
            main() {
                a = x[0][1][2] + y[100] - z[Ngan::$yeuPhong];
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),BinaryOp(-,BinaryOp(+,ArrayCell(Id(x),[IntLit(0),IntLit(1),IntLit(2)]),ArrayCell(Id(y),[IntLit(100)])),ArrayCell(Id(z),[FieldAccess(Id(Ngan),Id($yeuPhong))])))]))])])"
        self._test(input, expect)
        
    def test_phong_20(self):
        input = """
        Class Phong
        {
            main() {
                a = x[y[z[0]]] + y[100];
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),BinaryOp(+,ArrayCell(Id(x),[ArrayCell(Id(y),[ArrayCell(Id(z),[IntLit(0)])])]),ArrayCell(Id(y),[IntLit(100)])))]))])])"
        self._test(input, expect)
        
    def test_phong_21(self):
        input = """
        Class Phong
        {
            main() {
                a = -x[A.getText(True||!False)+."Ngan"][B.getNum()-5+7];
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),UnaryOp(-,ArrayCell(Id(x),[BinaryOp(+.,CallExpr(Id(A),Id(getText),[BinaryOp(||,BooleanLit(True),UnaryOp(!,BooleanLit(False)))]),StringLit(Ngan)),BinaryOp(+,BinaryOp(-,CallExpr(Id(B),Id(getNum),[]),IntLit(5)),IntLit(7))])))]))])])"
        self._test(input, expect)
        
    def test_phong_22(self):
        input = """
        Class Phong
        {
            main() {
                a = x::$y.z.t;
                b = (x + 1 ).y.z.t;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),FieldAccess(FieldAccess(FieldAccess(Id(x),Id($y)),Id(z)),Id(t))),AssignStmt(Id(b),FieldAccess(FieldAccess(FieldAccess(BinaryOp(+,Id(x),IntLit(1)),Id(y)),Id(z)),Id(t)))]))])])"
        self._test(input, expect)
        
    def test_phong_23(self):
        input = """
        Class Phong
        {
            main() {
                x = New Ngan().yeuPhong;
                y = New Ngan().yeuPhong.yeuP;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),FieldAccess(NewExpr(Id(Ngan),[]),Id(yeuPhong))),AssignStmt(Id(y),FieldAccess(FieldAccess(NewExpr(Id(Ngan),[]),Id(yeuPhong)),Id(yeuP)))]))])])"
        self._test(input, expect)
        
    def test_phong_24(self):
        input = """
        Class Phong
        {
            main() {
                a = x.y().z.t();
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(a),CallExpr(FieldAccess(CallExpr(Id(x),Id(y),[]),Id(z)),Id(t),[]))]))])])"
        self._test(input, expect)
        
    def test_phong_25(self):
        input = """
        Class Phong
        {  
            Val x:Array[Int, 3] = Array(x+1+"To",y+2+"Thanh",z+3+"Phong"+."Ngan");
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),ArrayType(3,IntType),[BinaryOp(+,BinaryOp(+,Id(x),IntLit(1)),StringLit(To)),BinaryOp(+,BinaryOp(+,Id(y),IntLit(2)),StringLit(Thanh)),BinaryOp(+.,BinaryOp(+,BinaryOp(+,Id(z),IntLit(3)),StringLit(Phong)),StringLit(Ngan))]))])])"
        self._test(input, expect)
        
    def test_phong_26(self):
        input = """
        Class Phong
        {
            Var a: Array[Int, 0X1_2_3_4_5_A_F];
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(19088815,IntType)))])])"
        self._test(input, expect)

    def test_phong_27(self):
        input = """
        Class Phong
        {
            Var a: Array[Array[Int, 2], 2] = Array(Array(x, y),Array(0, 0));
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(2,ArrayType(2,IntType)),[[Id(x),Id(y)],[IntLit(0),IntLit(0)]]))])])"
        self._test(input, expect)
        
    def test_phong_28(self):
        input = """
        Class Phong
        {
            Var a: Array[Array[Array[Int, 1], 1], 2] = Array(Array(Array(10)),Array(Array(11)));
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(2,ArrayType(1,ArrayType(1,IntType))),[[[IntLit(10)]],[[IntLit(11)]]]))])])"
        self._test(input, expect)
        
    def test_phong_29(self):
        input = """
        Class Phong
        {
            Var a: Array[Float,2] = Array(1.01, 7_8_9_10.123456e78);
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(2,FloatType),[FloatLit(1.01),FloatLit(7.8910123456e+82)]))])])"
        self._test(input, expect)
        
    def test_phong_30(self):
        input = """
        Class Phong
        {
            Var a: Array[String,3] = Array("Ngan", "Phong", "PhongYeuNgan");
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(3,StringType),[StringLit(Ngan),StringLit(Phong),StringLit(PhongYeuNgan)]))])])"
        self._test(input, expect)
        
    def test_phong_31(self):
        input = """
        Class Phong
        {
            main(){
                If(3>2){
                    If(6>3){
                        If(True){
                            Break;
                        }
                    }
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([If(BinaryOp(>,IntLit(3),IntLit(2)),Block([If(BinaryOp(>,IntLit(6),IntLit(3)),Block([If(BooleanLit(True),Block([Break]))]))]))]))])])"
        self._test(input, expect)
        
    def test_phong_32(self):
        input = """
        Class Phong
        {
            main(){
                If(True){
                    If((1+1)*2-8/6%2==3){
                        Continue;
                    }
                    Else{
                        Break;
                    }
                }
                Elseif(1-8*8+x-y/2==6%2){
                    Var x:Int = 5;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([If(BooleanLit(True),Block([If(BinaryOp(==,BinaryOp(-,BinaryOp(*,BinaryOp(+,IntLit(1),IntLit(1)),IntLit(2)),BinaryOp(%,BinaryOp(/,IntLit(8),IntLit(6)),IntLit(2))),IntLit(3)),Block([Continue]),Block([Break]))]),If(BinaryOp(==,BinaryOp(-,BinaryOp(+,BinaryOp(-,IntLit(1),BinaryOp(*,IntLit(8),IntLit(8))),Id(x)),BinaryOp(/,Id(y),IntLit(2))),BinaryOp(%,IntLit(6),IntLit(2))),Block([VarDecl(Id(x),IntType,IntLit(5))])))]))])])"
        self._test(input, expect)
        
    def test_phong_33(self):
        input = """
        Class Phong
        {
            main(){
                If(True){
                    Foreach(x In 1 .. 100+2 By 2){
                        If(x==5){
                            x=Ngan.yeuPhong() + 5;
                        }
                        Else{
                            Continue;
                        }
                    }
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([If(BooleanLit(True),Block([For(Id(x),IntLit(1),BinaryOp(+,IntLit(100),IntLit(2)),IntLit(2),Block([If(BinaryOp(==,Id(x),IntLit(5)),Block([AssignStmt(Id(x),BinaryOp(+,CallExpr(Id(Ngan),Id(yeuPhong),[]),IntLit(5)))]),Block([Continue]))])])]))]))])])"
        self._test(input, expect)
        
    def test_phong_34(self):
        input = """
        Class Phong
        {
            main(){
                Return Ngan.yeuPhong();
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([Return(CallExpr(Id(Ngan),Id(yeuPhong),[]))]))])])"
        self._test(input, expect)
        
    def test_phong_35(self):
        input = """
        Class Phong
        {
            main() {
                Ngan[1+1-5] = 1+7-8;
                Self.x = 2*5%3;
                Ngan::$YeuPhong = 1212.115;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(ArrayCell(Id(Ngan),[BinaryOp(-,BinaryOp(+,IntLit(1),IntLit(1)),IntLit(5))]),BinaryOp(-,BinaryOp(+,IntLit(1),IntLit(7)),IntLit(8))),AssignStmt(FieldAccess(Self(),Id(x)),BinaryOp(%,BinaryOp(*,IntLit(2),IntLit(5)),IntLit(3))),AssignStmt(FieldAccess(Id(Ngan),Id($YeuPhong)),FloatLit(1212.115))]))])])"
        self._test(input, expect)

    def test_phong_36(self):
        input = """
        Class Phong
        {
            main() {
                x.a = 0.123;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(FieldAccess(Id(x),Id(a)),FloatLit(0.123))]))])])"
        self._test(input, expect)
        
    def test_phong_37(self):
        input = """
        Class Phong
        {
            main() {
                Foreach(x In start..end By x+5/8-9*3) {
                    Continue;
                }
                Foreach(x::$y In a + 9 .. b + 100) {
                    Break;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([For(Id(x),Id(start),Id(end),BinaryOp(-,BinaryOp(+,Id(x),BinaryOp(/,IntLit(5),IntLit(8))),BinaryOp(*,IntLit(9),IntLit(3))),Block([Continue])]),For(FieldAccess(Id(x),Id($y)),BinaryOp(+,Id(a),IntLit(9)),BinaryOp(+,Id(b),IntLit(100)),IntLit(1),Block([Break])])]))])])"
        self._test(input, expect)
        
    def test_phong_38(self):
        input = """
        Class Phong
        {
            main() {
                Return x.y.z();
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([Return(CallExpr(FieldAccess(Id(x),Id(y)),Id(z),[]))]))])])"
        self._test(input, expect)
        
    def test_phong_39(self):
        input = """
        Class Phong
        {
            main() {
                Return;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([Return()]))])])"
        self._test(input, expect)
        
    def test_phong_40(self):
        input = """
        Class Phong
        {
            main() {
                x = Ngan::$YeuPhong[1.04e45132 - 1_123_123 + -5];
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),ArrayCell(FieldAccess(Id(Ngan),Id($YeuPhong)),[BinaryOp(+,BinaryOp(-,FloatLit(inf),IntLit(1123123)),UnaryOp(-,IntLit(5)))]))]))])])"
        self._test(input, expect)
        
    def test_phong_41(self):
        input = """
        Class Phong
        {
            Constructor(x,y,z:Int){}
            Destructor(){}
            main(){}
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(Constructor),Instance,[param(Id(x),IntType),param(Id(y),IntType),param(Id(z),IntType)],Block([])),MethodDecl(Id(Destructor),Instance,[],Block([])),MethodDecl(Id(main),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_42(self):
        input = """
        Class Program
        {
            main(){
                If (True){
                    Var a: Int;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([If(BooleanLit(True),Block([VarDecl(Id(a),IntType)]))]))])])"
        self._test(input, expect)
        
    def test_phong_43(self):
        input = """
        Class Program : Phong
        {
            main(){
                If (a + b > c){
                    Var a: Int;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),Id(Phong),[MethodDecl(Id(main),Static,[],Block([If(BinaryOp(>,BinaryOp(+,Id(a),Id(b)),Id(c)),Block([VarDecl(Id(a),IntType)]))]))])])"
        self._test(input, expect)
        

    def test_phong_44(self):
        input = """
            Class Phong: Ngan {
                main() {
                    x = y +. z;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(+.,Id(y),Id(z)))]))])])"
        self._test(input, expect)

    def test_phong_45(self):
        input = """
            Class Phong: Ngan {
                main() {
                    x = z ==. t;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(==.,Id(z),Id(t)))]))])])"
        self._test(input, expect)


    def test_phong_46(self):
        input = """
            Class Phong: Ngan {
                main() { 
                    x = y <= z;
                    x = y >= z;
                    x = y < z;
                    x = y > z;
                }

            }

        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(<=,Id(y),Id(z))),AssignStmt(Id(x),BinaryOp(>=,Id(y),Id(z))),AssignStmt(Id(x),BinaryOp(<,Id(y),Id(z))),AssignStmt(Id(x),BinaryOp(>,Id(y),Id(z)))]))])])"
        self._test(input, expect)

    def test_phong_47(self):
        input = """
            Class Phong: Ngan {
                main() {    
                    x = y || z || t && x;
                    x = y && z && t && z;
                }

            }

        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(&&,BinaryOp(||,BinaryOp(||,Id(y),Id(z)),Id(t)),Id(x))),AssignStmt(Id(x),BinaryOp(&&,BinaryOp(&&,BinaryOp(&&,Id(y),Id(z)),Id(t)),Id(z)))]))])])"
        self._test(input, expect)

    def test_phong_48(self):
        input = """
            Class Program {
                main(){
                    Var a, b, c: Int = 1,2,3;
                    Val x, y, z: Int = 1,2,3;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,IntLit(1)),VarDecl(Id(b),IntType,IntLit(2)),VarDecl(Id(c),IntType,IntLit(3)),ConstDecl(Id(x),IntType,IntLit(1)),ConstDecl(Id(y),IntType,IntLit(2)),ConstDecl(Id(z),IntType,IntLit(3))]))])])"
        self._test(input, expect)
        
    def test_phong_49(self):
        input = """
            Class Phong{}
            Class Ngan{}
        """
        expect = "Program([ClassDecl(Id(Phong),[]),ClassDecl(Id(Ngan),[])])"
        self._test(input, expect)
        
    def test_phong_50(self):
        input = """
        Class ToThanhPhong
        {
            Val x, $y, z: Int;
        }"""
        expect = "Program([ClassDecl(Id(ToThanhPhong),[AttributeDecl(Instance,ConstDecl(Id(x),IntType,None)),AttributeDecl(Static,ConstDecl(Id($y),IntType,None)),AttributeDecl(Instance,ConstDecl(Id(z),IntType,None))])])"
        self._test(input, expect)
        
    def test_phong_51(self):
        input = """
        Class Phong
        {
            Val x, $y: Int = 1_2_3_4, 0xA_F;
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),IntType,IntLit(1234))),AttributeDecl(Static,ConstDecl(Id($y),IntType,IntLit(175)))])])"
        self._test(input, expect)
        
    def test_phong_52(self):
        input = """
        Class Phong
        {
            Val a:String = "Ngan";
            Var x: String = "Phong" +. "Ngan";
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(a),StringType,StringLit(Ngan))),AttributeDecl(Instance,VarDecl(Id(x),StringType,BinaryOp(+.,StringLit(Phong),StringLit(Ngan))))])])"
        self._test(input, expect)
        
    def test_phong_53(self):
        input = """
        Class Phong
        {
            Val x, $y, z: Int;
            Var a: String;
            Var b: Float;
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),IntType,None)),AttributeDecl(Static,ConstDecl(Id($y),IntType,None)),AttributeDecl(Instance,ConstDecl(Id(z),IntType,None)),AttributeDecl(Instance,VarDecl(Id(a),StringType)),AttributeDecl(Instance,VarDecl(Id(b),FloatType))])])"
        self._test(input, expect)
        
    def test_phong_54(self):
        input = """
        Class Phong
        {
            Val x , $y: Int = 1_2_3_4, 0xA_F;
            Var z: Float = 456.789;
        }"""
        expect = "Program([ClassDecl(Id(Phong),[AttributeDecl(Instance,ConstDecl(Id(x),IntType,IntLit(1234))),AttributeDecl(Static,ConstDecl(Id($y),IntType,IntLit(175))),AttributeDecl(Instance,VarDecl(Id(z),FloatType,FloatLit(456.789)))])])"
        self._test(input, expect)
        
    def test_phong_55(self):
        input = """
        Class Phong:Ngan
        {
            Val _Phong_:Float = (1>3)||True&&False;
            Var a: Array[Int,10];
        }"""
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[AttributeDecl(Instance,ConstDecl(Id(_Phong_),FloatType,BinaryOp(&&,BinaryOp(||,BinaryOp(>,IntLit(1),IntLit(3)),BooleanLit(True)),BooleanLit(False)))),AttributeDecl(Instance,VarDecl(Id(a),ArrayType(10,IntType)))])])"
        self._test(input, expect)
        
    def test_phong_56(self):
        input = """
        Class Phong:Ngan
        {
            Var a: Array[Int,1];
        }"""
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(1,IntType)))])])"
        self._test(input, expect)
        
    def test_phong_57(self):
        input = """
            Class Program {
                main() {    
                    Val a: Int = New Phong(x, y, z).c + d * e - (m == n) + a::$b - a::$b() - -a.b[0][a.b] + a ==. !c - New X().b.c.d() + a.b.c();
                }   
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(a),IntType,BinaryOp(==.,BinaryOp(+,BinaryOp(-,BinaryOp(-,BinaryOp(+,BinaryOp(-,BinaryOp(+,FieldAccess(NewExpr(Id(Phong),[Id(x),Id(y),Id(z)]),Id(c)),BinaryOp(*,Id(d),Id(e))),BinaryOp(==,Id(m),Id(n))),FieldAccess(Id(a),Id($b))),CallExpr(Id(a),Id($b),[])),UnaryOp(-,ArrayCell(FieldAccess(Id(a),Id(b)),[IntLit(0),FieldAccess(Id(a),Id(b))]))),Id(a)),BinaryOp(+,BinaryOp(-,UnaryOp(!,Id(c)),CallExpr(FieldAccess(FieldAccess(NewExpr(Id(X),[]),Id(b)),Id(c)),Id(d),[])),CallExpr(FieldAccess(Id(a),Id(b)),Id(c),[]))))]))])])"
        self._test(input, expect)

    def test_phong_58(self):
        input = """
        Class Phong
        {
            Constructor(a: Int) {}
            Destructor() {}
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(Constructor),Instance,[param(Id(a),IntType)],Block([])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_59(self):
        input = """
        Class Program
        {
            Val x: Array[Float, 3] = Array(1, 2, 3);
            main() {
                Val z : Int = A.x[0][1][2][3];
                z = New X();
                z.num = y.num;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,ConstDecl(Id(x),ArrayType(3,FloatType),[IntLit(1),IntLit(2),IntLit(3)])),MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(z),IntType,ArrayCell(FieldAccess(Id(A),Id(x)),[IntLit(0),IntLit(1),IntLit(2),IntLit(3)])),AssignStmt(Id(z),NewExpr(Id(X),[])),AssignStmt(FieldAccess(Id(z),Id(num)),FieldAccess(Id(y),Id(num)))]))])])"
        self._test(input, expect)

    def test_phong_60(self):
        input = """
        Class Program
        {
            main() {
                Var x : Car = New Car();
                Out.println(x.engine.fuel * Car::$sum);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(x),ClassType(Id(Car)),NewExpr(Id(Car),[])),Call(Id(Out),Id(println),[BinaryOp(*,FieldAccess(FieldAccess(Id(x),Id(engine)),Id(fuel)),FieldAccess(Id(Car),Id($sum)))])]))])])"
        self._test(input, expect)
        
    def test_phong_61(self):
        input = """
        Class Calculator
        {
            main(){
                window = New JFrame("Calculator");
                window.setSize(WINDOW_WIDTH, WINDOW_HEIGHT);
                window.setLocationRelativeTo(Null);
            }
        }
        """
        expect = "Program([ClassDecl(Id(Calculator),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(window),NewExpr(Id(JFrame),[StringLit(Calculator)])),Call(Id(window),Id(setSize),[Id(WINDOW_WIDTH),Id(WINDOW_HEIGHT)]),Call(Id(window),Id(setLocationRelativeTo),[NullLiteral()])]))])])"
        self._test(input, expect)

    def test_phong_62(self):
        input = """
        Class Phong
        {
            main() {
                Var x, y__y, z : Int;
                Var j: Float = 1.0;
            }
        }"""
        expect = "Program([ClassDecl(Id(Phong),[MethodDecl(Id(main),Instance,[],Block([VarDecl(Id(x),IntType),VarDecl(Id(y__y),IntType),VarDecl(Id(z),IntType),VarDecl(Id(j),FloatType,FloatLit(1.0))]))])])"
        self._test(input, expect)


    def test_phong_63(self):
        input = """
        Class Program
        {
            Var a, $b, c : Float;
            main() {
                Var x, z : Int;
            }
        }
        
        Class Phong : Program
        {
            $fact(num: Int) {
                If((num == 0) || (num == 1)){
                    Return 1;
                }
                Elseif(num == 0){
                    Return num * Program::$factorial(num - 1);
                }
                Else{
                    Return 0;
                }
            }
            main() {
                Out.println(Program::$fact(10));
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(a),FloatType)),AttributeDecl(Static,VarDecl(Id($b),FloatType)),AttributeDecl(Instance,VarDecl(Id(c),FloatType)),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(x),IntType),VarDecl(Id(z),IntType)]))]),ClassDecl(Id(Phong),Id(Program),[MethodDecl(Id($fact),Static,[param(Id(num),IntType)],Block([If(BinaryOp(||,BinaryOp(==,Id(num),IntLit(0)),BinaryOp(==,Id(num),IntLit(1))),Block([Return(IntLit(1))]),If(BinaryOp(==,Id(num),IntLit(0)),Block([Return(BinaryOp(*,Id(num),CallExpr(Id(Program),Id($factorial),[BinaryOp(-,Id(num),IntLit(1))])))]),Block([Return(IntLit(0))])))])),MethodDecl(Id(main),Instance,[],Block([Call(Id(Out),Id(println),[CallExpr(Id(Program),Id($fact),[IntLit(10)])])]))])])"
        self._test(input, expect)
        
    def test_phong_64(self):
        input = """
        Class Program
        {
            Var a, $b, c : Float;
            main() {
                Var x, z : Int;
            }
        }
        
        Class Phong : Program
        {
            $fact(num: Int) {
                If((num == 0) || (num == 1)){
                    Return 1;
                }
                Elseif(num == 0){
                    Return num * Program::$factorial(num - 1);
                }
                Else{
                    Return 0;
                }
            }
            main() {
                Out.println(Program::$fact(10));
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(a),FloatType)),AttributeDecl(Static,VarDecl(Id($b),FloatType)),AttributeDecl(Instance,VarDecl(Id(c),FloatType)),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(x),IntType),VarDecl(Id(z),IntType)]))]),ClassDecl(Id(Phong),Id(Program),[MethodDecl(Id($fact),Static,[param(Id(num),IntType)],Block([If(BinaryOp(||,BinaryOp(==,Id(num),IntLit(0)),BinaryOp(==,Id(num),IntLit(1))),Block([Return(IntLit(1))]),If(BinaryOp(==,Id(num),IntLit(0)),Block([Return(BinaryOp(*,Id(num),CallExpr(Id(Program),Id($factorial),[BinaryOp(-,Id(num),IntLit(1))])))]),Block([Return(IntLit(0))])))])),MethodDecl(Id(main),Instance,[],Block([Call(Id(Out),Id(println),[CallExpr(Id(Program),Id($fact),[IntLit(10)])])]))])])"
        self._test(input, expect)

    def test_phong_65(self):
        input = """
            Class Phong: Ngan {
                main() {    
                    x = y && z && t || c || r;
                }

            }

        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(||,BinaryOp(||,BinaryOp(&&,BinaryOp(&&,Id(y),Id(z)),Id(t)),Id(c)),Id(r)))]))])])"
        self._test(input, expect)

    def test_phong_66(self):
        input = """
            Class Phong: Ngan {
                main(a,b,c: Int; d,e,f: Float) {    
                    a = ab.b.c.d.e.f;
                    a = a.b().c().d().e;
                }

            }

        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[param(Id(a),IntType),param(Id(b),IntType),param(Id(c),IntType),param(Id(d),FloatType),param(Id(e),FloatType),param(Id(f),FloatType)],Block([AssignStmt(Id(a),FieldAccess(FieldAccess(FieldAccess(FieldAccess(FieldAccess(Id(ab),Id(b)),Id(c)),Id(d)),Id(e)),Id(f))),AssignStmt(Id(a),FieldAccess(CallExpr(CallExpr(CallExpr(Id(a),Id(b),[]),Id(c),[]),Id(d),[]),Id(e)))]))])])"
        self._test(input, expect)

    def test_phong_67(self):
        input = """
            Class Phong: Ngan {
                main(a,b,c: Int; d,e,f: Float) {   
                    x = New Ngan();
                    y = New Ngan(a, b, c);
                }   

            }

        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[param(Id(a),IntType),param(Id(b),IntType),param(Id(c),IntType),param(Id(d),FloatType),param(Id(e),FloatType),param(Id(f),FloatType)],Block([AssignStmt(Id(x),NewExpr(Id(Ngan),[])),AssignStmt(Id(y),NewExpr(Id(Ngan),[Id(a),Id(b),Id(c)]))]))])])"
        self._test(input, expect)
        
    def test_phong_68(self):
        input = """
        Class Phong:Ngan
        {
            Var a: Array[Int,1];
        }"""
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(1,IntType)))])])"
        self._test(input, expect)
        
    def test_phong_69(self):
        input = """
        Class Phong:Ngan
        {
            Var a: Array[Int,0123];
        }"""
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(83,IntType)))])])"
        self._test(input, expect)
        
    def test_phong_70(self):
        input = """
        Class Phong:Ngan
        {
            Var a: Array[Int,0xAFF];
        }"""
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(2815,IntType)))])])"
        self._test(input, expect)
        
    def test_phong_71(self):
        input = """
        Class Phong:Ngan
        {
            Var a: Array[Int,0b1011];
        }"""
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[AttributeDecl(Instance,VarDecl(Id(a),ArrayType(11,IntType)))])])"
        self._test(input, expect)


    def test_phong_72(self):
        input = """
            Class Phong: Ngan {
                main() {    
                    x = y + z && t - r || a * b + c / d || e % k;
                }   
            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(||,BinaryOp(||,BinaryOp(&&,BinaryOp(+,Id(y),Id(z)),BinaryOp(-,Id(t),Id(r))),BinaryOp(+,BinaryOp(*,Id(a),Id(b)),BinaryOp(/,Id(c),Id(d)))),BinaryOp(%,Id(e),Id(k))))]))])])"
        self._test(input, expect)

    def test_phong_73(self):
        input = """
            Class Phong:Ngan {
                main() {    
                    x = y * !z * t / !!g % k + !h - !!!i % m;
                }   
            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(-,BinaryOp(+,BinaryOp(%,BinaryOp(/,BinaryOp(*,BinaryOp(*,Id(y),UnaryOp(!,Id(z))),Id(t)),UnaryOp(!,UnaryOp(!,Id(g)))),Id(k)),UnaryOp(!,Id(h))),BinaryOp(%,UnaryOp(!,UnaryOp(!,UnaryOp(!,Id(i)))),Id(m))))]))])])"
        self._test(input, expect)

    def test_phong_74(self):
        input = """
            Class Phong : Ngan {
                main() {    
                    x = !y - z[0x86][1_2_3] + t[0b1011][0123] * m[0][a+b+c];
                }   
            }

        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(x),BinaryOp(+,BinaryOp(-,UnaryOp(!,Id(y)),ArrayCell(Id(z),[IntLit(134),IntLit(123)])),BinaryOp(*,ArrayCell(Id(t),[IntLit(11),IntLit(83)]),ArrayCell(Id(m),[IntLit(0),BinaryOp(+,BinaryOp(+,Id(a),Id(b)),Id(c))]))))]))])])"
        self._test(input, expect)
        
    def test_phong_75(self):
        input = """
        Class Program{
            Var x : Array[String, 1];
            Var y : Array[Array[Int, 10], 20];
            Var z : Array[Array[Array[Int, 123], 213], 331];
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(x),ArrayType(1,StringType))),AttributeDecl(Instance,VarDecl(Id(y),ArrayType(20,ArrayType(10,IntType)))),AttributeDecl(Instance,VarDecl(Id(z),ArrayType(331,ArrayType(213,ArrayType(123,IntType)))))])])"
        self._test(input, expect)
        
    def test_phong_76(self):
        input = """
        Class Program{
            main(args: Array[String, 10]) {}
            foo(a, b: String){
                Return a == b;
            }
            Constructor() {}
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Instance,[param(Id(args),ArrayType(10,StringType))],Block([])),MethodDecl(Id(foo),Instance,[param(Id(a),StringType),param(Id(b),StringType)],Block([Return(BinaryOp(==,Id(a),Id(b)))])),MethodDecl(Id(Constructor),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_77(self):
        input = """
        Class Program{
            main(args: Array[String, 10]) {}
            foo(a, b: String){
                Return a == b;
            }
            Constructor() {}
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Instance,[param(Id(args),ArrayType(10,StringType))],Block([])),MethodDecl(Id(foo),Instance,[param(Id(a),StringType),param(Id(b),StringType)],Block([Return(BinaryOp(==,Id(a),Id(b)))])),MethodDecl(Id(Constructor),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_78(self):
        input = """
        Class Program{
            main() {
                Foreach(i In 1 .. 100 By 2){
                    If(x + 2 == 3){
                        Break;
                    }
                    Else{
                        Continue;
                    }
                }
                Return x + y;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),IntLit(1),IntLit(100),IntLit(2),Block([If(BinaryOp(==,BinaryOp(+,Id(x),IntLit(2)),IntLit(3)),Block([Break]),Block([Continue]))])]),Return(BinaryOp(+,Id(x),Id(y)))]))])])"
        self._test(input, expect)


    def test_phong_79(self):
        input = """
            Class Phong: Ngan {
                main() {    
                    Var x:Ngan = Null;
                    If(x == Null){
                        x = New Ngan();
                    }
                    Else{
                        Return x;
                    }
                }   

            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(main),Instance,[],Block([VarDecl(Id(x),ClassType(Id(Ngan)),NullLiteral()),If(BinaryOp(==,Id(x),NullLiteral()),Block([AssignStmt(Id(x),NewExpr(Id(Ngan),[]))]),Block([Return(Id(x))]))]))])])"
        self._test(input, expect)

    def test_phong_80(self):
        input = """
            Class Phong: Ngan {
                Constructor() {
                }
                Destructor() {
                }
            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(Constructor),Instance,[],Block([])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])"
        self._test(input, expect)
        
    def test_phong_81(self):
        input = """
            Class Phong: Ngan {
                Constructor() {
                }
                main() {
                    y = New X();
                    Return 0;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[MethodDecl(Id(Constructor),Instance,[],Block([])),MethodDecl(Id(main),Instance,[],Block([AssignStmt(Id(y),NewExpr(Id(X),[])),Return(IntLit(0))]))])])"
        self._test(input, expect)

    def test_phong_82(self):
        input = """
            Class Program {
                main() {
                    Return 0;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Return(IntLit(0))]))])])"
        self._test(input, expect)

    def test_phong_83(self):
        input = """
            Class Program {
                $getString(x: String) {
                    Return x;
                }
                $upperCase(y: String) {
                    Return y;
                }
            }

        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id($getString),Static,[param(Id(x),StringType)],Block([Return(Id(x))])),MethodDecl(Id($upperCase),Static,[param(Id(y),StringType)],Block([Return(Id(y))]))])])"
        self._test(input, expect)
        
    def test_phong_84(self):
        input = """
            Class Program {
                getString(x: String) {
                    Return x;
                }
                upperCase(y: String) {
                    Return y;
                }
            }

        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(getString),Instance,[param(Id(x),StringType)],Block([Return(Id(x))])),MethodDecl(Id(upperCase),Instance,[param(Id(y),StringType)],Block([Return(Id(y))]))])])"
        self._test(input, expect)

    def test_phong_85(self):
        input = """
        Class Program {
            removeDuplicates(S : String){
                ## TODO ##
                Var st : Stack;
                Foreach(i In 0 .. S.length() By 2){
                    If(!st.empty()) {
                        st.push_back(S[i]);
                    }
                    Elseif(st.top() == S[i]){
                        st.pop_back();
                    }
                    Else{
                        st.push(S[i]);
                    } 
                }
                Return st.top();
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(removeDuplicates),Instance,[param(Id(S),StringType)],Block([VarDecl(Id(st),ClassType(Id(Stack)),NullLiteral()),For(Id(i),IntLit(0),CallExpr(Id(S),Id(length),[]),IntLit(2),Block([If(UnaryOp(!,CallExpr(Id(st),Id(empty),[])),Block([Call(Id(st),Id(push_back),[ArrayCell(Id(S),[Id(i)])])]),If(BinaryOp(==,CallExpr(Id(st),Id(top),[]),ArrayCell(Id(S),[Id(i)])),Block([Call(Id(st),Id(pop_back),[])]),Block([Call(Id(st),Id(push),[ArrayCell(Id(S),[Id(i)])])])))])]),Return(CallExpr(Id(st),Id(top),[]))]))])])"
        self._test(input, expect)

    def test_phong_86(self):
        input = """
            Class Program {
                main(x: Boolean) {
                    Val a, b: Int;
                }

            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Instance,[param(Id(x),BoolType)],Block([ConstDecl(Id(a),IntType,None),ConstDecl(Id(b),IntType,None)]))])])"
        self._test(input, expect)

    def test_phong_87(self):
        input = """
            Class Program {
                main(x: Boolean) {
                    Val a, b: Int = 1, 2;
                    Val x, y: String = Array(1, "abc", 0x54) + 2, a.b.c();
                }
            }

        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Instance,[param(Id(x),BoolType)],Block([ConstDecl(Id(a),IntType,IntLit(1)),ConstDecl(Id(b),IntType,IntLit(2)),ConstDecl(Id(x),StringType,BinaryOp(+,[IntLit(1),StringLit(abc),IntLit(84)],IntLit(2))),ConstDecl(Id(y),StringType,CallExpr(FieldAccess(Id(a),Id(b)),Id(c),[]))]))])])"
        self._test(input, expect)

    def test_phong_88(self):
        input = """
            Class Program {
                main(x: Boolean) {
                    If (x + y + z >= 2) {
                        res = x+y+z;
                    }
                    Elseif (x % 2 == 0) {
                        Return 0;
                    }     
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Instance,[param(Id(x),BoolType)],Block([If(BinaryOp(>=,BinaryOp(+,BinaryOp(+,Id(x),Id(y)),Id(z)),IntLit(2)),Block([AssignStmt(Id(res),BinaryOp(+,BinaryOp(+,Id(x),Id(y)),Id(z)))]),If(BinaryOp(==,BinaryOp(%,Id(x),IntLit(2)),IntLit(0)),Block([Return(IntLit(0))])))]))])])"
        self._test(input, expect)

    def test_phong_89(self):
        input = """
            Class Program {
                main() {
                    If (x == y) {
                        c = d * f;
                    }
                    Elseif (x != y) {
                        a = b[0] + 1;
                    }
                    Elseif ((c + d) % 5 == 0) {
                        a = b[c+d][z][0x86] + 1;
                    }
                    Else {
                        c = c + b.d;
                    }       
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([If(BinaryOp(==,Id(x),Id(y)),Block([AssignStmt(Id(c),BinaryOp(*,Id(d),Id(f)))]),If(BinaryOp(!=,Id(x),Id(y)),Block([AssignStmt(Id(a),BinaryOp(+,ArrayCell(Id(b),[IntLit(0)]),IntLit(1)))]),If(BinaryOp(==,BinaryOp(%,BinaryOp(+,Id(c),Id(d)),IntLit(5)),IntLit(0)),Block([AssignStmt(Id(a),BinaryOp(+,ArrayCell(Id(b),[BinaryOp(+,Id(c),Id(d)),Id(z),IntLit(134)]),IntLit(1)))]),Block([AssignStmt(Id(c),BinaryOp(+,Id(c),FieldAccess(Id(b),Id(d))))]))))]))])])"
        self._test(input, expect)

    def test_phong_90(self):
        input = """
            Class Program {
                Val a: Ngan;
                main() {
                    
                    Foreach (i In a + b .. c[0] + d * c - a::$b() By i) {
                        a[0][1] = New A(a, b).c() + 1e10 - !(m == n) + a::$b - a::$b() - -a.b[0][a.b] + x % y - z;
                    }
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,ConstDecl(Id(a),ClassType(Id(Ngan)),NullLiteral())),MethodDecl(Id(main),Static,[],Block([For(Id(i),BinaryOp(+,Id(a),Id(b)),BinaryOp(-,BinaryOp(+,ArrayCell(Id(c),[IntLit(0)]),BinaryOp(*,Id(d),Id(c))),CallExpr(Id(a),Id($b),[])),Id(i),Block([AssignStmt(ArrayCell(Id(a),[IntLit(0),IntLit(1)]),BinaryOp(-,BinaryOp(+,BinaryOp(-,BinaryOp(-,BinaryOp(+,BinaryOp(-,BinaryOp(+,CallExpr(NewExpr(Id(A),[Id(a),Id(b)]),Id(c),[]),FloatLit(10000000000.0)),UnaryOp(!,BinaryOp(==,Id(m),Id(n)))),FieldAccess(Id(a),Id($b))),CallExpr(Id(a),Id($b),[])),UnaryOp(-,ArrayCell(FieldAccess(Id(a),Id(b)),[IntLit(0),FieldAccess(Id(a),Id(b))]))),BinaryOp(%,Id(x),Id(y))),Id(z)))])])]))])])"
        self._test(input, expect)
        
    def test_phong_91(self):
        input = """
        Class Ngan {
            Constructor(x:Phong){
                Return x;
            }
            Destructor(){
                Sys.Print("Destroy");
            }
        }
        Class Program {
            main() {
                If(x != "") {
                    a = New Ngan();
                    Return a;
                }
                Else{
                    Return a;
                }
            }
        }
        """
        expect = "Program([ClassDecl(Id(Ngan),[MethodDecl(Id(Constructor),Instance,[param(Id(x),ClassType(Id(Phong)))],Block([Return(Id(x))])),MethodDecl(Id(Destructor),Instance,[],Block([Call(Id(Sys),Id(Print),[StringLit(Destroy)])]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([If(BinaryOp(!=,Id(x),StringLit()),Block([AssignStmt(Id(a),NewExpr(Id(Ngan),[])),Return(Id(a))]),Block([Return(Id(a))]))]))])])"
        self._test(input, expect)

    def test_phong_92(self):

        input = """
        Class Phong : Ngan {}
        Class Ba : Me {}
        """
        expect = "Program([ClassDecl(Id(Phong),Id(Ngan),[]),ClassDecl(Id(Ba),Id(Me),[])])"
        self._test(input, expect)
        
    def test_phong_93(self):

        input = """
        Class Program {
            main() {
                x[0][a+b][0b11] = y[2] + 3;
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(ArrayCell(Id(x),[IntLit(0),BinaryOp(+,Id(a),Id(b)),IntLit(3)]),BinaryOp(+,ArrayCell(Id(y),[IntLit(2)]),IntLit(3)))]))])])"
        self._test(input, expect)
        
    def test_phong_94(self):

        input = """
        Class Program {
            main() {
                If(True){
                    Break;
                }
                Else{
                    Continue;
                }
                Return;
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([If(BooleanLit(True),Block([Break]),Block([Continue])),Return()]))])])"
        self._test(input, expect)

    def test_phong_95(self):
        input = """
        Class Program
        {
            main() {
                Var m : Array[Int, 10];
                Foreach (i In (0)..ARRAY_SIZE By 1) {
                    If (utility.rand() % 2 == 0) {
                        m[i] = Utility.mem_alloc(size+1);
                        If (m[i] != Null && True || False) {
                            i = index + 1;
                        }
                        Break;
                    }
                    Else{
                        If (i == 0) {
                            Continue;
                        }
                    }
                }
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(m),ArrayType(10,IntType)),For(Id(i),IntLit(0),Id(ARRAY_SIZE),IntLit(1),Block([If(BinaryOp(==,BinaryOp(%,CallExpr(Id(utility),Id(rand),[]),IntLit(2)),IntLit(0)),Block([AssignStmt(ArrayCell(Id(m),[Id(i)]),CallExpr(Id(Utility),Id(mem_alloc),[BinaryOp(+,Id(size),IntLit(1))])),If(BinaryOp(!=,ArrayCell(Id(m),[Id(i)]),BinaryOp(||,BinaryOp(&&,NullLiteral(),BooleanLit(True)),BooleanLit(False))),Block([AssignStmt(Id(i),BinaryOp(+,Id(index),IntLit(1)))])),Break]),Block([If(BinaryOp(==,Id(i),IntLit(0)),Block([Continue]))]))])])]))])])"
        self._test(input, expect)
        
    def test_phong_96(self):
        input = """
        Class Program
        {
            Val x: Array[Int, 3] = Array(1, 2, 3);
            main() {
                Val z : Int = Self.x[0+1][1%2][2-3][3*5/6+7];
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,ConstDecl(Id(x),ArrayType(3,IntType),[IntLit(1),IntLit(2),IntLit(3)])),MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(z),IntType,ArrayCell(FieldAccess(Self(),Id(x)),[BinaryOp(+,IntLit(0),IntLit(1)),BinaryOp(%,IntLit(1),IntLit(2)),BinaryOp(-,IntLit(2),IntLit(3)),BinaryOp(+,BinaryOp(/,BinaryOp(*,IntLit(3),IntLit(5)),IntLit(6)),IntLit(7))]))]))])])"
        self._test(input, expect)

    def test_phong_97(self):
        input = """
            Class Program {
                main() {
                    Foreach (i In 0 .. 100) {
                        Continue;
                    }
                    Return 0;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),IntLit(0),IntLit(100),IntLit(1),Block([Continue])]),Return(IntLit(0))]))])])"
        self._test(input, expect)

    def test_phong_98(self):
        input = """
            Class Program {
                main() {
                    Foreach (i In 0 .. 100) {
                        Break;
                    }
                    Return 0;
                }
            }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),IntLit(0),IntLit(100),IntLit(1),Block([Break])]),Return(IntLit(0))]))])])"
        self._test(input, expect)
        
    def test_phong_99(self):
        input = """Class Program{
            Var i: Int;
            Var $static: Int;
               
            main(){
                Var a:Int = Self.init();
               }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(i),IntType)),AttributeDecl(Static,VarDecl(Id($static),IntType)),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,CallExpr(Self(),Id(init),[]))]))])])"
        self._test(input, expect)
        
    def test_phong_100(self):
        input = """
        Class Program
        {
            main() {
                Var sum : Int = 0;
                Var i : Int = 0;
                Foreach(i In 1 .. 10 By (a + 5 - 6 * 7 /10)%2) {
                    sum = sum + i;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(sum),IntType,IntLit(0)),VarDecl(Id(i),IntType,IntLit(0)),For(Id(i),IntLit(1),IntLit(10),BinaryOp(%,BinaryOp(-,BinaryOp(+,Id(a),IntLit(5)),BinaryOp(/,BinaryOp(*,IntLit(6),IntLit(7)),IntLit(10))),IntLit(2)),Block([AssignStmt(Id(sum),BinaryOp(+,Id(sum),Id(i)))])])]))])])"
        self._test(input, expect)
