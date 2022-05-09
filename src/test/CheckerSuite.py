import unittest
from TestUtils import TestChecker
import AST
import StaticError as SE


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
        CheckerSuite.counter = 1999

    def _test(self, testcase, expect):
        CheckerSuite.counter += 1
        try:
            self.assertTrue(TestChecker.test(testcase, expect, CheckerSuite.counter))
        except AssertionError:
            write_wrong_answer(expect, self.counter)
            raise AssertionError(f"checker failed at test {CheckerSuite.counter}")

    # sample test from BKeL
    def test_sample_0(self):
        testcase = """
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
        """
        expect = "Redeclared Attribute: myVar"
        self._test(testcase, expect)

    def test_entry_point_0(self):
        testcase = """
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
        """
        expect = str(SE.NoEntryPoint())
        self._test(testcase, expect)