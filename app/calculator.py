import math


class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль запрещено.")
        return a / b

    @staticmethod
    def is_prime_number(n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Ожидается целое число.")
        if n < 2:
            return False
        return all(n % divisor for divisor in range(2, math.isqrt(n) + 1))
