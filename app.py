import subprocess
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class TestStatus(Enum):
    PASS = "PASS"
    WRONG_ANSWER = "Wrong Answer"
    TLE = "Time Limit Exceeded"
    RUNTIME_ERROR = "Runtime Error"
    COMPILATION_ERROR = "Compilation Error"


@dataclass
class TestCase:
    input_data: str
    expected_output: str


@dataclass
class TestResult:
    status: TestStatus
    execution_time: float
    actual_output: str
    expected_output: str
    error_message: str = ""


class LanguageConfig:
    """Configuration for different programming languages"""
    
    def __init__(self, extension: str, compile_cmd: Optional[List[str]], 
                 run_cmd: List[str], needs_compilation: bool):
        self.extension = extension
        self.compile_cmd = compile_cmd
        self.run_cmd = run_cmd
        self.needs_compilation = needs_compilation


class AutoGrader:
    # Language configurations
    LANGUAGES = {
        '.py': LanguageConfig(
            extension='.py',
            compile_cmd=None,
            run_cmd=['python'],
            needs_compilation=False
        ),
        '.c': LanguageConfig(
            extension='.c',
            compile_cmd=['gcc', '{file}', '-o', 'prog.exe'],
            run_cmd=['prog.exe'],
            needs_compilation=True
        ),
        '.cpp': LanguageConfig(
            extension='.cpp',
            compile_cmd=['g++', '{file}', '-o', 'prog.exe'],
            run_cmd=['prog.exe'],
            needs_compilation=True
        ),
        '.java': LanguageConfig(
            extension='.java',
            compile_cmd=['javac', '{file}'],
            run_cmd=['java', '{classname}'],
            needs_compilation=True
        )
    }
    
    def __init__(self, time_limit: float = 2.0):
        self.time_limit = time_limit
    
    def detect_language(self, file_path: str) -> Optional[LanguageConfig]:
        """Detect programming language from file extension"""
        extension = Path(file_path).suffix.lower()
        return self.LANGUAGES.get(extension)
    
    def compile_code(self, file_path: str, lang_config: LanguageConfig) -> Tuple[bool, str]:
        """Compile the code if needed. Returns (success, error_message)"""
        if not lang_config.needs_compilation:
            return True, ""
        
        # Prepare compile command
        compile_cmd = [cmd.format(file=file_path) for cmd in lang_config.compile_cmd]
        
        try:
            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second compilation timeout
            )
            
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
            
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, str(e)
    
    def normalize_output(self, output: str) -> str:
        """Normalize output by removing trailing spaces and newlines"""
        lines = output.split('\n')
        # Remove trailing spaces from each line
        lines = [line.rstrip() for line in lines]
        # Join and remove trailing newlines
        return '\n'.join(lines).rstrip('\n')
    
    def run_test_case(self, lang_config: LanguageConfig, file_path: str, 
                      test_case: TestCase) -> TestResult:
        """Run a single test case"""
        # Prepare run command
        run_cmd = lang_config.run_cmd.copy()
        
        # For Java, extract class name
        if lang_config.extension == '.java':
            classname = Path(file_path).stem
            run_cmd = [cmd.format(classname=classname) for cmd in run_cmd]
        elif lang_config.extension == '.py':
            run_cmd.append(file_path)
        
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                run_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Run with timeout
            stdout, stderr = process.communicate(
                input=test_case.input_data,
                timeout=self.time_limit
            )
            
            execution_time = time.time() - start_time
            
            # Check for runtime error
            if process.returncode != 0:
                return TestResult(
                    status=TestStatus.RUNTIME_ERROR,
                    execution_time=execution_time,
                    actual_output=stdout,
                    expected_output=test_case.expected_output,
                    error_message=stderr
                )
            
            # Normalize outputs
            actual = self.normalize_output(stdout)
            expected = self.normalize_output(test_case.expected_output)
            
            # Compare outputs
            if actual == expected:
                status = TestStatus.PASS
            else:
                status = TestStatus.WRONG_ANSWER
            
            return TestResult(
                status=status,
                execution_time=execution_time,
                actual_output=actual,
                expected_output=expected
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            execution_time = time.time() - start_time
            return TestResult(
                status=TestStatus.TLE,
                execution_time=execution_time,
                actual_output="",
                expected_output=test_case.expected_output,
                error_message="Time limit exceeded"
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                status=TestStatus.RUNTIME_ERROR,
                execution_time=execution_time,
                actual_output="",
                expected_output=test_case.expected_output,
                error_message=str(e)
            )
    
    def grade(self, file_path: str, test_cases: List[TestCase]) -> Dict:
        """Grade a student's code against test cases"""
        
        # Detect language
        lang_config = self.detect_language(file_path)
        if not lang_config:
            return {
                'error': f"Unsupported file extension: {Path(file_path).suffix}",
                'results': [],
                'score': 0
            }
        
        # Compile if needed
        if lang_config.needs_compilation:
            success, error_msg = self.compile_code(file_path, lang_config)
            if not success:
                # Return compilation error for all test cases
                results = [
                    TestResult(
                        status=TestStatus.COMPILATION_ERROR,
                        execution_time=0,
                        actual_output="",
                        expected_output=tc.expected_output,
                        error_message=error_msg
                    )
                    for tc in test_cases
                ]
                return {
                    'compilation_error': error_msg,
                    'results': results,
                    'score': 0,
                    'passed': 0,
                    'total': len(test_cases)
                }
        
        # Run test cases
        results = []
        for i, test_case in enumerate(test_cases):
            print(f"Running test case {i + 1}/{len(test_cases)}...", end=' ')
            result = self.run_test_case(lang_config, file_path, test_case)
            results.append(result)
            print(result.status.value)
        
        # Calculate score
        passed = sum(1 for r in results if r.status == TestStatus.PASS)
        total = len(test_cases)
        score = (passed / total * 100) if total > 0 else 0
        
        return {
            'results': results,
            'score': score,
            'passed': passed,
            'total': total
        }
    
    def print_report(self, grading_result: Dict, file_path: str):
        """Print a detailed grading report"""
        print("\n" + "="*70)
        print(f"GRADING REPORT FOR: {file_path}")
        print("="*70)
        
        if 'error' in grading_result:
            print(f"\nERROR: {grading_result['error']}")
            return
        
        if 'compilation_error' in grading_result:
            print("\n❌ COMPILATION ERROR")
            print("-"*70)
            print(grading_result['compilation_error'])
            print("-"*70)
            return
        
        results = grading_result['results']
        
        print(f"\nTest Cases: {grading_result['total']}")
        print(f"Passed: {grading_result['passed']}")
        print(f"Failed: {grading_result['total'] - grading_result['passed']}")
        print(f"Score: {grading_result['score']:.2f}%")
        print("\n" + "-"*70)
        
        for i, result in enumerate(results, 1):
            status_symbol = "✓" if result.status == TestStatus.PASS else "✗"
            print(f"\nTest Case {i}: {status_symbol} {result.status.value}")
            print(f"Execution Time: {result.execution_time:.4f}s")
            
            if result.status != TestStatus.PASS:
                print(f"\nExpected Output:")
                print(result.expected_output)
                print(f"\nActual Output:")
                print(result.actual_output)
                
                if result.error_message:
                    print(f"\nError Message:")
                    print(result.error_message)
            
            print("-"*70)
        
        print(f"\n{'='*70}")
        print(f"FINAL SCORE: {grading_result['score']:.2f}%")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    # Initialize grader
    grader = AutoGrader(time_limit=2.0)
    
    # Example test cases
    test_cases = [
    TestCase(input_data="5\n1 2 3 4 5\n", expected_output="15"),
    TestCase(input_data="3\n10 20 30\n", expected_output="60"),
    TestCase(input_data="4\n-1 -2 -3 -4\n", expected_output="-10"),
]

    
    # Grade a student's code
    student_file = "student_solution.py"  # or .c, .cpp, .java
    
    if os.path.exists(student_file):
        result = grader.grade(student_file, test_cases)
        grader.print_report(result, student_file)
    else:
        print(f"File {student_file} not found!")