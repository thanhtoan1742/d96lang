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


    def test_sample_1000(self):
        testcase = \
"""
class main{}
"""
        expect = """successful"""
        self._test(testcase, expect)


    def test_sample_1001(self):
        testcase = \
"""
class Rectangle: Shape {
    getArea() {
        Return self.length * self.width;
    }
}
"""
        expect = "successful"
        self._test(testcase, expect)


    def test_sample_1002(self):
        testcase = \
"""
    class Shape {
        $getNumOfShape( {
            Return self.length * self.width;
        }
    }
"""
        expect = "Error on line 3 col 40: {"
        self._test(testcase, expect)