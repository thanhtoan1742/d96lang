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


    #my testcase
    #comment
    def test_comment_0(self):
        testcase = """## 123 ##"""
        expect = """ 123 ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_1(self):
        testcase = \
"""## multiline
comment ##
"""
        expect = \
""" multiline
comment ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_2(self):
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

    def test_comment_3(self):
        testcase = """## keywords in comment are ignored: Val Var Int Float For If Else ##"""
        expect = """ keywords in comment are ignored: Val Var Int Float For If Else ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_4(self):
        testcase = """##2 consecutive comments##  ## the second comment ##"""
        expect = """2 consecutive comments, the second comment ,<EOF>"""
        self._test(testcase, expect)

    def test_comment_5(self):
        testcase = """## 2 consecutive comments with some thing in between ## Val Var ## the second comment ##"""
        expect = """ 2 consecutive comments with some thing in between ,Val,Var, the second comment ,<EOF>"""
        self._test(testcase, expect)



    # keyword
    def test_keyword_0(self):
        testcase = """Break"""
        expect = """Break,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_1(self):
        testcase = """Continue"""
        expect = """Continue,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_2(self):
        testcase = """If"""
        expect = """If,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_3(self):
        testcase = """Elseif"""
        expect = """Elseif,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_4(self):
        testcase = """Else"""
        expect = """Else,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_5(self):
        testcase = """Foreach"""
        expect = """Foreach,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_6(self):
        testcase = """Array"""
        expect = """Array,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_7(self):
        testcase = """In"""
        expect = """In,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_8(self):
        testcase = """Int"""
        expect = """Int,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_9(self):
        testcase = """Float"""
        expect = """Float,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_10(self):
        testcase = """Boolean"""
        expect = """Boolean,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_11(self):
        testcase = """String"""
        expect = """String,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_12(self):
        testcase = """Return"""
        expect = """Return,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_13(self):
        testcase = """Null"""
        expect = """Null,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_14(self):
        testcase = """Class"""
        expect = """Class,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_15(self):
        testcase = """Val"""
        expect = """Val,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_16(self):
        testcase = """Var"""
        expect = """Var,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_17(self):
        testcase = """Self"""
        expect = """Self,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_18(self):
        testcase = """Constructor"""
        expect = """Constructor,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_19(self):
        testcase = """Destructor"""
        expect = """Destructor,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_20(self):
        testcase = """New"""
        expect = """New,<EOF>"""
        self._test(testcase, expect)

    def test_keyword_21(self):
        testcase = """By"""
        expect = """By,<EOF>"""
        self._test(testcase, expect)




    # operator
    def test_operator_0(self):
        testcase = """+"""
        expect = """+,<EOF>"""
        self._test(testcase, expect)

    def test_operator_1(self):
        testcase = """-"""
        expect = """-,<EOF>"""
        self._test(testcase, expect)

    def test_operator_2(self):
        testcase = """*"""
        expect = """*,<EOF>"""
        self._test(testcase, expect)

    def test_operator_3(self):
        testcase = """/"""
        expect = """/,<EOF>"""
        self._test(testcase, expect)

    def test_operator_4(self):
        testcase = """%"""
        expect = """%,<EOF>"""
        self._test(testcase, expect)

    def test_operator_5(self):
        testcase = """!"""
        expect = """!,<EOF>"""
        self._test(testcase, expect)

    def test_operator_6(self):
        testcase = """&&"""
        expect = """&&,<EOF>"""
        self._test(testcase, expect)

    def test_operator_7(self):
        testcase = """||"""
        expect = """||,<EOF>"""
        self._test(testcase, expect)

    def test_operator_8(self):
        testcase = """=="""
        expect = """==,<EOF>"""
        self._test(testcase, expect)

    def test_operator_9(self):
        testcase = """="""
        expect = """=,<EOF>"""
        self._test(testcase, expect)

    def test_operator_10(self):
        testcase = """!="""
        expect = """!=,<EOF>"""
        self._test(testcase, expect)

    def test_operator_11(self):
        testcase = """<"""
        expect = """<,<EOF>"""
        self._test(testcase, expect)

    def test_operator_12(self):
        testcase = """<="""
        expect = """<=,<EOF>"""
        self._test(testcase, expect)

    def test_operator_13(self):
        testcase = """>"""
        expect = """>,<EOF>"""
        self._test(testcase, expect)

    def test_operator_14(self):
        testcase = """>="""
        expect = """>=,<EOF>"""
        self._test(testcase, expect)

    def test_operator_15(self):
        testcase = """==."""
        expect = """==.,<EOF>"""
        self._test(testcase, expect)

    def test_operator_16(self):
        testcase = """+."""
        expect = """+.,<EOF>"""
        self._test(testcase, expect)

    def test_operator_17(self):
        testcase = """."""
        expect = """.,<EOF>"""
        self._test(testcase, expect)

    def test_operator_18(self):
        testcase = """::"""
        expect = """::,<EOF>"""
        self._test(testcase, expect)

    def test_operator_19(self):
        testcase = """New"""
        expect = """New,<EOF>"""
        self._test(testcase, expect)



    # seperator
    def test_seperator_0(self):
        testcase = """("""
        expect = """(,<EOF>"""
        self._test(testcase, expect)

    def test_seperator_1(self):
        testcase = """)"""
        expect = """),<EOF>"""
        self._test(testcase, expect)

    def test_seperator_2(self):
        testcase = """["""
        expect = """[,<EOF>"""
        self._test(testcase, expect)

    def test_seperator_3(self):
        testcase = """]"""
        expect = """],<EOF>"""
        self._test(testcase, expect)

    def test_seperator_4(self):
        testcase = """{"""
        expect = """{,<EOF>"""
        self._test(testcase, expect)

    def test_seperator_5(self):
        testcase = """}"""
        expect = """},<EOF>"""
        self._test(testcase, expect)

    def test_seperator_6(self):
        testcase = """."""
        expect = """.,<EOF>"""
        self._test(testcase, expect)

    def test_seperator_7(self):
        testcase = ""","""
        expect = """,,<EOF>"""
        self._test(testcase, expect)

    def test_seperator_8(self):
        testcase = """;"""
        expect = """;,<EOF>"""
        self._test(testcase, expect)

    def test_seperator_9(self):
        testcase = """:"""
        expect = """:,<EOF>"""
        self._test(testcase, expect)



    #int literal
    def test_int_lit_0(self):
        testcase = """0"""
        expect = """0,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_1(self):
        testcase = """1234567890"""
        expect = """1234567890,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_2(self):
        testcase = """1_234_567_890"""
        expect = """1234567890,<EOF>"""
        self._test(testcase, expect)

    #TODO: test 123a, 19a2, _123, 123_

    def test_int_lit_4(self):
        testcase = """0x0"""
        expect = """0x0,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_5(self):
        testcase = """0X1234567890ABCDEF"""
        expect = """0X1234567890ABCDEF,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_6(self):
        testcase = """0X123_456_789_0_A_B_CDE_F"""
        expect = """0X1234567890ABCDEF,<EOF>"""
        self._test(testcase, expect)

    #TODO: test 0x00, 0xA_AG, 0x_A1, 0_x112, 0x11_

    def test_int_lit_7(self):
        testcase = """00"""
        expect = """00,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_8(self):
        testcase = """012345670"""
        expect = """012345670,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_9(self):
        testcase = """012_3_456_70"""
        expect = """012345670,<EOF>"""
        self._test(testcase, expect)

    #TODO: test 000, 07_18, 0_21, 023_

    def test_int_lit_10(self):
        testcase = """0b0"""
        expect = """0b0,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_11(self):
        testcase = """0b10"""
        expect = """0b10,<EOF>"""
        self._test(testcase, expect)

    def test_int_lit_12(self):
        testcase = """0b1_0"""
        expect = """0b10,<EOF>"""
        self._test(testcase, expect)

    #TODO: test 0b00, 0b1_02, 0b_11, 0_b11, 0b11_

