def calculate_sum(records):
    total = 0
    for r in records:
        total += r['amount']
    return total

def helper_other(x, y):
    return x + y
