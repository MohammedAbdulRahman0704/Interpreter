import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from scanner import Scanner
from interpreter_token import TokenType

class ScannerTest(unittest.TestCase):
    def test_empty_file(self):
        scanner = Scanner("")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

if __name__ == '__main__':
    unittest.main()