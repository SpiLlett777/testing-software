import pytest
from app.calculator import Calculator


@pytest.mark.parametrize("method,a,b,expected", [
    ("add", 2, 3, 5), ("add", -2, -3, -5), ("add", .1, .2, .3),
    ("subtract", 5, 8, -3), ("subtract", -4, -4, 0), ("subtract", 0, 2, -2),
    ("multiply", 6, 7, 42), ("multiply", -2, 3, -6), ("multiply", 0, 999, 0),
    ("divide", 8, 2, 4), ("divide", 1, 4, .25), ("divide", -9, 3, -3),
    ("divide", 0, 5, 0), ("add", 10**12, 10**12, 2 * 10**12),
])
def test_arithmetic(method, a, b, expected):
    assert getattr(Calculator, method)(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a", [0, 1, -1, .5])
def test_division_by_zero(a):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        Calculator.divide(a, 0)


@pytest.mark.parametrize("number,expected", [(-7, False), (0, False), (1, False), (2, True), (3, True), (4, False), (9, False), (25, False), (97, True)])
def test_prime(number, expected):
    assert Calculator.is_prime_number(number) is expected


@pytest.mark.parametrize("value", [2.5, "3", None, True])
def test_prime_rejects_non_integer(value):
    with pytest.raises(TypeError):
        Calculator.is_prime_number(value)
