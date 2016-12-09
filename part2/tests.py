import unittest
import analyze as part1
import math

# Part 1 Unit Tests
class AnalyzeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_name = 'unittest_docs/testdoc.txt'
        cls.analyzer = part1.Analyze('unittest_docs/testdoc.txt')
        
    def test_count_words(self):
        assert self.analyzer.count_words(self.file_name) == 34

    def test_find_words(self):
        # Should return a list of words
        assert len(self.analyzer.find_words(self.file_name)) == 34 

    def test_count_sentences(self):
        assert self.analyzer.count_sentences(self.file_name) == 1

    def test_count_letter(self):
        assert self.analyzer.count_letter(self.file_name) == 196 

    # Difficult to get an exact number to test for
    def test_count_syllables(self):
        pass

    def test_coleman(self):
        assert round((self.analyzer.coleman_score(80, 15, 3)), 2) == 9.64

        # Test for division by 0 errors
        assert self.analyzer.coleman_score(0, 0, 0) < -15.58

    def test_fk(self):
        assert round((self.analyzer.fk_score(80, 15, 3)), 2) == 49.29
        
        # Test for division by 0 errors
        assert self.analyzer.fk_score(0, 0, 0) < -15
        
def main():
    unittest.main()

if __name__ == '__main__':
    main() 
