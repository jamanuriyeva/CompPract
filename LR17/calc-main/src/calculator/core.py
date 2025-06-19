import datetime
import math
from tabulate import tabulate

PARAMS = {
    'precision': None,
    'output_type': None,
    'possible_types': None,
    'dest': None
}

def load(file="params.ini"):
    """Перенос из текстового файла в словарь"""
    global PARAMS, SETTINGS
    with open(file, mode='r', errors='ignore') as f:
        lines = f.readlines()

    for line in lines:
        key, val = line.strip().split('=')
        if key != 'dest':
            val = eval(val)
        if file == "params.ini":
            PARAMS[key] = val

def write_log(*args, action=None, result=None, file='calc-history.log.txt'):
    """Запись истории в файл"""
    with open(file, mode='a', errors='ignore') as f:
        date = datetime.datetime.today()
        args_lst = list(args)
        if len(args_lst) == 1:
            f.write(
                f'Дата: {date.strftime("%d/%m/%Y")}    Время:{date.strftime("%H:%M:%S")} \n{action}: {args_lst[0]} = {result} \n\n')
        else:
            f.write(
                f'Дата: {date.strftime("%d/%m/%Y")}    Время: {date.strftime("%H:%M:%S")} \nОперация: {args[0]} {action} {args[1]}  = {result} \n\n')

def print_results(*args, action=None, result=None):
    """Красивый вывод через tabulate"""
    lst = list(args)
    if len(args) == 1:
        t_value = [lst, [action], [result]]
        t_description = ['Числа', 'Операция', 'Результат']
    else:
        t_value = [[lst[0]], [action], [lst[1]], [result]]
        t_description = ['Число 1', 'Операция', 'Число 2', 'Результат']

    d = {t_description[i]: t_value[i] for i in range(len(t_description))}
    print(tabulate(d, headers="keys", tablefmt="pretty"))

def convert_precision():
    """Определение количества знаков после запятой"""
    val = float(PARAMS['precision'])
    # Ограничим число знаков после запятой: округлим и сравним
    for i in range(16):
        if round(val, i) == val:
            return i
    return 15  # максимум

def product(args):
    """Приведение к заданной точности"""
    ndigits = convert_precision()
    return round(args, ndigits)

def Calculator(op1, op2, act):
    """Калькулятор с действиями"""
    if act == "+": r = op1 + op2
    elif act == "-": r = op1 - op2
    elif act == "*": r = op1 * op2
    elif act == "/": r = op1 / op2 if op2 != 0 else "Деление на ноль не реализуется"
    elif act == "^": r = "Возведение 0 в отрицательную степень не реализуется" if op1 == 0 and op2 < 0 else op1 ** op2
    elif act == "//": r = op1 // op2
    elif act == "%": r = op1 % op2
    else: r = "Операция не распознана"

    write_log(op1, op2, action=act, result=r)
    print_results(op1, op2, action=act, result=r)
    return

def standard_deviation():
    """Среднеквадратичное отклонение с заданной точностью"""
    try:
        number_count = int(input("Введите количество числел: "))
        if number_count <= 1:
            print("Введите количество значений больше одного")
            return
        args_list = [float(input(f'Введите {i} число: ')) for i in range(1, number_count + 1)]
    except ValueError:
        print('Проверьте вводимые значение на правильность: вводить необходимо целые числа')
        return

    x_mean = sum(args_list) / len(args_list)
    s_d = math.sqrt(sum((y - x_mean) ** 2 for y in args_list) / len(args_list))
    result = round(s_d, convert_precision(PARAMS['precision']))

    write_log(args_list, action='Среднеквадратичное отклонение', result=result)
    print_results(args_list, action='Среднеквадратичное отклонение', result=result)

def main():
    load("params.ini")

    print("""
Калькулятор с действиями

  '+' - Сложение;
  '-' - Вычитание;
  '*' - Умножение;
  '/' - Деление;
  '^' - Возведение в степень;
  '//' - Деление без остатка;
  '%' - Деление по модулю; 
""")
    try:
        operand1 = int(input("Оператор 1: "))
        operand2 = int(input("Операнд 2: "))
        sign = input("Оператор: ")
    except ValueError:
        print('Проверьте вводимые значение на правильность: вводить необходимо числа')
        return

    Calculator(operand1, operand2, sign)
    print("\nПоиск среднеквадратичного отклонения\n")
    standard_deviation()

