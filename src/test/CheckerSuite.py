import unittest
from TestUtils import TestChecker
import StaticError as SE
from AST import *


def write_wrong_answer(expect, num):
    from pathlib import Path
    Path('./test/WAs/').mkdir(parents=True, exist_ok=True)
    path = './test/WAs/' + str(num) + '.txt'
    with open(path, 'w+') as f:
        testcase = open('./test/testcases/' + str(num) + '.txt').read()
        solution = open('./test/solutions/' + str(num) + '.txt').read()
        f.write('\n-----------------------------------TESTCASE----------------------------------\n')
        f.write(testcase)
        f.write('\n-----------------------------------EXPECT------------------------------------\n')
        f.write(expect)
        f.write('\n-----------------------------------GOT---------------------------------------\n')
        f.write(solution)


class CheckerSuite(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        CheckerSuite.counter = 3999

    def _test(self, testcase, expect):
        CheckerSuite.counter += 1
        try:
            self.assertTrue(TestChecker.test(testcase, expect, CheckerSuite.counter))
        except AssertionError:
            write_wrong_answer(expect, self.counter)
            raise AssertionError(f"checker failed at test {CheckerSuite.counter}")

    # sample test from BKeL
    def test_sample_0(self):
        testcase = \
Program(
    [
        ClassDecl(
            Id("Program"),
            [
                MethodDecl(
                    Static(),
                    Id("main"),
                    [],
                    Block([])
                ),
                AttributeDecl(
                    Instance(),
                    VarDecl(
                        Id("myVar"),
                        StringType(),
                        StringLiteral("Hello World")
                    )
                ),
                AttributeDecl(
                    Instance(),
                    VarDecl(
                        Id("myVar"),
                        IntType()
                    )
                )
            ]
        )
    ]
)
        expect = "Redeclared Attribute: myVar"
        self._test(testcase, expect)

    def test_sample_1(self):
        testcase = \
Program(
    [
        ClassDecl(
            Id("Program"),
            [
                MethodDecl(
                    Static(),
                    Id("main"),
                    [],
                    Block(
                        [
                            Assign(
                                Id("myVar"),
                                IntLiteral(10)
                            )
                        ]
                    )
                )
            ]
        )
    ]
)
        expect = "Undeclared Identifier: myVar"
        self._test(testcase, expect)

    def test_sample_2(self):
        testcase = \
Program(
    [
        ClassDecl(
            Id("Program"),
            [
                MethodDecl(
                    Static(),
                    Id("main"),
                    [],
                    Block([
                        ConstDecl(
                            Id("myVar"),
                            IntType(),
                            IntLiteral(5)
                        ),
                        Assign(
                            Id("myVar"),
                            IntLiteral(10)
                        )]
                    )
                )
            ]
        )
    ]
)
        expect = "Cannot Assign To Constant: AssignStmt(Id(myVar),IntLit(10))"
        self._test(testcase, expect)

    def test_sample_3(self):
        testcase = \
Program(
    [
        ClassDecl(
            Id("Program"),
            [
                MethodDecl(
                    Static(),
                    Id("main"),
                    [],
                    Block(
                        [
                            Break()
                        ]
                    )
                )
            ]
        )
    ]
)
        expect = "Break Not In Loop"
        self._test(testcase, expect)

    def test_sample_4(self):
        testcase = \
Program(
    [
        ClassDecl(
            Id("Program"),
            [
                MethodDecl(
                    Static(),
                    Id("main"),
                    [],
                    Block(
                        [
                            ConstDecl(
                                Id("myVar"),
                                IntType(),
                                FloatLiteral(1.2)
                            )
                        ]
                    )
                )
            ]
        )
    ]
)
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(myVar),IntType,FloatLit(1.2))"
        self._test(testcase, expect)



    def test_type_coercion_0(self):
        stmt = VarDecl(
            Id("a"),
            ArrayType(3, FloatType()),
            ArrayLiteral([FloatLiteral(0), FloatLiteral(1)])
        )
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [],
                Block([stmt])
            )
        ]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)



    def test_array_literal_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [],
                Block([
                    VarDecl(
                        Id("a"),
                        ArrayType(3, IntType()),
                        ArrayLiteral([
                            IntLiteral(0),
                            IntLiteral(1),
                            FloatLiteral(1),
                        ])
                    )
                ])
            )
        ]
    )
])
        expect = str(SE.IllegalArrayLiteral(
            ArrayLiteral([
                IntLiteral(0),
                IntLiteral(1),
                FloatLiteral(1),
            ])
        ))
        self._test(testcase, expect)

    def test_array_literal_1(self):
        array_literal = ArrayLiteral([
            ArrayLiteral([IntLiteral(0), IntLiteral(1), IntLiteral(2)]),
            ArrayLiteral([IntLiteral(3), IntLiteral(4), IntLiteral(5)]),
            ArrayLiteral([IntLiteral(6), IntLiteral(7)]),
        ])
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [],
                Block([
                    VarDecl(
                        Id("a"),
                        ArrayType(3, ArrayType(3, IntType())),
                        array_literal
                    )
                ])
            )
        ]
    )
])
        expect = str(SE.IllegalArrayLiteral(array_literal))
        self._test(testcase, expect)

    def test_array_literal_2(self):
        array_literal = ArrayLiteral([
            ArrayLiteral([IntLiteral(0), IntLiteral(1), IntLiteral(2)]),
            ArrayLiteral([IntLiteral(3), IntLiteral(4), IntLiteral(5)]),
            ArrayLiteral([IntLiteral(6), IntLiteral(7), Id("x")]),
        ])
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [],
                Block([
                    VarDecl(Id("x"), FloatType(), FloatLiteral(8)),
                    VarDecl(
                        Id("a"),
                        ArrayType(3, ArrayType(3, IntType())),
                        array_literal
                    )
                ])
            )
        ]
    )
])
        expect = str(SE.IllegalArrayLiteral(array_literal))
        self._test(testcase, expect)

    def test_array_literal_3(self):
        array_literal = ArrayLiteral([IntLiteral(6), IntLiteral(7), Id("x")])
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [],
                Block([
                    VarDecl(Id("x"), FloatType(), FloatLiteral(8)),
                    VarDecl(Id("a"), ArrayType(3, IntType()), array_literal)
                ])
            )
        ]
    )
])
        expect = str(SE.IllegalArrayLiteral(array_literal))
        self._test(testcase, expect)

    def test_array_literal_4(self):
        array_literal = ArrayLiteral([
            NewExpr(Id("A"), []),
            NewExpr(Id("B"), []),
            NewExpr(Id("A"), []),
        ])
        testcase = \
