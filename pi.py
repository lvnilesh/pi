import math
from decimal import Decimal, getcontext

def calculate_pi_ramanujan(iterations, precision):
    """
    Calculates an approximate value of pi using Ramanujan's formula.
    Formula: 1/pi = (2*sqrt(2)/9801) * sum_{k=0 to infinity} [(4k)! * (1103 + 26390k)] / [(k!)^4 * 396^(4k)]

    Args:
        iterations (int): The number of terms to sum (k from 0 to iterations-1).
                          Even 1 iteration provides remarkable accuracy.
        precision (int): The number of decimal places for the calculation.
                         The 'decimal' context will be set to this precision + a buffer.

    Returns:
        Decimal: The approximate value of pi calculated to the specified precision.
    """
    # Set the precision for Decimal calculations.
    # Add a buffer (e.g., 5 or 10) to ensure intermediate calculations
    # don't lose precision before the final rounding.
    getcontext().prec = precision + 10 

    sum_val = Decimal(0)

    # Constant part outside the sum: (2 * sqrt(2)) / 9801
    # Ensure all numbers are Decimals for high precision
    constant_multiplier = (Decimal(2) * Decimal(2).sqrt()) / Decimal(9801)

    # Loop to sum the terms from k=0 up to (iterations - 1)
    for k in range(iterations):
        # Calculate the numerator part of the sum term: (4k)! * (1103 + 26390k)
        numerator_factorial = Decimal(math.factorial(4 * k))
        numerator_linear = Decimal(1103 + 26390 * k)
        numerator_term = numerator_factorial * numerator_linear

        # Calculate the denominator part of the sum term: (k!)^4 * 396^(4k)
        denominator_factorial_pow = Decimal(math.factorial(k))**4
        denominator_power_term = Decimal(396)**(4 * k)
        denominator_term = denominator_factorial_pow * denominator_power_term

        # Calculate the current term and add it to the total sum
        current_term = numerator_term / denominator_term
        sum_val += current_term

    # The formula calculates 1/pi, so we need to take the reciprocal to get pi
    one_over_pi = constant_multiplier * sum_val
    pi_approx = Decimal(1) / one_over_pi

    # Return the result, potentially rounding to the exact desired precision
    return pi_approx.quantize(Decimal('1e-{}'.format(precision)))

if __name__ == "__main__":
    print("--- Pi Calculator using Ramanujan's Formula ---")
    print("This formula converges extremely fast!")
    print("Even 1 or 2 iterations will give many correct digits.")

    try:
        # Get user input for iterations and precision
        num_iterations = int(input("\nEnter the number of iterations (e.g., 1 for ~30 digits, 2 for ~60 digits): "))
        if num_iterations < 1:
            print("Number of iterations must be at least 1.")
            exit()

        desired_precision = int(input("Enter the desired precision (number of decimal places, e.g., 50, 100, 200): "))
        if desired_precision < 1:
            print("Precision must be at least 1.")
            exit()

        # Perform the calculation
        calculated_pi = calculate_pi_ramanujan(num_iterations, desired_precision)

        print(f"\n--- Results ---")
        print(f"Pi approximated with {num_iterations} iterations and {desired_precision} digits of precision:")
        print(f"Calculated Pi: {calculated_pi}")

        # For comparison, let's include a known value of Pi to high precision
        # (Copied from a reliable source like Wikipedia for the first 100 digits)
        known_pi_str = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
        
        # Ensure the known pi string is also a Decimal and trimmed to the desired precision
        # Add 2 for "3." part
        known_pi = Decimal(known_pi_str[:min(len(known_pi_str), desired_precision + 2)]) 
        print(f"Known Pi       : {known_pi}")

        # Calculate and display the absolute error
        error = abs(calculated_pi - known_pi)
        print(f"Absolute Error : {error}")

    except ValueError:
        print("Invalid input. Please enter integer numbers for iterations and precision.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")