import unittest

from reco.src.heuristic import HeuristicRecommender


class TestHeuristicRecommender(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

    def test_heuristic_recommender(self):
        recommender = HeuristicRecommender()
        move, rationale = recommender.suggest_move(self.grid)
        
        self.assertIn(move, ['left', 'right', 'up', 'down'])
        self.assertIsInstance(rationale, str)
        self.assertTrue(len(rationale) > 0)

if __name__ == '__main__':
    unittest.main()
