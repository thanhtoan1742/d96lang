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
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_2(self):
        testcase = \
"""
Class Program {
    Val a, b: Int = 1, 2, 3;
}
"""
        expect = """Error on line 3 col 24: ,"""
        self._test(testcase, expect)

    def test_att_decl_3(self):
        testcase = \
"""
Class Program {
    Val a, b: Int =;
}
"""
        expect = """Error on line 3 col 19: ;"""
        self._test(testcase, expect)

    def test_att_decl_4(self):
        testcase = \
"""
Class Program {
    Val a, b: Int = 1 + 2;
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_5(self):
        testcase = \
"""
Class Program {
    Val $a, $b: Int = 1 + 2;
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_6(self):
        testcase = \
"""
Class Program {
    Val $a, b: Int = 1 + 2;
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_att_decl_7(self):
        testcase = \
"""
Class Program {
    NotValOrVar att: Int;
}
"""
        expect = "Error on line 3 col 16: att"
        self._test(testcase, expect)

    def test_att_decl_8(self):
        testcase = \
"""
Class Program {
    Var 123: Int;
}
"""
        expect = "Error on line 3 col 8: 123"
        self._test(testcase, expect)

    def test_att_decl_9(self):
        testcase = \
"""
Class Program {
    att: Int;
}
"""
        expect = "Error on line 3 col 7: :"
        self._test(testcase, expect)

    def test_att_decl_10(self):
        testcase = \
"""
Class Program {
    Var att;
}
"""
        expect = "Error on line 3 col 11: ;"
        self._test(testcase, expect)

    def test_att_decl_11(self):
        testcase = \
"""
Class Program {
    Var att: Int 123;
}
"""
        expect = "Error on line 3 col 17: 123"
        self._test(testcase, expect)

    def test_att_decl_12(self):
        testcase = \
"""
Class Program {
    Var att: Int = 123
}
"""
        expect = "Error on line 4 col 0: }"
        self._test(testcase, expect)



    # method declaration
    def test_method_decl_0(self):
        testcase = \
"""
Class Program {
    main() {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_1(self):
        testcase = \
"""
Class Program {
    $main() {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_2(self):
        testcase = \
"""
Class Program {
    method(a: Int) {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_3(self):
        testcase = \
"""
Class Program {
    method(a, b: Int) {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_4(self):
        testcase = \
"""
Class Program {
    method(a, b: Int; c: String; d, e: Boolean) {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_5(self):
        testcase = \
"""
Class Program {
    method(a, b: Int; c: String; d, e: Boolean)
}
"""
        expect = "Error on line 4 col 0: }"
        self._test(testcase, expect)

    def test_method_decl_6(self):
        testcase = \
"""
Class Program {
    method {}
}
"""
        expect = "Error on line 3 col 11: {"
        self._test(testcase, expect)

    def test_method_decl_7(self):
        testcase = \
"""
Class Program {
    0123() {}
}
"""
        expect = "Error on line 3 col 4: 0123"
        self._test(testcase, expect)

    def test_method_decl_8(self):
        testcase = \
"""
Class Program {
    method(a) {}
}
"""
        expect = "Error on line 3 col 12: )"
        self._test(testcase, expect)

    def test_method_decl_10(self):
        testcase = \
"""
Class Program {
    method(a: Int, b: String) {}
}
"""
        expect = "Error on line 3 col 17: ,"
        self._test(testcase, expect)

    def test_method_decl_11(self):
        testcase = \
"""
Class Program {
    method(a,: Int) {}
}
"""
        expect = "Error on line 3 col 13: :"
        self._test(testcase, expect)

    def test_method_decl_12(self):
        testcase = \
"""
Class Program {
    method(a: Int;) {}
}
"""
        expect = "Error on line 3 col 18: )"
        self._test(testcase, expect)

    def test_method_decl_13(self):
        testcase = \
"""
Class Program {
    method($a: Int) {}
}
"""
        expect = "Error on line 3 col 11: $a"
        self._test(testcase, expect)

    def test_method_decl_14(self):
        testcase = \
"""
Class Program {
    Constructor(a: Int) {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_15(self):
        testcase = \
"""
Class Program {
    Destructor() {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_16(self):
        testcase = \
"""
Class Program {
    Constructor() {}
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_method_decl_17(self):
        testcase = \
"""
Class Program {
    Destructor(a: Int) {}
}
"""
        expect = "Error on line 3 col 15: a"
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




    # array declaration
    def test_array_decl_0(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int, 2];
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_array_decl_1(self):
        testcase = \
"""
Class Program {
    Var a: Array[Array[Int, 3], 2];
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_array_decl_2(self):
        testcase = \
"""
Class Program {
    Var a: Array[Program, 2];
}
"""
        expect = "Error on line 3 col 17: Program"
        self._test(testcase, expect)

    def test_array_decl_3(self):
        testcase = \
"""
Class Program {
    Var a: Array(Int, 2);
}
"""
        expect = "Error on line 3 col 16: ("
        self._test(testcase, expect)

    def test_array_decl_4(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int];
}
"""
        expect = "Error on line 3 col 20: ]"
        self._test(testcase, expect)

    def test_array_decl_5(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int, 1.2];
}
"""
        expect = "Error on line 3 col 22: 1.2"
        self._test(testcase, expect)

    def test_array_decl_6(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int 1];
}
"""
        expect = "Error on line 3 col 21: 1"
        self._test(testcase, expect)




    # array expression
    def test_array_exp_0(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int, 2] = Array(1, 2);
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_array_exp_1(self):
        testcase = \
"""
Class Program {
    Var a: Array[Array[Int, 2], 2] = Array(Array(1, 2), Array(3, 4));
}
"""
        expect = "successful"
        self._test(testcase, expect)

    def test_array_exp_2(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int, 2] = Array(1 2);
}
"""
        expect = "Error on line 3 col 35: 2"
        self._test(testcase, expect)

    def test_array_exp_2(self):
        testcase = \
"""
Class Program {
    Var a: Array[Int, 2] = Array[1, 2];
}
"""
        expect = "Error on line 3 col 32: ["
        self._test(testcase, expect)




    # arithmetic expression
    def test_arith_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = 1 + 2;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_arith_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = 1 - 2;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_arith_exp_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = 1 * 2;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_arith_exp_3(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = 1 / 2;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_arith_exp_4(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = 1 % 2;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)


    def test_arith_exp_5(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = -1;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)


    # boolean expression
    def test_bool_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = !boolVar;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_bool_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = bool0 && bool1;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_bool_exp_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = bool0 || bool1;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_bool_exp_3(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = "a" ==. "b";
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_bool_exp_4(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = !b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)


    # string expression
    def test_str_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: String = "a" +. "b";
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)



    # relational operation
    def test_rel_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = a == b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_rel_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = a != b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_rel_exp_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = a < b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_rel_exp_3(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = a > b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_rel_exp_4(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = a <= b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_rel_exp_5(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Bool = a >= b;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)



    # index operator expression
    def test_idx_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = arr[1];
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_idx_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = arr[1][2][3];
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_idx_exp_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Int = arr[];
    }
}
"""
        expect = """Error on line 4 col 24: ["""
        self._test(testcase, expect)


    # instance access operator expression
    def test_dot_op_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: String = System.filename;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_dot_op_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: String = Stdin.read();
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_dot_op_exp_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: String = System.File.Path.filename;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_dot_op_exp_3(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: File = System.File.Path.open("input.txt");
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_dot_op_exp_4(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: String = System.File.Path..filename;
    }
}
"""
        expect = """Error on line 4 col 40: .."""
        self._test(testcase, expect)

    def test_dot_op_exp_5(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: String = System.$filename;
    }
}
"""
        expect = """Error on line 4 col 30: ."""
        self._test(testcase, expect)




    # static access operator expression
    def test_coloncolon_op_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Float = Math::$PI;
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_coloncolon_op_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Float = Math::$exp(10);
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_coloncolon_op_exp_2(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Float = Math::exp(10);
    }
}
"""
        expect = """Error on line 4 col 29: exp"""
        self._test(testcase, expect)

    def test_coloncolon_op_exp_3(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Float = Math::Functions::$exp(10);
    }
}
"""
        expect = """Error on line 4 col 29: Functions"""
        self._test(testcase, expect)


    # new operator expression
    def test_new_op_exp_0(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Shade = New Shade();
    }
}
"""
        expect = """successful"""
        self._test(testcase, expect)

    def test_new_op_exp_1(self):
        testcase = \
"""
Class Program {
    main() {
        Val a: Shade = New Square(10);
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

