import re
from sympy import symbols, Eq, solve, sympify

def evaluate_expression(expression):
    expression = expression.replace('−', '-')
    if 'x' in expression:
        x = symbols('x')
        lhs, rhs = expression.split('=')
        lhs = add_implicit_multiplication(lhs)
        rhs = add_implicit_multiplication(rhs)
        lhs = sympify(lhs, locals={'x': x})
        rhs = sympify(rhs, locals={'x': x})
        eq = Eq(lhs, rhs)
        result = solve(eq, x)
    elif '%' in expression:
        result = solve_percentage(expression)
    else:
        result = eval(expression)
    if str(result).endswith('.0'):
        result = int(str(result).replace('.0', ''))
    return result

def add_implicit_multiplication(expression):
    return re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)

def solve_percentage(expression):
    pattern = r'(\d+(?:\.\d+)?)([+\-*/])(\d+(?:\.\d+)?)%'
    while re.search(pattern, expression):
        expression = re.sub(pattern, replace_percentage, expression)
    try:
        result = eval(expression)
    except:
        try:
            expression = re.sub(r'(\d+(?:\.\d+)?)%', calculate_percentage, expression)
            result = eval(expression)
        except Exception as e:
            raise ValueError(f"Erro na avaliação da expressão: {e}")
    return result

def replace_percentage(match):
    number = float(match.group(1))
    operator = match.group(2)
    percentage = float(match.group(3))
    
    if operator == '+':
        return str(number + (number * (percentage / 100)))
    elif operator == '-':
        return str(number - (number * (percentage / 100)))
    elif operator == '*':
        return str(number * (percentage / 100))
    elif operator == '/':
        return str(number / (percentage / 100))
    return match.group(0)

def calculate_percentage(match):
    value = float(match.group(1))
    return str(value / 100)
