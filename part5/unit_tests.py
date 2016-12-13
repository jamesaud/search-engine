import TextCleaner as TC
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

    def test_get_urls(self):
        index = os.path.join(os.getcwd(), 'pages/index.dat')
        url = TC.get_urls(index)
        self.assertEquals('http://bloomington.craigslist.org/apa/5839062999.html', url['1.html'])


    def test_get_title(self):
        html = 'test.html'
        title = TC.get_title(html)
        self.assertEquals(title, 'hello')

        
    def test_remove_stopwords(self):
        tokens = ("i ate his chicken sandwich all by myself and then i flew to the moon").split()
        tokens = TC._remove_stopwords(tokens)
        remove_stopwords = ("ate chicken sandwich flew moon".split())
        self.assertEquals(tokens, remove_stopwords)


if __name__ == "__main__":
    unittest.main()
