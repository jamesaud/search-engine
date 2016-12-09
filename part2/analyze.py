from __future__ import print_function, division
import sys, re
from io import open


class Analyze(object):
    def __init__(self, document):
        self.document = document
        self.words = self.count_words(document)
        self.letters = self.count_letter(document)
        self.sentences = self.count_sentences(document)
        self.syllables = self.count_syllables(document)
        self.cl = self.coleman_score(self.letters, self.words, self.sentences)
        self.fk = self.fk_score(self.syllables, self.words, self.sentences)

    """
    Counts the number of words in a document
    :param document: String, The name of the document
    :return: int, # of words in document
    """
    @classmethod
    def count_words(cls, document):
        return(len(cls.find_words(document)))


    """
    Finds the words in a document
    :param document: String, The name of the document
    :return: list[String], the words in document
    """
    @staticmethod
    def find_words(document):
        words = None
        with open(document, encoding='utf-8') as doc:
            words = doc.read().replace(".",'').split()
        return words


    """
    Counts the number of sentences in a document
    :param document: String, The name of the document
    :return: int, # of sentences in document
    """
    @staticmethod
    def count_sentences(document):
        read = None
        with open(document, encoding='utf-8') as doc:
            read = doc.read()
        sentences = re.findall(r'[\.|!|?] [A-Z]', read)
        return len(sentences)

    """
    Counts the number of letterswords in a document
    :param document: String, The name of the document
    :return: int, # of letters in document
    """
    @staticmethod
    def count_letter(document):
        read = None
        with open(document, encoding='utf-8') as doc:
            read = doc.read()
        letters = re.findall('[a-z|A-Z]', read)
        return len(letters)




    """
    Calculates the syllables in a string
    :param string: String, the string to find syllables in
    :return: int, the number of syllables found
    """
    @classmethod
    def count_syllables(cls, document):
        # count_vowels: returns int, the number of vowels. Ignores e at the end of word, unless it's the only vowel
        def count_vowels(word):
            count = 0
            for char in word:
                if char in 'aeiou':
                    count += 1

            # Ignore e if it is the last letter, unless it's the only letter
            if count > 1 and word[-1] == 'e':
                count -= 1
            return count

        # count_dipthongs: returns int, the number of dipthongs
        def count_dipthongs(word):
            return len(re.findall(r'[a|e|i|o|u]{2,}', word.lower()))

        count_vowels('helloe')
        count_vowels('mdke')
        words = cls.find_words(document)
        syllable_count = sum([(count_vowels(word) - count_dipthongs(word)) for word in words])
        return syllable_count

    

    """
    Calculates the Coleman Index, the US grade level to understand the document
    :param letter_count: int, the number of letters in the document
    :param word_count: int, the number of words in the document
    :param sentence_count: int, the number of sentences in the document
    :return: int, the Coleman-Liau index
    """
    @staticmethod
    def coleman_score(letter_count, word_count, sentence_count):
        try:
            return (5.88 * (letter_count/word_count)) - (29.6 * (sentence_count/word_count)) - 15.8
        # Set to almost zero if zero div error occurs
        except ZeroDivisionError:
            if word_count == 0:
                word_count = .0001
            return (5.88 * (letter_count/word_count)) - (29.6 * (sentence_count/word_count)) - 15.8
        
    """
    Calculates the Flesch-Kincaid Score, a metric of US grade level to understand the document
    :param syllable_count: int, the number of letters in the document
    :param word_count: int, the number of words in the document
    :param sentence_count: int, the number of sentences in the document
    :return: int, the Flesch index
    """
    @staticmethod
    def fk_score(syllable_count, word_count, sentence_count):
        try:
            return (.39 * (word_count/sentence_count)) + (11.8 * (syllable_count/word_count)) - 15.59
        # Set to almost zero if zero div error occurs
        except ZeroDivisionError:
            if sentence_count == 0:
                sentence_count = .0001
            if word_count == 0:
                word_count = .0001
            return (.39 * (word_count/sentence_count)) + (11.8 * (syllable_count/word_count)) - 15.59

    """
    Prints stats about the document
    """
    def print_stats(self):
        print("Number of Words:", self.words)
        print("Number of Sentences:", self.sentences)
        print("CL Level:", self.cl)
        print("Number of Syllables:", self.syllables)
        print("FK Level:", self.fk)


#location = 'part1_test_documents/violin_en.txt'
#a = Analyze(location)
#a.print_stats()
if __name__ == '__main__':
    try:
        del sys.argv[0] # Delete the file name from the args
        location = sys.argv[0] # Get the first real arg, the name of the file to analyze
    except IndexError:
        raise ValueError ("Please specify a file in the command arg, like: 'python analyze.py myfile.txt'")

    try:
        a = Analyze(location)
        a.print_stats()
    except IOError as e:
        raise IOError("Please enter a correct file. Python says: '" + str(e)+"'")