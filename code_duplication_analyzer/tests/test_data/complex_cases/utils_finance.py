def get_interest_amount(amount, percent, duration):
    """Similar to calculate_interest in utils_math"""
    return (amount * percent * duration) / 100


def compute_compound_interest(principal, rate, years):
    total = principal * ((1 + (rate / 100)) ** years)
    return total - principal


def total_sum(numbers):
    s = 0
    for n in numbers:
        s += n
    return s


def multiply_list(nums):
    """Same logic as product()"""
    result = 1
    for n in nums:
        result *= n
    return result