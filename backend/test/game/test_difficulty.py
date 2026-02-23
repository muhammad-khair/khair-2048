import unittest

from src.game.difficulty import Difficulty


class DifficultyTest(unittest.TestCase):
    def test_get_boulder_count(self):
        self.assertEqual(Difficulty.EASY.get_boulder_count(), 0)
        self.assertEqual(Difficulty.MEDIUM.get_boulder_count(), 1)
        self.assertEqual(Difficulty.HARD.get_boulder_count(), 2)


if __name__ == '__main__':
    unittest.main()
