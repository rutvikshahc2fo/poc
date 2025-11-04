def compute_total(items):
    total = 0
    for it in items:
        total += it['amount']
    return total


def helper_unique(a, b):
    return a + b