Program([
    ClassDecl(Id('A'), []),
    ClassDecl(Id('B'), []),
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [],
                Block([
                    VarDecl(Id("a"), ArrayType(3, ClassType(Id("A"))), array_literal)
                ])
            )
        ]
    )
])
        expect = str(SE.IllegalArrayLiteral(array_literal))
        self._test(testcase, expect)


    def test_field_access_0(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1)))
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("y"), IntType(), FieldAccess(Id("A"), Id("$att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_field_access_1(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("a"), Id("att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_field_access_2(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("a"), Id("$att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.IllegalMemberAccess(FieldAccess(Id("a"), Id("$att"))))
        self._test(testcase, expect)

    def test_field_access_3(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("A"), Id("att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.IllegalMemberAccess(FieldAccess(Id("A"), Id("att"))))
        self._test(testcase, expect)

    def test_field_access_4(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(Id("B"), []),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("b"), ClassType(Id("B"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("b"), Id("att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.Undeclared(SE.Attribute(), "att"))
        self._test(testcase, expect)

    def test_field_access_5(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(Id("B"), []),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("b"), ClassType(Id("B"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("B"), Id("$att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.Undeclared(SE.Attribute(), "$att"))
        self._test(testcase, expect)

    def test_field_access_6(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(Id("B"), []),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("b"), ClassType(Id("B"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("c"), Id("att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.Undeclared(SE.Identifier(), "c"))
        self._test(testcase, expect)

    def test_field_access_5(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(Id("B"), []),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                VarDecl(Id("b"), ClassType(Id("B"))),
                VarDecl(Id("y"), IntType(), FieldAccess(Id("C"), Id("$att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.Undeclared(SE.Class(), "C"))
        self._test(testcase, expect)



    def test_var_decl_0(self):
        stmt = VarDecl(Id("a"), IntType(), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                stmt,
            ])),
        ])
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_var_decl_1(self):
        stmt = VarDecl(Id("a"), FloatType(), IntLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                stmt,
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_var_decl_2(self):
        stmt = VarDecl(Id("a"), FloatType())
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                stmt,
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)


    def test_const_decl_0(self):
        stmt = ConstDecl(Id("a"), IntType(), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                stmt,
            ])),
        ])
])
        expect = str(SE.TypeMismatchInConstant(stmt))
        self._test(testcase, expect)

    def test_const_decl_1(self):
        stmt = ConstDecl(Id("a"), IntType(), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                ConstDecl(Id("a"), FloatType(), IntLiteral(1)),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_const_decl_2(self):
        stmt = ConstDecl(Id("a"), IntType(), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                ConstDecl(Id("a"), ArrayType(2, FloatType()), ArrayLiteral([IntLiteral(1), IntLiteral(2)])),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_const_decl_3(self):
        stmt = ConstDecl(Id("a"), ArrayType(3, FloatType()), ArrayLiteral([IntLiteral(1), IntLiteral(2)]))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                stmt
            ])),
        ])
])
        expect = str(SE.TypeMismatchInConstant(stmt))
        self._test(testcase, expect)

    def test_const_decl_4(self):
        stmt = ConstDecl(Id("a"), IntType())
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                stmt
            ])),
        ])
])
        expect = str(SE.IllegalConstantExpression(None))
        self._test(testcase, expect)

    def test_const_decl_5(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                ConstDecl(Id("x"), IntType(), IntLiteral(1)),
                ConstDecl(Id("y"), IntType(), UnaryOp("-", Id("x"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_const_decl_6(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                ConstDecl(Id("x"), IntType(), IntLiteral(1)),
                ConstDecl(Id("y"), IntType(), BinaryOp("+", Id("x"), Id("x"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_const_decl_7(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("x"), IntType(), IntLiteral(1)),
                ConstDecl(Id("y"), IntType(), Id('x')),
            ])),
        ])
])
        expect = str(SE.IllegalConstantExpression(Id('x')))
        self._test(testcase, expect)

    def test_const_decl_8(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("x"), IntType(), IntLiteral(1)),
                ConstDecl(Id("z"), IntType(), IntLiteral(1)),
                ConstDecl(Id("y"), IntType(), BinaryOp('-', Id('x'), Id('z'))),
            ])),
        ])
])
        expect = str(SE.IllegalConstantExpression(BinaryOp('-', Id('x'), Id('z'))))
        self._test(testcase, expect)

    def test_const_decl_9(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                ConstDecl(Id("y"), IntType(), CallExpr(Id("A"), Id("$func"), [])),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_const_decl_10(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1)))
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                ConstDecl(Id("y"), IntType(), FieldAccess(Id("A"), Id("$att"))),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_const_decl_10(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        MethodDecl(Instance(), Id("func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("A"))),
                ConstDecl(Id("y"), IntType(), BinaryOp(
                    '*',
                    FieldAccess(Id("A"), Id("$att")),
                    FieldAccess(Id("a"), Id("att")),
                )),
                Break(),
            ])),
        ])
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)


    def test_attr_decl_0(self):
        stmt = Assign(Id("a"), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            AttributeDecl(Instance(), VarDecl(Id("att"), IntType())),
            MethodDecl(Static(), Id("not_main"), [], Block([])),
        ])
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)

    def test_attr_decl_1(self):
        stmt = Assign(Id("a"), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
            MethodDecl(Static(), Id("not_main"), [], Block([])),
        ])
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)

    def test_attr_decl_2(self):
        stmt = Assign(Id("a"), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Instance(), Id("att"), [], Block([])),
            AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
            MethodDecl(Static(), Id("not_main"), [], Block([])),
        ])
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)

    def test_attr_decl_3(self):
        stmt = Assign(Id("a"), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("$att"), [], Block([])),
            AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
            MethodDecl(Static(), Id("not_main"), [], Block([])),
        ])
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)

    def test_attr_decl_4(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            AttributeDecl(Instance(), VarDecl(Id("att"), IntType(), IntLiteral(1))),
            AttributeDecl(Instance(), VarDecl(Id("att"), IntType(), IntLiteral(1))),
            MethodDecl(Static(), Id("main"), [], Block([])),
        ])
])
        expect = str(SE.Redeclared(SE.Attribute(), "att"))
        self._test(testcase, expect)

    def test_attr_decl_5(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [
            AttributeDecl(Static(), VarDecl(Id("$att"), IntType(), IntLiteral(1))),
            AttributeDecl(Static(), VarDecl(Id("$att"), IntType(), IntLiteral(1))),
            MethodDecl(Static(), Id("main"), [], Block([])),
        ])
])
        expect = str(SE.Redeclared(SE.Attribute(), "$att"))
        self._test(testcase, expect)


    def test_assign_0(self):
        stmt = Assign(Id("a"), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType()),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_assign_1(self):
        stmt = Assign(Id("a"), StringLiteral("a"))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), FloatType()),
            Assign(Id("a"), IntLiteral(1)),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_assign_2(self):
        stmt = Assign(Id("a"), StringLiteral("a"))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), FloatType()),
            VarDecl(Id("b"), ArrayType(2, FloatType())),
            Assign(Id("b"), ArrayLiteral([IntLiteral(0), IntLiteral(1)])),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_assign_3(self):
        stmt = Assign(Id("a"), ArrayLiteral([IntLiteral(0), IntLiteral(1)]))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), ArrayType(3, IntType())),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_assign_4(self):
        stmt = Assign(Id("a"), IntLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            ConstDecl(Id("a"), IntType(), IntLiteral(1)),
            stmt,
        ])),]
    )
])
        expect = str(SE.CannotAssignToConstant(stmt))
        self._test(testcase, expect)

    def test_assign_5(self):
        stmt = Assign(Id("a"), IntLiteral(1))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            ConstDecl(Id("a"), IntType(), IntLiteral(1)),
            stmt,
        ])),]
    )
])
        expect = str(SE.CannotAssignToConstant(stmt))
        self._test(testcase, expect)


    def test_if_0(self):
        stmt = If(IntLiteral(10), Block([]), Block([]))
        testcase = \
