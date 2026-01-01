import unittest

from unittest import mock
from unittest.mock import MagicMock

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

    def test_equality_returns_true(self):
        board_one = GameBoard(
            board=[
                [2, None, None, None],
                [None, None, 2, None],
                [None, None, None, None],
                [None, 2, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
        )
        board_two = GameBoard(
            board=[
                [2, None, None, None],
                [None, None, 2, None],
                [None, None, None, None],
                [None, 2, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
        )
        self.assertEqual(board_one, board_two)

    def test_equality_returns_false(self):
        board_one = GameBoard(
            board=[
                [2, None, None, None],
                [None, None, 2, None],
                [None, None, None, None],
                [None, 2, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
        )
        board_two = GameBoard(
            board=[
                [None, None, 2, None],
                [None, None, None, None],
                [None, None, 4, None],
                [2, None, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
        )
        self.assertNotEqual(board_one, board_two)

    @mock.patch('src.game.board.random.randint')
    def test_static_constructor(self, mock_randint: MagicMock):
        # coordinates for random number placement
        mock_randint.side_effect = [
            0, 0,
            1, 2,
            1, 2,  # to test if slot is already populated so logic will skip
            3, 1,
        ]
        generated_board = GameBoard.create_new(
            grid_length=4,
            goal_number=2048,
            starting_count=3,
            starting_number=2,
        )
        expected_board = GameBoard(
            board=[
                [2, None, None, None],
                [None, None, 2, None],
                [None, None, None, None],
                [None, 2, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
        )
        self.assertEqual(generated_board, expected_board)


if __name__ == "__main__":
    unittest.main()
