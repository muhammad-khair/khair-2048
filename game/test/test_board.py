import unittest
from unittest import mock
from unittest.mock import MagicMock

from game.src.board import GameBoard, GameBoardException
from game.src.status import GameStatus


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
                turns=1,
            )
        except Exception as ex:
            self.fail(f"Should be able to construct GameBoard, see {ex}")

    def test_initialiser_raises_ValueError_when_board_is_empty(self):
        with self.assertRaises(ValueError) as context:
            GameBoard(
                board=[],
                goal=2048,
                prop_numbers=[2, 4],
                turns=1,
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
            turns=3,
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
            turns=3,
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
            turns=3,
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
            turns=3,
        )
        self.assertNotEqual(board_one, board_two)

    @mock.patch('game.src.board.random.randint')
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
            turns=0,
        )
        self.assertEqual(generated_board, expected_board)

    def test_move_left(self):
        board = GameBoard(
            board=[
                [None, 8, 2, 2],
                [4, 2, None, 2],
                [None, None, None, None],
                [None, None, None, 2],
            ],
            goal=2048,
            prop_numbers=[],
            turns=0,
        )
        board.move_left()

        expected_board = GameBoard(
            board=[
                [8, 4, None, None],
                [4, 4, None, None],
                [None, None, None, None],
                [2, None, None, None],
            ],
            goal=2048,
            prop_numbers=[],
            turns=1,
        )
        self.assertEqual(board, expected_board)

    def test_move_right(self):
        board = GameBoard(
            board=[
                [None, 8, 2, 2],
                [4, 2, None, 2],
                [None, None, None, None],
                [None, None, None, 2],
            ],
            goal=2048,
            prop_numbers=[],
            turns=0,
        )
        board.move_right()

        expected_board = GameBoard(
            board=[
                [None, None, 8, 4],
                [None, None, 4, 4],
                [None, None, None, None],
                [None, None, None, 2],
            ],
            goal=2048,
            prop_numbers=[],
            turns=1,
        )
        self.assertEqual(board, expected_board)

    def test_move_up(self):
        board = GameBoard(
            board=[
                [None, 8, 2, 2],
                [4, 2, None, 2],
                [None, None, None, None],
                [None, None, None, 2],
            ],
            goal=2048,
            prop_numbers=[],
            turns=0,
        )
        board.move_up()

        expected_board = GameBoard(
            board=[
                [4, 8, 2, 4],
                [None, 2, None, 2],
                [None, None, None, None],
                [None, None, None, None],
            ],
            goal=2048,
            prop_numbers=[],
            turns=1,
        )
        self.assertEqual(board, expected_board)

    def test_move_down(self):
        board = GameBoard(
            board=[
                [None, 8, 2, 2],
                [4, 2, None, 2],
                [None, None, None, None],
                [None, None, None, 2]
            ],
            goal=2048,
            prop_numbers=[],
            turns=0,
        )
        board.move_down()

        expected_board = GameBoard(
            board=[
                [None, None, None, None],
                [None, None, None, None],
                [None, 8, None, 2],
                [4, 2, 2, 4]
            ],
            goal=2048,
            prop_numbers=[],
            turns=1,
        )
        self.assertEqual(board, expected_board)

    @mock.patch('game.src.board.random.choice')
    def test_move_up_and_add_random_number_onto_board(self, mock_choice: MagicMock):
        board = GameBoard(
            board=[
                [None, 8, 2, 2],
                [4, 2, None, 2],
                [None, None, None, None],
                [None, None, None, 2],
            ],
            goal=2048,
            prop_numbers=[2, 4],
            turns=0,
        )

        mock_choice.side_effect = [
            2,  # number chosen
            (3, 0),  # position chosen
        ]
        board.move_up()

        expected_board = GameBoard(
            board=[
                [4, 8, 2, 4],
                [None, 2, None, 2],
                [None, None, None, None],
                [2, None, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
            turns=1,
        )
        self.assertEqual(board, expected_board)

    def test_status_win(self):
        board = GameBoard(
            board=[
                [4, None, None, 2],
                [2048, None, None, None],
                [4, 2, None, None],
                [4, None, None, None],
            ],
            goal=2048,
            prop_numbers=[2, 4],
            turns=1,
        )
        self.assertEqual(board.status(), GameStatus.WIN)

    def test_status_lose(self):
        board = GameBoard(
            board=[
                [2, 4, 2, 4],
                [4, 2, 4, 2],
                [2, 4, 2, 4],
                [4, 2, 4, 2],
            ],
            goal=2048,
            prop_numbers=[2, 4],
            turns=1,
        )
        self.assertEqual(board.status(), GameStatus.LOSE)

    def test_status_ongoing(self):
        board = GameBoard(
            board=[
                [None, 8, 2, 2],
                [4, 2, None, 2],
                [None, None, None, None],
                [None, None, None, 2],
            ],
            goal=2048,
            prop_numbers=[2, 4],
            turns=0,
        )
        self.assertEqual(board.status(), GameStatus.ONGOING)

    def test_movement_raise_GameBoardException_upon_terminal_status(self):
        board = GameBoard(
            board=[
                [2, 4, 2, 4],
                [4, 2, 4, 2],
                [2, 4, 2, 4],
                [4, 2, 4, 2],
            ],
            goal=2048,
            prop_numbers=[2, 4],
            turns=1,
        )

        self.assertTrue(board.status().is_terminal)
        with self.assertRaises(GameBoardException) as context:
            board.move_up()
        self.assertEqual(str(context.exception), f"Unable to move, status is {board.status()}")

    def test_get_board_deepcopies_nested_list(self):
        init_board = [
            [None, 8, 2, 2],
            [4, 2, None, 2],
            [None, None, None, None],
            [None, None, None, 2],
        ]
        game_board = GameBoard(
            board=init_board,
            goal=2048,
            prop_numbers=[],
            turns=0,
        )

        board = game_board.get_board()
        self.assertEqual(board, init_board)
        self.assertIsNot(board, init_board)
        for init_row, row in zip(init_board, board):
            self.assertIsNot(init_row, row)

        board[3][2] = 128  # modify value in instance
        other_game_board = GameBoard(
            board=board,
            goal=2048,
            prop_numbers=[],
            turns=0,
        )
        self.assertNotEqual(game_board, other_game_board)

    def test_move_left_no_change_does_not_increment_turns_or_add_tile(self):
        initial_board_grid = [
            [2, None, None, None],
            [4, None, None, None],
            [2, 4, None, None],
            [None, None, None, None],
        ]
        board = GameBoard(
            board=initial_board_grid,
            goal=2048,
            prop_numbers=[2, 4],
            turns=5,
        )
        
        # This move should change nothing as everything is already left
        board.move_left()
        
        self.assertEqual(board.get_board(), initial_board_grid)
        self.assertEqual(board.turns, 5)

    def test_move_right_no_change_does_not_increment_turns_or_add_tile(self):
        initial_board_grid = [
            [None, None, None, 2],
            [None, None, None, 4],
            [None, None, 2, 4],
            [None, None, None, None],
        ]
        board = GameBoard(
            board=initial_board_grid,
            goal=2048,
            prop_numbers=[2, 4],
            turns=5,
        )
        
        board.move_right()
        
        self.assertEqual(board.get_board(), initial_board_grid)
        self.assertEqual(board.turns, 5)

    def test_move_up_no_change_does_not_increment_turns_or_add_tile(self):
        initial_board_grid = [
            [2, 4, 2, None],
            [None, None, 4, None],
            [None, None, None, None],
            [None, None, None, None],
        ]
        board = GameBoard(
            board=initial_board_grid,
            goal=2048,
            prop_numbers=[2, 4],
            turns=5,
        )
        
        board.move_up()
        
        self.assertEqual(board.get_board(), initial_board_grid)
        self.assertEqual(board.turns, 5)

    def test_move_down_no_change_does_not_increment_turns_or_add_tile(self):
        initial_board_grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, 4, None],
            [2, 4, 2, None],
        ]
        board = GameBoard(
            board=initial_board_grid,
            goal=2048,
            prop_numbers=[2, 4],
            turns=5,
        )
        
        board.move_down()
        
        self.assertEqual(board.get_board(), initial_board_grid)
        self.assertEqual(board.turns, 5)


if __name__ == "__main__":
    unittest.main()