Program([
    ClassDecl(Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)



    def test_continue_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            Continue(),
        ])),]
    )
])
        expect = str(SE.MustInLoop(Continue()))
        self._test(testcase, expect)

    def test_break_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            Break(),
        ])),]
    )
])
        expect = str(SE.MustInLoop(Break()))
        self._test(testcase, expect)

    def test_for_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), StringType()),
            For(Id("a"), IntLiteral(0), IntLiteral(10), Block([])),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(Assign(Id("a"), IntLiteral(0))))
        self._test(testcase, expect)

    def test_for_1(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            # VarDecl(Id("a"), StringType()),
            For(Id("a"), IntLiteral(0), IntLiteral(10), Block([])),
        ])),]
    )
])
        expect = str(SE.Undeclared(SE.Identifier(), "a"))
        self._test(testcase, expect)

    def test_for_2(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            ConstDecl(Id("a"), IntType(), IntLiteral(0)),
            For(Id("a"), IntLiteral(0), IntLiteral(10), Block([])),
        ])),]
    )
])
        expect = str(SE.CannotAssignToConstant(Assign(Id("a"), IntLiteral(0))))
        self._test(testcase, expect)

    def test_for_3(self):
        stmt = For(Id("a"), FloatLiteral(0), IntLiteral(10), Block([]))
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType(), IntLiteral(0)),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_for_4(self):
        stmt = For(Id("a"), IntLiteral(0), FloatLiteral(10), Block([]))
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType(), IntLiteral(0)),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)

    def test_for_5(self):
        stmt = For(Id("a"), IntLiteral(0), IntLiteral(10), Block([]), FloatLiteral(1))
        testcase = \
