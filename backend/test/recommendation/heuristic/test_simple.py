import unittest

from src.recommendation.heuristic.simple import SimpleHeuristicRecommender


class TestSimpleHeuristicRecommender(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

    def test_heuristic_recommender(self):
        recommender = SimpleHeuristicRecommender()
        move, rationale = recommender.suggest_move(self.grid, "simple")

        self.assertIn(move, ['left', 'right', 'up', 'down'])
        self.assertIsInstance(rationale, str)
        self.assertGreater(len(rationale), 0)

if __name__ == '__main__':
    unittest.main()
