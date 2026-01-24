def is_prime(n):
    # Prime numbers must be greater than 1
    if n <= 1:
        return False
    
    # Check for divisors from 2 up to the square root of n
    # (We use int(n**0.5) + 1 for efficiency)
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False  # Found a divisor, so it's not prime
            
    return True  # No divisors found, it's prime

n=int(input())
if is_prime(n):
    print("True")
else:
    print("False")