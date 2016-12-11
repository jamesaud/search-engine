import TextCleaner as TC
import unittest
import os

class TextCleanerTests(unittest.TestCase):

    def setUp(self):
        self.text = 'This is some test text, in order to test the code in this suite. There is some quotation ;...' \
                    'randomly 3&^ 4 as003 added. 33:22 : | akdfo fantasizing going added best'
        self.split_text = self.text.split()


if __name__ == "__main__":
    unittest.main()