Program([
    ClassDecl(
        Id("A"), [MethodDecl(Instance(), Id("func"), [], Block([])),]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType(), IntLiteral(0)),
            stmt,
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(stmt))
        self._test(testcase, expect)





    def test_return_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            Return(IntLiteral(1))
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(Return(IntLiteral(1))))
        self._test(testcase, expect)

    def test_return_1(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Instance(), Id("Constructor"), [], Block([
                Return(IntLiteral(1))
            ])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(Return(IntLiteral(1))))
        self._test(testcase, expect)

    def test_return_2(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Instance(), Id("Destructor"), [], Block([
                Return(IntLiteral(1))
            ])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(Return(IntLiteral(1))))
        self._test(testcase, expect)

    def test_return_3(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Instance(), Id("func"), [], Block([
                Return(FloatLiteral(1)),
                Return(IntLiteral(1)),
                Return(),
            ])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(Return()))
        self._test(testcase, expect)



    def test_call_stmt_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(Instance(), Id("func"), [], Block([])),
            MethodDecl(Static(), Id("main"), [], Block([
                CallStmt(SelfLiteral(), Id("not_func"), [])
            ])),
        ]
    )
])
        expect = str(SE.Undeclared(SE.Method(), "not_func"))
        self._test(testcase, expect)

    def test_call_stmt_1(self):
        stmt = CallStmt(Id("Program"), Id("func"), [])
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(Instance(), Id("func"), [], Block([])),
            MethodDecl(Static(), Id("main"), [], Block([stmt])),
        ]
    )
])
        expect = str(SE.IllegalMemberAccess(stmt))
        self._test(testcase, expect)

    def test_call_stmt_2(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            CallStmt(Id("B"), Id("$func"), [])
        ])),]
    )
])
        expect = str(SE.Undeclared(SE.Class(), "B"))
        self._test(testcase, expect)

    def test_call_stmt_3(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            CallStmt(Id("B"), Id("func"), [])
        ])),]
    )
])
        expect = str(SE.Undeclared(SE.Identifier(), "B"))
        self._test(testcase, expect)

    def test_call_stmt_4(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), ClassType(Id("A"))),
            CallStmt(Id("a"), Id("$func"), []),
        ])),]
    )
])
        expect = str(SE.IllegalMemberAccess(CallStmt(Id("a"), Id("$func"), [])))
        self._test(testcase, expect)

    def test_call_stmt_5(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType()),
            CallStmt(Id("a"), Id("func"), []),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("a"), Id("func"), [])))
        self._test(testcase, expect)

    def test_call_stmt_6(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType()),
            CallStmt(Id("a"), Id("$func"), []),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("a"), Id("$func"), [])))
        self._test(testcase, expect)

    def test_call_stmt_7(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType()),
            CallStmt(Id("A"), Id("$func2"), []),
        ])),]
    )
])
        expect = str(SE.Undeclared(SE.Method(), "$func2"))
        self._test(testcase, expect)

    def test_call_stmt_8(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), IntType()),
            CallStmt(Id("A"), Id("$func"), [IntLiteral(1)]),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("A"), Id("$func"), [IntLiteral(1)])))
        self._test(testcase, expect)

    def test_call_stmt_9(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), ClassType(Id("A"))),
            CallStmt(Id("a"), Id("func"), [IntLiteral(1)]),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("a"), Id("func"), [IntLiteral(1)])))
        self._test(testcase, expect)

    def test_call_stmt_10(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [VarDecl(Id("X"), IntType())], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), ClassType(Id("A"))),
            CallStmt(Id("a"), Id("func"), [FloatLiteral(1)]),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("a"), Id("func"), [FloatLiteral(1)])))
        self._test(testcase, expect)

    def test_call_stmt_11(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [VarDecl(Id("X"), IntType())], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), ClassType(Id("A"))),
            CallStmt(Id("a"), Id("func"), [IntLiteral(1)]),
            CallStmt(Id("a"), Id("func"), [FloatLiteral(1)]),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("a"), Id("func"), [FloatLiteral(1)])))
        self._test(testcase, expect)

    def test_call_stmt_12(self):
        testcase = \
