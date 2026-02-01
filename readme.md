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
8. Outputs the result to a Excel sheet

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
```

##This grader works for simple console (terminal) programs that follow this pattern:

1. Program starts
2. Reads all required input from standard input (stdin)
3. Computes the answer
4. Prints the final result to standard output (stdout)
5. Program ends

Typical examples that work perfectly:
- Mathematical calculations (sum, factorial, prime check, etc.)
- Array and string processing
- Loops and condition based problems
- Competitive programming style questions
- Programs that run once and terminate quickly

As long as your program only uses:
- `input()` / `scanf` / `cin` / `Scanner`
to read input, and
- `print()` / `printf` / `cout` / `System.out.print`
to print output,

the grader will work correctly.

The grader simulates a user typing input in the terminal and pressing Enter.


## Where This Grader Will NOT Work

This grader will fail or hang for programs that:

- Open GUI windows (Swing, JavaFX, Tkinter, etc.)
- Require mouse clicks or button presses
- Read from or write to external files instead of stdin/stdout
- Wait for continuous or interactive user input
  (for example: menus like “press 1, 2, 3 repeatedly”)
- Run forever (infinite loops or servers)
- Start web servers or network listeners
- Depend on real-time input after producing output

Examples that will NOT work:

```text
1) Programs that show:
   "Enter your choice:"
   and wait again and again for input

2) Programs that do:
   read from "input.txt"
   write to "output.txt"

3) Programs that never exit, like:
   while(true) { ... }

4) GUI apps that open a window instead of using the console
