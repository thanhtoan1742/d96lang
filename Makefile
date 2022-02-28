build_antlr:
	cd src/ &&\
	python run.py gen

clean_test:
	cd src/test/ &&\
	rm -rf solutions/ testcases/ WAs/ &&\
	mkdir solutions/ testcases/ WAs/

test_lexer: build_antlr clean_test
	cd src/ &&\
	python run.py test LexerSuite 2>&1 | grep -E "(FAIL|OK|Ran|^AssertionError: lexer)"

test_parser: build_antlr clean_test
	cd src/ &&\
	python run.py test ParserSuite 2>&1 | grep -E "(FAIL|OK|Ran|^AssertionError: parser)"

test_ast: build_antlr clean_test
	cd src/ &&\
	python run.py test ASTGenSuite 2>&1 | grep -E "(FAIL|OK|Ran|^AssertionError: ast)"


prepare_submission: build_antlr
	rm -f submission/*
	cp -f src/main/d96/parser/D96.g4 submission/
	cp -f src/test/ASTGenSuite.py submission/
	cp -f src/main/d96/astgen/ASTGeneration.py submission/
	cp -f target/main/d96/parser/D96.interp submission/
	cp -f target/main/d96/parser/D96.tokens submission/
	cp -f target/main/d96/parser/D96Lexer.interp submission/
	cp -f target/main/d96/parser/D96Lexer.py submission/
	cp -f target/main/d96/parser/D96Lexer.tokens submission/
	cp -f target/main/d96/parser/D96Parser.py submission/
	cp -f target/main/d96/parser/D96Visitor.py submission/


clean: clean_test