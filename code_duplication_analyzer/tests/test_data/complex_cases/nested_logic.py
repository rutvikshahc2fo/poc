def wrapper_function(a, b):
    def inner_sum(x, y):
        return x + y

    total = inner_sum(a, b)
    return total


class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, x, y):
        result = 0
        for _ in range(y):
            result += x
        return result