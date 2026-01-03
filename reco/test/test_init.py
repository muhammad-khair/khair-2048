import unittest

from reco.src import get_recommender
from reco.src.heuristic import HeuristicRecommender


class TestRecommenderFactory(unittest.TestCase):
    def test_recommender_factory(self):
        reco = get_recommender("heuristic")
        self.assertIsInstance(reco, HeuristicRecommender)

if __name__ == '__main__':
    unittest.main()
