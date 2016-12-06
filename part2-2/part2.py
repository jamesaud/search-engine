from __future__ import print_function
import os
import math
from collections import Counter
from collections import defaultdict
from io import open

"""
Category is a representation of a document cateogry, such as 'business' or 'entertainment'.
"""
class Category(object):
    """
    :param name: String, name of the category
    :param document: String, the path of the document
    :attr word_scores: Counter, the dictionary of {word:score} of the words in the document
    :attr word_counts: Dict, a dictionary of {word:count} as {str:int} of the word and its count in the doc.
    """
    def __init__(self, name):
        self.word_counts = Counter()
        self.name = name
        self.word_scores = Counter()  # Scores, comparative to the other categories

    def train(self, document):
        self.word_counts.update(self.count_words(document))


    """
    Counts the number of occurences of all words in the document
    :param document: String, the path of the document
    :return: Counter, the dictionary of {word:count}
    """
    @staticmethod
    def count_words(document):
        with open(document, encoding='utf-8') as doc:
            words = doc.read().replace(".","").split()
        return Counter(words)

    """
    Gets the score of a word
    :param word: String, the word to get the score of
    :return: float, the score associated with the word
    """
    def find_score(self, word):
        return self.word_scores.get(word, 0)


"""
Training corpus is a representaion of a search data trainer. First you provide the documents it will train on.
 Then, you can provide documents to run against your test data.
"""
class TrainingCorpus:
    """
    :param categories: Category objects
    :attr word_total: - The total counts of all occurrences of a word in all documents {word:total_count}
    """
    def __init__(self, *categories):
        self.category_list = categories
        self.word_total = self._join_categories(categories)  # Total count of all the words
        self._calculate_categories_scores()  # Updates the category objects with the word scores

    """
    Returns a Counter (dictionary) of the total occurences of all words in the given categories
    :param category_lst: List[Category], a list of categories to operate on
    """
    @staticmethod
    def _join_categories(category_list):
        word_total = Counter()
        for category in category_list:
            word_total.update(category.word_counts)
        return word_total

    """
    Calculates the word scores in each category and updates those objects accordingly with the search calculation formula.
    """
    def _calculate_categories_scores(self):
        # Calculates the word scores and updates a single Category object
        def _calculate_category_scores(category): # Takes a Category object to calculate scores for
            for word in category.word_counts:
                if self.word_total[word] - category.word_counts[word] == 0: # Prevents doing log(0)
                    category.word_scores[word] = math.log(category.word_counts[word])
                else:
                    category.word_scores[word] = math.log(category.word_counts[word]) - math.log(self.word_total[word] - category.word_counts[word])
            return None

        # Updates the words scores in each Category object
        for category in self.category_list:
            _calculate_category_scores(category)
        return None

    """
    Calculates a document score by running it against the test data
    :param document: String, path to the document
    """
    def document_score(self, document):
        doc = Document(document)
        for word in doc.words:
            for category in self.category_list:
                doc.update_score(category.name, category.find_score(word), word)
        return doc


"""
Document represents a document that you want to compute against the test data.
"""
class Document:
    """
    :param path: String, the path to the document
    :attr self.words: List, a list of all the words in the document [String, ...]
    :attr self.category_scores: Dict, a dictionary of the {category_name:score} - {String:Float}
    :attr informative_words: List[Tuple], a list of the 5 most informative words with their scores [(score, word), ...]\
                                                                                                   [(Float, String)...]
    """
    def __init__(self, path):
        self.words = self._get_words(path)
        self.category_scores = defaultdict(lambda: 0)  # Set default score to 0 for any word
        self.informative_words = [(float('-inf'), 'fakename')]  # num, word

    """
    Gets the words in a document
    :param path: String, the path to the document
    :return: List, a list of all the words found
    """
    @staticmethod
    def _get_words(path):
        words = None
        with open(path, encoding='utf-8') as file:
            words = file.read().replace('.','').split()
        return words


    def update_score(self, category, score, word):
        self.category_scores[category] += score


        # Trying to calculate the top informative words, must change
        if len(self.informative_words) == 5:
            self.informative_words.sort()
            if score > self.informative_words[0][0] and word not in [item[1] for item in self.informative_words]:
                self.informative_words[0] = (score, word)
        else:
            self.informative_words.append((score, word))

