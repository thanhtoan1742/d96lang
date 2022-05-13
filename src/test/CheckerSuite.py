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
