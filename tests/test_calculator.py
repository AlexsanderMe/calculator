import unittest
from app.utils import evaluate_expression

class TestCalculator(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(evaluate_expression("1+1"), 2)
        self.assertEqual(evaluate_expression("2*2"), 4)
        self.assertEqual(evaluate_expression("6/3"), 2)
        self.assertEqual(evaluate_expression("5.5-3.2"), 2.3)

    def test_implicit_multiplication(self):
        self.assertEqual(evaluate_expression("2x=4"), [2])

    def test_percentage(self):
        self.assertEqual(evaluate_expression("100+10%"), 110)
        self.assertEqual(evaluate_expression("100-10%"), 90)
        self.assertEqual(evaluate_expression("100*10%"), 10)
        self.assertEqual(evaluate_expression("100/10%"), 1000)

if __name__ == '__main__':
    unittest.main()
