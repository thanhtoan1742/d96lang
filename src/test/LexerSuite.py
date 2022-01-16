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
    def test_comment_6(self):
        testcase = """## 123 ##"""
        expect = """ 123 ,<EOF>"""
        self._test(testcase, expect)

    def test_commnet_7(self):
        testcase = \
"""## multiline
comment ##
"""
        expect = \
""" multiline
comment ,<EOF>"""
        self._test(testcase, expect)

    def test_commnet_8(self):
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