def main():
    # MAIN
    # Create Category Objects for each type
    business = Category('business')
    business.train('part2_corpus2/part2_train/business.txt')
    entertainment = Category('entertainment')
    entertainment.train( 'part2_corpus2/part2_train/entertainment.txt')
    health = Category('health')
    health.train('part2_corpus2/part2_train/health.txt')
    scitech = Category('scitech')
    scitech.train('part2_corpus2/part2_train/scitech.txt')
    sports = Category('sports')
    sports.train('part2_corpus2/part2_train/sports.txt')
    world = Category('world')
    world.train('part2_corpus2/part2_train/world.txt')

    # Create the Training Object based on these categories
    tc = TrainingCorpus(business, entertainment, health, scitech, sports, world)

    document = 'part2_corpus2/part2_test/business-1.txt'
    print("Analyzing", document)
    # Calculate and get the Document object from the test document
    doc = tc.document_score(document)

    # Get the category scores from the Document object
    scores = doc.category_scores


    # Get the scores from the document object, sorted by the score itself
    sorted_keys = sorted(scores, key=scores.get, reverse=True)

    print("Category Scores:")
    # Print the scores for each cateogry
    for key in sorted_keys:
        print(key, ':', scores[key])

    print()

    print("Important Words:")
    # Get the informative words from the Document object
    for item in doc.informative_words:
        print(item)


# Should be a path containing category folders
def main2(base_path_train, base_path_test):

    # Return Category object from full folder path containing docs
    # String, Category -> Category
    def train_category_from_folder(folder):
        # Get list of folders, prevent hidden files from showing up
        files = [file for file in os.listdir(folder)]
        category = Category(os.path.basename(folder))  # Create new category object, named with the folder name

        for file in files:
            # Try except to catch unicode errors for strange files
            try:
                category.train(os.path.join(folder, file))
            except UnicodeDecodeError:
                print("Unicode Error, Skipping", file)
        return category

    # Get folder in the path
    def get_folders(path):
        # Get list of folders, prevent hidden folders from showing up
        return [file for file in os.listdir(path) if
         os.path.isdir(os.path.join(path, file)) & (file[0] != '.')]

    # Returns a list of Document objects that are tested against the training corpus
    def test_files_in_folder(folder, training_corpus):
        tc = training_corpus
        files = [file for file in os.listdir(folder)]
        trained_docs = []
        for file in files:
            try:
                file_path = os.path.join(folder, file)
                trained_docs.append(tc.document_score(file_path)) # Appends the Document object
            except UnicodeDecodeError:
                print("Unicode Error, Skipping", file_path)
        return trained_docs

        # Takes in a dictionary of {folder_name: List of Document} and prints how many documents match in each category

    def make_docs_categories(category_doc):
        category_counts = []  # List of Tuples [(category_name, {cateogry_name:count...}))]
        # the number of docs appearing in which categories, for that category of tests.
        for c_name, c_docs in category_doc.items():
            c_counts = defaultdict(lambda: 0)
            for doc in c_docs:
                scores_dict = doc.category_scores
                category_score_min = max(scores_dict, key=scores_dict.get)  # Get the document it matches with the most
                c_counts[category_score_min] += 1  # Add one to the category count if the doc matches it

            category_counts.append((c_name, c_counts))  # Add tuple of category and its doc counts for each cateogry
        return category_counts

    # Main code for the main2() function
    folders = get_folders(base_path_train)
    category_list = []  # List of category objects

    # Train with the text files, add categories to the category list
    for folder in folders:
        folder_path = os.path.join(base_path_train, folder)
        category_list.append(train_category_from_folder(folder_path))


    # Test against the test documents make sure they return the correct category
    tc = TrainingCorpus(*category_list) # Train using the categories that were created.
    test_folders = get_folders(base_path_test) # Get list of folders to look through
    category_docs = {} # {folder_name: List of Document} to see if they all fit the correct cateogry

    for folder in test_folders:
        folder_path = os.path.join(base_path_test, folder)
        documents = test_files_in_folder(folder_path, tc) # list of trained Document objects
        category_docs[folder] = documents # Set key, value of dictionary


    doc_cats = make_docs_categories(category_docs) # Get dictionary of the category, and how many testing docs match it
    print('\n\n' + '-'*50)
    print("Key is Category Name, Value is the number of documents that matched to that category.")
    for category, matches in doc_cats: # Print the
        print('Documents in the category >', category, '< actually matched with the categories: ')
        print(str(dict(matches))) # Turn default dict to dict for easy printing
        print()

if __name__ == '__main__':
    train_path = os.path.join(os.getcwd(), 'part2_corpus2/bbc-train')
    test_path = os.path.join(os.getcwd(), 'part2_corpus2/bbc-test')
    print("Training with a single document:")
    main()
    print("\n\nTraining against huge document base, 70% for training 30% for testing:")
    main2(train_path, test_path)
