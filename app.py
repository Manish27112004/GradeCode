import subprocess

# -----------------------------
# HARDCODED TEST CASES
# -----------------------------
testcases = [
    {
        "input": "5\n",
        "expected": "True"
    },
    {
        "input": "3\n",
        "expected": "True"
    },
    {
        "input": "100\n",
        "expected": "False"
    }
]

# -----------------------------
# FUNCTION TO RUN ONE TESTCASE
# -----------------------------
def run_testcase(input_data, expected_output):
    try:
        # Run the student program
        result = subprocess.run(
            ["python", "student.py"],       # program to run
            input=input_data.encode(),       # send input
            stdout=subprocess.PIPE,          # capture output
            stderr=subprocess.PIPE,          # capture errors
            timeout=2                        # max time allowed
        )
    except subprocess.TimeoutExpired:
        return "TIME LIMIT EXCEEDED"

    # Get the output as text
    output = result.stdout.decode().strip()

    # Compare expected vs actual
    if output == expected_output:
        return "PASS"
    else:
        return f"FAIL (expected: {expected_output}, got: {output})"


# -----------------------------
# RUN ALL TESTCASES
# -----------------------------
print("----- GRADING STARTED -----")
passed = 0
total = len(testcases)
for i, t in enumerate(testcases, start=1):
    result = run_testcase(t["input"], t["expected"])
    if result == "PASS":
        passed += 1
    print(f"Testcase {i}: {result}")
    
print(f"Score: {passed}/{total}")
print("----- GRADING FINISHED -----")
