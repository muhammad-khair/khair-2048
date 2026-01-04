import unittest
from unittest.mock import MagicMock

from src.game.direction import Direction


class TestDirection(unittest.TestCase):
    def test_enum_values(self):
        """Test that enum values match expected strings."""
        self.assertEqual(Direction.UP.value, "up")
        self.assertEqual(Direction.DOWN.value, "down")
        self.assertEqual(Direction.LEFT.value, "left")
        self.assertEqual(Direction.RIGHT.value, "right")

    def test_apply_to_board_up(self):
        """Test delegation to move_up."""
        mock_board = MagicMock()
        Direction.UP.apply_to_board(mock_board)
        mock_board.move_up.assert_called_once()

    def test_apply_to_board_down(self):
        """Test delegation to move_down."""
        mock_board = MagicMock()
        Direction.DOWN.apply_to_board(mock_board)
        mock_board.move_down.assert_called_once()

    def test_apply_to_board_left(self):
        """Test delegation to move_left."""
        mock_board = MagicMock()
        Direction.LEFT.apply_to_board(mock_board)
        mock_board.move_left.assert_called_once()

    def test_apply_to_board_right(self):
        """Test delegation to move_right."""
        mock_board = MagicMock()
        Direction.RIGHT.apply_to_board(mock_board)
        mock_board.move_right.assert_called_once()


if __name__ == '__main__':
    unittest.main()
