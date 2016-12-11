import TextCleaner as TC
from DocSearch import DocSearch, Doc
import unittest
import os

class TextCleanerTests(unittest.TestCase):

    def setUp(self):
        self.text = 'This is some test text, in order to test the code in this suite. There is some quotation ;...' \
                    'randomly 3&^ 4 as003 added. 33:22 : | akdfo fantasizing going added best'
        self.split_text = self.text.split()

    def test_stemm(self):
        stems = TC._stemm(['bears', 'beats', 'hated', 'going'])
        no_stems = ['bear', 'beat', 'hate', 'go']

        self.assertEquals(stems, no_stems)





class DocSearchTests(unittest.TestCase):

    def setUp(self):
        d1 = Doc('A')
        d2 = Doc('B')
        d3 = Doc('C')
        d1.docs=[d2,d3]
        d2.docs=[d3]
        d3.docs=[d1]
        self.DS = DocSearch()
        self.DS.docs += [d1, d2, d3]



    def test_page_rank_intialize(self):
        self.DS._initialize_page_rank()
        self.assertAlmostEqual(self.DS.docs[0].pagerank, .333333333333333)
        pass

    def test_page_rank(self):
        self.DS._initialize_page_rank()
        self.DS._page_rank()
        ls = [doc.pagerank for doc in self.DS.docs]
        print(ls)


if __name__ == "__main__":
    unittest.main()