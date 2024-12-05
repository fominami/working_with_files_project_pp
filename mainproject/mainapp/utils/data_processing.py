import re
import numexpr as ne

class DataProcessor:
    def __init__(self, data):
        self.data = data

#методы для обработки выражений без регулярных выражений(обратная польская запись)
    def tokenize(self, data):
        tokens = []
        number = ''
        i = 0
        while i < len(data):
            char = data[i]
            if char.isdigit() or (char == '.' and number and not number[-1] == '.'):
                number += char
            else:
                if number:
                    tokens.append(number)
                    number = ''
                if char in '+-*/()':
                    tokens.append(char)
                elif char == '.':
                    if i + 1 < len(data) and data[i + 1].isdigit():
                        number += char
                    else:
                        tokens.append(char)
            i += 1
        if number:
            tokens.append(number)
        return tokens

    def higher_precedence(self, op1, op2):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        return precedence[op1] >= precedence[op2]

    def infix_to_postfix(self, tokens):
        output = []
        operators = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if token.isdigit() or '.' in token:
                output.append(token)
            elif token in precedence:
                while (operators and operators[-1] != '(' and
                    self.higher_precedence(operators[-1], token)):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()


        while operators:
            output.append(operators.pop())

        return output

    def evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token.isdigit() or '.' in token:
                stack.append(float(token))
            else:
                if len(stack) < 2: 
                    raise ValueError("Ошибка в выражении: некорректный синтаксис")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0: 
                        raise ValueError("Ошибка в выражении: деление на ноль")
                    stack.append(a / b)
        if len(stack) != 1:
            raise ValueError("Ошибка в выражении: некорректный синтаксис")

        return stack[0]

    def process_without_regex(self):
        while True:
         initial_data = self.data
         math_expressions = self.extract_math_expressions(self.data)
         for expr_tuple in math_expressions:
             expr = expr_tuple[0]
             tokens = self.tokenize(expr)
             postfix_tokens = self.infix_to_postfix(tokens)
             result = self.evaluate_postfix(postfix_tokens)
             self.data = self.data.replace(expr, str(result))
         if self.data == initial_data:
            break
        return self.data

# методы для работы с библиотекой numexpr 
    def extract_math_expressions(self, data):
        pattern = re.compile(r'(\b\d+(\.\d+)?(?:[\+\-\*/\(\)])*\d+(\.\d+)?\b)')
        return pattern.findall(data)


    def process_with_library(self):
        while True:
            initial_data = self.data
            math_expressions = self.extract_math_expressions(self.data)

            for expr_tuple in math_expressions:
                expr = expr_tuple[0]
                try:
                    result = ne.evaluate(expr)
                    self.data = self.data.replace(expr, str(result))
                except Exception as e:
                    print(f"Error processing expression '{expr}': {e}")
                    pass  
            if self.data == initial_data:
                break

        return self.data
