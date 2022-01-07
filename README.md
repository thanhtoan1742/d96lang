# D96
A programming language created follows a PPL course.

## Setup development environment
Set environment variable ANTLR_JAR to the file antlr-4.9.2-complete.jar in your computer.  
Place `jasmin.jar` in `src/external/`.  
Compile `src/lib/io.java` into `src/lib/io.class`.  
Install antlr4 python runtime with `pip install antlr4-python3-runtime`.  

## Commands
Change current directory to `src/` where there is file run.py
```txt
python run.py gen
python run.py test LexerSuite
python run.py test ParserSuite
python run.py test ASTGenSuite
python run.py test CheckerSuite
python run.py test CodeGenSuite
```
