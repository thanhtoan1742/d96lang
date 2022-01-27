import unittest
from TestUtils import TestParser
from LexerSuite import write_expect

class ParserSuite(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        ParserSuite.counter = 999
        ParserSuite.marker = '☒'

    def _test(self, testcase, expect):
        ParserSuite.counter += 1
        write_expect(expect, self.counter)
        try:
            self.assertTrue(TestParser.test(testcase, expect, ParserSuite.counter))
        except AssertionError:
            raise AssertionError(f"{ParserSuite.marker} parser failed at test: {ParserSuite.counter}")


    # sample test from BKeL
    def test_sample_1000(self):
        testcase = \
"""
Class main{}
"""
        expect = """successful"""
        self._test(testcase, expect)


    def test_sample_1001(self):
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


    def test_sample_1002(self):
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
    def test_class_1003(self):
        testcase = \
"""
Class Program {
    Val attr1: Int = 0;
    Var $attr2: String = "asdasd";
    main() {
    }
}
"""
        expect = "successful"

    def test_class_1004(self):
        testcase = \
"""
Class Program {
    Val attr1: Int = 0;
    Var $attr2: String = "asdasd";
    Val $attr3, at5: Float;

    $laugh(a, b: String; c: Int) {
    }

    add() {
    }

    main() {
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)
