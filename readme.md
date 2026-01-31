# Multi-Language Auto Grader

This project is a simple auto-grading system written in Python.  
It can compile and run student programs in multiple languages and check their output against predefined test cases.

Supported languages:

- Python (`.py`)
- C (`.c`)
- C++ (`.cpp`)
- Java (`.java`)

The grader:
1. Detects the language from the file extension
2. Compiles the code if required (C/C++/Java)
3. Runs the program for each test case
4. Sends input through standard input (stdin)
5. Captures printed output (stdout)
6. Compares it with expected output
7. Reports PASS / Wrong Answer / TLE / Runtime Error / Compilation Error

## ⚙️ Requirements

### Python
- Python 3 installed

### Java
- JDK installed and available in PATH

Check:
```bash
java --version
```

### C / C++
- `gcc` and `g++` installed and available in PATH

Check:
```bash
gcc --version
g++ --version
