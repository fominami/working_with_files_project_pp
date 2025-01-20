from django.test import SimpleTestCase
from mainapp.utils.data_processing import DataProcessor
class TestDataProcessing(SimpleTestCase):
    def test_processing_without_regex(self):
        data='hello 5+(8-4)/2+5*2'
        process = DataProcessor(data) 

        new_data=process.process_text_without_regex()

        self.assertEqual(new_data,"hello 17.0")
    def test_processing_without_regex_without_numbers(self):
        data='hello'
        process = DataProcessor(data) 

        new_data=process.process_text_without_regex()

        self.assertEqual(new_data,"hello")
    def test_processing_with_regex(self):
        data='Calculate ((2+3)*(7-2))+(10/(5-(3*1)))-4'
        process = DataProcessor(data) 

        new_data=process.process_text_with_regex()

        self.assertEqual(new_data,"Calculate 26")
        
    def test_processing_with_regex_without_numbers(self):
        data='hello'
        process = DataProcessor(data) 

        new_data=process.process_text_with_regex()

        self.assertEqual(new_data,"hello")
    def test_processing_with_library(self):
        data='hello 5+(8-4)/2+5*2'
        process = DataProcessor(data) 

        new_data=process.process_text_library()

        self.assertEqual(new_data,"hello 17")
    def test_processing_with_library_without_numbers(self):
        data='hello'
        process = DataProcessor(data) 

        new_data=process.process_text_library()

        self.assertEqual(new_data,"hello")
    
