import unittest
from TestUtils import TestParser
from LexerSuite import write_wrong_answer

class ParserSuite(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        ParserSuite.counter = 999

    def _test(self, testcase, expect):
        ParserSuite.counter += 1
        try:
            self.assertTrue(TestParser.test(testcase, expect, ParserSuite.counter))
        except AssertionError:
            write_wrong_answer(expect, self.counter)
            raise AssertionError(f"parser failed at test {ParserSuite.counter}")


    # sample test from BKeL
    def test_sample_0(self):
        testcase = \
"""
Class main{}
"""
        expect = """successful"""
        self._test(testcase, expect)


    def test_sample_1(self):
        testcase = \
"""
Class Rectangle: Shape {
    getArea() {
        Return Self.length * Self.width;
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)


    def test_sample_2(self):
        testcase = \
"""
    Class Shape {
        $getNumOfShape( {
            Return Self.length * Self.width;
        }
    }
"""
        expect = "Error on line 3 col 24: {"
        self._test(testcase, expect)


    # my test
    # class declaration test
    def test_class_decl_0(self):
        testcase = \
"""
Class Program {
}
"""
        expect = "successful"

    def test_class_decl_1(self):
        testcase = \
"""
Class Derived:Super {
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_class_decl_2(self):
        testcase = \
"""
Class $Program {
}
"""
        expect = "Error on line 2 col 6: $Program"
        self._test(testcase, expect)

    def test_class_decl_3(self):
        testcase = \
"""
Class Derived:$Super {
}
"""
        expect = "Error on line 2 col 14: $Super"
        self._test(testcase, expect)

    def test_class_decl_4(self):
        testcase = \
"""
Class Program
"""
        expect = "Error on line 3 col 0: <EOF>"
        self._test(testcase, expect)

    def test_class_decl_5(self):
        testcase = \
"""
Class Derived: {
}
"""
        expect = "Error on line 2 col 15: {"
        self._test(testcase, expect)

    def test_class_decl_6(self):
        testcase = \
"""
Class {
}
"""
        expect = "Error on line 2 col 6: {"
        self._test(testcase, expect)



    # atrributes declaration
    def test_att_decl_0(self):
        testcase = \
"""
Class Program {
    Val a, b: Int = 1, 2;
    main() {
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_1(self):
        testcase = \
"""
Class Program {
    Val a, b: Int = 1;
    main() {
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_2(self):
        testcase = \
"""
Class Program {
    Val a, b: Int = 1, 2, 3;
    main() {
    }
}
"""
        expect = """Error on line 3 col 24: ,"""
        self._test(testcase, expect)

    def test_att_decl_3(self):
        testcase = \
"""
Class Program {
Val a, b: Int =;
    main() {
    }
}
"""
        expect = """Error on line 3 col 15: ;"""
        self._test(testcase, expect)

    def test_att_decl_4(self):
        testcase = \
"""
Class Program {
Val a, b: Int = 1 + 2;
    main() {
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_5(self):
        testcase = \
"""
Class Program {
Val $a, $b: Int = 1 + 2;
    main() {
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_6(self):
        testcase = \
"""
Class Program {
Val $a, b: Int = 1 + 2;
    main() {
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)




    # var/val declaration
    def test_var_decl_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a, b: Int = 1, 2;
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_var_decl_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a, b: Int = 1;
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_var_decl_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a, b: Int = 1, 2, 3;
    }
}
"""
        expect = """Error on line 4 col 28: ,"""
        self._test(testcase, expect)

    def test_var_decl_3(self):
        testcase = \
"""
Class Program {
    main() {
        Val a, b: Int =;
    }
}
"""
        expect = """Error on line 4 col 23: ;"""
        self._test(testcase, expect)

    def test_var_decl_4(self):
        testcase = \
"""
Class Program {
    main() {
        Val a, b: Int = 1 + 2;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    # test variable declaration statement
    def test_var_decl_stmt_0(self):
        testcase = \
"""
Class Program {
    main() {
        Var a: Boolean = True;
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)

    # test variable declaration statement
    def test_var_decl_stmt_1(self):
        testcase = \
"""
Class Program {
    main() {
        Var $a: Boolean = True;
    }
}
"""
        expect = "Error on line 4 col 12: $a"
        self._test(testcase, expect)

