import re 
from sympy import sympify, SympifyError

class DataProcessor:
    def __init__(self,data):
        self.data=data
    def extract_math_expressions(self, data): 
        # Используем регулярные выражения для извлечения математических выражений 
        pattern = re.compile(r'(\d+\s*[\+\-\*/]\s*\d+)') 
        return pattern.findall(data)
    def process_with_library(self): 
        math_expressions = self.extract_math_expressions(self.data) 
        for expr in math_expressions:
            try:
                result = sympify(expr) 
                self.data = self.data.replace(expr, str(result)) 
            except SympifyError: 
                pass
            
        return self.data