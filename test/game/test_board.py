import unittest

from src.game.board import GameBoard


class GameBoardTest(unittest.TestCase):
    def test_initialiser(self):
        try:
            GameBoard(
                board=[
                    [2, None, None, None],
                    [None, None, 2, None],
                    [None, None, None, None],
                    [None, 2, None, None],
                ],
                goal=2048,
                prop_numbers=[2, 4],
            )
        except Exception as ex:
            self.fail(f"Should be able to construct GameBoard, see {ex}")

    def test_initialiser_raises_ValueError_when_board_is_empty(self):
        with self.assertRaises(ValueError) as context:
            GameBoard(
                board=[],
                goal=2048,
                prop_numbers=[2, 4],
            )
        self.assertEqual(str(context.exception), "Board is empty")


if __name__ == "__main__":
    unittest.main()
