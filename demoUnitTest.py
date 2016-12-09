import unittest

def pagerank(graph):
    prank = dict()
    #TODO: implement pagerank algorithm
    return prank

def create_test_graph():
    pass


class TestInput(unittest.TestCase):
    def test_empty_graph(self):
        pass

    def test_none(self):
        pass

class TestStopCondition(unittest.TestCase):
    def setUp(self):
        self._test_graph = create_test_graph()

    def test_non_stop(self):
        pass
    
    def test_stop(self):
        pass

    def tearDown(self):
        self._test_graph = None


iff __name__ == '__main__':
    unittest.main()