Program([
    ClassDecl(
        Id("A"),
        [
            MethodDecl(Static(), Id("$func"), [], Block([])),
            MethodDecl(Instance(), Id("func"), [VarDecl(Id("X"), FloatType())], Block([])),
        ]
    ),
    ClassDecl(
        Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([
            VarDecl(Id("a"), ClassType(Id("A"))),
            CallStmt(Id("a"), Id("func"), [IntLiteral(1)]),
            CallStmt(Id("a"), Id("func"), [StringLiteral("a")]),
        ])),]
    )
])
        expect = str(SE.TypeMismatchInStatement(CallStmt(Id("a"), Id("func"), [StringLiteral("a")])))
        self._test(testcase, expect)



    def test_method_decl_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(Instance(), Id("func"), [ ], Block([])),
            MethodDecl(Instance(), Id("func"), [ ], Block([])),
            MethodDecl(Static(), Id("main"), [ ], Block([])),
        ]
    )
])
        expect = str(SE.Redeclared(SE.Method(), "func"))
        self._test(testcase, expect)

    def test_method_decl_1(self):
        vd = VarDecl(Id("a"), IntType(), IntLiteral(1))
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(Instance(), Id("func"), [vd, vd], Block([])),
            MethodDecl(Instance(), Id("main"), [], Block([])),
        ]
    )
])
        expect = str(SE.Redeclared(SE.Parameter(), "a"))
        self._test(testcase, expect)

    def test_method_decl_2(self):
        vd = VarDecl(Id("a"), IntType(), IntLiteral(1))
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(Instance(), Id("func"), [vd], Block([vd])),
            MethodDecl(Instance(), Id("main"), [], Block([])),
        ]
    )
])
        expect = str(SE.Redeclared(SE.Variable(), "a"))
        self._test(testcase, expect)

    def test_method_decl_3(self):
        vd = VarDecl(Id("a"), IntType(), IntLiteral(1))
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(Instance(), Id("func"), [vd], Block([ConstDecl(Id("a"), IntType(), IntLiteral(1))])),
            MethodDecl(Instance(), Id("main"), [], Block([])),
        ]
    )
])
        expect = str(SE.Redeclared(SE.Constant(), "a"))
        self._test(testcase, expect)



    def test_class_decl_0(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [], Id("B")),
    ClassDecl(Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([])),]),
])
        expect = str(SE.Undeclared(SE.Class(), "B"))
        self._test(testcase, expect)

    def test_class_decl_1(self):
        testcase = \
