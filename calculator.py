"""Simple command-line calculator.

Supports addition, subtraction, multiplication and division.
"""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return a minus b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return a divided by b, rounded to 2 decimal places.

    Raises ValueError with a friendly message when b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return round(a / b, 2)


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a, op, b):
    """Apply the operator op to a and b."""
    if op not in OPERATIONS:
        raise ValueError(f"Unsupported operator: {op}")
    return OPERATIONS[op](a, b)


def main():
    print("Simple Calculator (type 'q' to quit)")
    while True:
        expr = input("Enter expression (e.g. 8 / 2): ").strip()
        if expr.lower() == "q":
            break
        try:
            a, op, b = expr.split()
            print("Result:", calculate(float(a), op, float(b)))
        except ValueError as err:
            print("Error:", err)


if __name__ == "__main__":
    main()
