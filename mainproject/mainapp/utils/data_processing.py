import re
import numexpr as ne

class DataProcessor:
    def __init__(self, data):
        self.data = data

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
