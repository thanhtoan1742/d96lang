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