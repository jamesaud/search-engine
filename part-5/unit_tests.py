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

    def test_get_url(self):
        index = os.path.join(os.getcwd(), 'pages/index.dat')
        url = TC.get_url('1.html', index)
        self.assertEquals('http://bloomington.craigslist.org/apa/5839062999.html', url)


    def test_get_title(self):
        html = '<title>hello</title>'
        title = TC.get_title(html)
        self.assertEquals(title, 'hello')

if __name__ == "__main__":
    unittest.main()