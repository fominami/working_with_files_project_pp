from sympy import sympify, SympifyError
import re

class DataProcessor:
    def __init__(self, data):
        self.data = data
#Обработка с библиотекой
    def process_text_library(self):
        processed_data = []
        expression = ''
        inside_expression = False

        i = 0
        while i < len(self.data):
            char = self.data[i]
            if char.isdigit() or char in '+-*/().':
                if not inside_expression:
                    inside_expression = True
                    expression += char
                else:
                    expression += char
            else:
                if inside_expression:
                    try:
                        result = sympify(expression)
                        processed_data.append(str(result))
                    except SympifyError:
                        processed_data.append(expression)  
                    expression = ''
                    inside_expression = False
                processed_data.append(char)
            i += 1

        
        if inside_expression and expression:
            try:
                result = sympify(expression)
                processed_data.append(str(result))
            except SympifyError:
                processed_data.append(expression)

        return ''.join(processed_data)
    
    #Без регулярных выражений 
    
    def process_text_without_regex(self):
        processed_data = []
        expression = ''
        inside_expression = False

        i = 0
        while i < len(self.data):
            char = self.data[i]
            if char.isdigit() or char in '+-*/().':
                if not inside_expression:
                    inside_expression = True
                    expression += char
                else:
                    expression += char
            else:
                if inside_expression:
                    try:
                        result = self.evaluate_expression(expression)
                        processed_data.append(str(result))
                    except Exception as e:
                        processed_data.append(expression) 
                    expression = ''
                    inside_expression = False
                processed_data.append(char)
            i += 1

        
        if inside_expression and expression:
            try:
                result = self.evaluate_expression(expression)
                processed_data.append(str(result))
            except Exception as e:
                processed_data.append(expression)

        return ''.join(processed_data)

    def evaluate_expression(self, expression):
        def precedence(op):
            if op in ('+', '-'):
                return 1
            if op in ('*', '/'):
                return 2
            return 0


        def greater_precedence(op1, op2):
            return precedence(op1) >= precedence(op2)

        def shunting_yard(expression):
            stack = []
            output = []
            number = ''
            for char in expression:
                if char.isdigit() or char == '.':
                    number += char
                else:
                    if number:
                        output.append(float(number))
                        number = ''
                    if char in '+-*/':
                        while (stack and stack[-1] != '(' and greater_precedence(stack[-1], char)):
                            output.append(stack.pop())
                        stack.append(char)
                    elif char == '(':
                        stack.append(char)
                    elif char == ')':
                        while stack and stack[-1] != '(':
                            output.append(stack.pop())
                        stack.pop()
            if number:
                output.append(float(number))
            while stack:
                output.append(stack.pop())
            return output

        tokens = shunting_yard(expression)
        return self.evaluate_postfix(tokens)

    def evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                result = self.apply_op(a, b, token)
                stack.append(result)
        return stack[0]

    def apply_op(self, a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ValueError("Деление на ноль.")
            return a / b
        

    #Обработка с использованием регулярного выражения
    def process_text_with_regex(self):
        pattern = re.compile(r'\([^()]+\)')
        while re.search(pattern, self.data):
            self.data = re.sub(pattern, self.replace_expression, self.data)
        final_pattern = re.compile(r'\d+(\.\d+)?(?:[\+\-\*/]\d+(\.\d+)?)*')
        self.data = re.sub(final_pattern, self.replace_expression, self.data)

        return self.data

    def replace_expression(self, match):
        expression = match.group(0)
        try:
            result = sympify(expression)
            return str(result)
        except SympifyError:
            print(f"Не удалось обработать выражение: {expression}")
            return expression







