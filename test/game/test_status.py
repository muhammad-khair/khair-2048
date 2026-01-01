import unittest

from src.game.status import GameStatus


class GameStatusTest(unittest.TestCase):
    def test_is_terminal_property(self):
        self.assertTrue(GameStatus.WIN.is_terminal)
        self.assertTrue(GameStatus.LOSE.is_terminal)
        self.assertFalse(GameStatus.ONGOING.is_terminal)


if __name__ == '__main__':
    unittest.main()
