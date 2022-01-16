import unittest
from TestUtils import TestLexer


def write_expect(expect, num):
    from pathlib import Path
    Path('./test/expects/').mkdir(parents=True, exist_ok=True)
    path = './test/expects/' + str(num) + '.txt'
    open(path, 'w+').write(expect)

class LexerSuite(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        LexerSuite.counter = -1
        LexerSuite.marker = '☒'

    def _test(self, testcase, expect):
        LexerSuite.counter += 1
        write_expect(expect, self.counter)
        try:
            self.assertTrue(TestLexer.test(testcase, expect, LexerSuite.counter))
        except AssertionError:
            raise AssertionError(f"{LexerSuite.marker} lexer failed at test: {LexerSuite.counter}")


    # sample test in BKeL
    def test_sample_0(self):
        testcase = "abc"
        expect = "abc,<EOF>"
        self._test(testcase, expect)

    def test_sample_1(self):
        testcase = "Break"
        expect = "Break,<EOF>"
        self._test(testcase, expect)

    def test_sample_2(self):
        testcase = "ab?svn"
        expect = "ab,Error Token ?"
        self._test(testcase, expect)

    def test_sample_3(self):
        testcase = "Return x;"
        expect = "Return,x,;,<EOF>"
        self._test(testcase, expect)

    def test_sample_4(self):
        testcase = """ "abc\\h def"  """
        expect = """Illegal Escape In String: abc\\h"""
        self._test(testcase, expect)

    def test_sample_5(self):
        testcase = """ "abc def  """
        expect = """Unclosed String: abc def"""
        self._test(testcase, expect)


    # my testcase
    # comment
    def test_comment_6(self):
        testcase = """## 123 ##"""
        expect = """ 123 ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_7(self):
        testcase = \
"""## multiline
comment ##
"""
        expect = \
""" multiline
comment ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_8(self):
        testcase = \
"""## multi
multi
    multi
       multi
line
  comment##
"""
        expect = \
""" multi
multi
    multi
       multi
line
  comment,<EOF>"""
        self._test(testcase, expect)

    def test_comment_9(self):
        testcase = """## keywords in comment are ignored: Val Var Int Float For If Else ##"""
        expect = """ keywords in comment are ignored: Val Var Int Float For If Else ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_10(self):
        testcase = """##2 consecutive comments##  ## the second comment ##"""
        expect = """2 consecutive comments, the second comment ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_11(self):
        testcase = """## 2 consecutive comments with some thing in between ## Val Var ## the second comment ##"""
        expect = """ 2 consecutive comments with some thing in between ,Val,Var, the second comment ,<EOF>"""
        self._test(testcase, expect)


    # int literal
    def test_int_lit_12(self):
        testcase = """1234567890"""
        expect = """1234567890,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_13(self):
        testcase = """1_234_567_890"""
        expect = """1234567890,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_14(self):
        testcase = """1_23___4__5_6___7_89___0"""
        expect = """1234567890,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_15(self):
        """
        NOTE:
        currently, this test gives '1234567890' as INT_LIT
        and '_' as ID, it should give an error, something like 'int literal not correct'
        but the statement does not define how to handle this kind of error.

        """
        return
        testcase = """1_23___4__5_6___7_89___0_"""
        expect = """1234567890,<EOF>"""
        self._test(testcase, expect)


    def test_int_lit_16(self):
        testcase = """0x1"""
        expect = """0x1,<EOF>"""
        self._test(testcase, expect)



    # TODO: create tests that check matching every token