Program([
    ClassDecl(Id("A"), []),
    ClassDecl(Id("A"), []),
    ClassDecl(Id("Program"), [MethodDecl(Static(), Id("main"), [], Block([])),]),
])
        expect = str(SE.Redeclared(SE.Class(), "A"))
        self._test(testcase, expect)

    def test_class_decl_2(self):
        testcase = \
Program([
    ClassDecl(Id("A"), [
        MethodDecl(Static(), Id("$func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Static(), ConstDecl(Id("$att"), IntType(), IntLiteral(1))),
        MethodDecl(Instance(), Id("func"), [], Block([Return(IntLiteral(1))])),
        AttributeDecl(Instance(), ConstDecl(Id("att"), IntType(), IntLiteral(1))),
    ]),
    ClassDecl(
        Id("Program"), [
            MethodDecl(Static(), Id("main"), [], Block([
                VarDecl(Id("a"), ClassType(Id("B"))),
            ])),
        ])
])
        expect = str(SE.Undeclared(SE.Class(), "B"))
        self._test(testcase, expect)



    def test_entry_point_0(self):
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("not_main"),
                [],
                Block([])
            ),
        ]
    )
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)

    def test_entry_point_1(self):
        testcase = \
Program([
    ClassDecl(Id("A"), []),
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)

    def test_entry_point_2(self):
        testcase = \
Program([
    ClassDecl(
        Id("Program"),
        [
            MethodDecl(
                Static(),
                Id("main"),
                [
                    VarDecl(Id("a"), IntType()),
                ],
                Block([])
            ),
        ]
    )
])
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)
