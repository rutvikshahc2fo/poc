def calculate_interest(principal, rate, time):
    """Compute simple interest"""
    return (principal * rate * time) / 100


def compute_area_circle(radius):
    pi = 3.14159
    return pi * (radius ** 2)


def sum_values(values):
    """Sum numeric values in a list"""
    total = 0
    for v in values:
        total += v
    return total


def product(values):
    result = 1
    for v in values:
        result *= v
    return result