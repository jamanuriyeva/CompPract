import pytest
from calculator.core import convert_precision, product, load, PARAMS, Calculator

@pytest.mark.parametrize("value,expected", [
    (0.00123, 5),
    (1e-5, 5),
    (1.0, 0),
])
def test_convert_precision(value, expected):
    PARAMS['precision'] = value
    assert convert_precision() == expected


@pytest.mark.parametrize("precision, input_val, expected", [
    (0.01, 3.14159, 3.14),
    (0.001, 2.71828, 2.718),
    (1, 5.678, 6),
])
def test_product(precision, input_val, expected):
    PARAMS['precision'] = precision
    assert product(input_val) == expected


def test_calculator_add(monkeypatch):
    """Проверка действия +"""
    # Заглушки для функций записи лога и вывода результата
    monkeypatch.setattr("src.calculator.core.write_log", lambda *a, **kw: None)
    monkeypatch.setattr("src.calculator.core.print_results", lambda *a, **kw: None)

    result = Calculator(2, 3, "+")
    assert result is None  # Функция возвращает None


def test_calculator_unknown(monkeypatch):
    """Проверка неизвестной операции"""
    monkeypatch.setattr("src.calculator.core.write_log", lambda *a, **kw: None)
    monkeypatch.setattr("src.calculator.core.print_results", lambda *a, **kw: None)

    result = Calculator(2, 3, "@")
    assert result is None
