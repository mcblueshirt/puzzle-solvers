# test_game_board.py

from pathlib import Path
from typing import Any
import pytest
from src.game_board import GameBoard


# Fixture for a standard game board
@pytest.fixture
def standard_board() -> GameBoard:
    return GameBoard([["x", "o", "x"], ["o", "x", "o"], ["x", "o", "x"]])


# Test for initializing the GameBoard
def test_init(standard_board: GameBoard) -> None:
    assert standard_board.n_rows == 3
    assert standard_board.n_cols == 3
    assert standard_board.board == [["x", "o", "x"], ["o", "x", "o"], ["x", "o", "x"]]


@pytest.mark.parametrize(
    "row, col, expected", [(0, 0, "x"), (1, 1, "x"), (2, 2, "x"), (0, 1, "o")]
)
def test_get_cell(standard_board: GameBoard, row: int, col: int, expected: str) -> None:
    assert standard_board.get_cell(row, col) == expected


def test_update_cell(standard_board: GameBoard) -> None:
    assert standard_board.get_cell(1, 1) != "o"
    standard_board.update_cell(1, 1, "o")
    assert standard_board.get_cell(1, 1) == "o"


# Test for copying the board
def test_copy(standard_board: GameBoard) -> None:
    new_board = standard_board.copy()
    assert new_board.board == standard_board.board
    assert new_board is not standard_board


# Test for creating a GameBoard from a CSV file
def test_from_csv(tmp_path: Path) -> None:
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "board.csv"
    p.write_text("x,o,x\no,x,o\nx,o,x")
    board = GameBoard.from_csv(str(p))
    assert board.board == [["x", "o", "x"], ["o", "x", "o"], ["x", "o", "x"]]


# Test for handling invalid CSV path
def test_invalid_csv_path() -> None:
    with pytest.raises(FileNotFoundError):
        GameBoard.from_csv("nonexistent.csv")


# # Test for out-of-bounds get_loc
# @pytest.mark.parametrize("row, col", [(-1, 0), (3, 0), (0, -1), (0, 3)])
# def test_get_loc_out_of_bounds(standard_board, row, col) -> None:
#     with pytest.raises(IndexError):
#         standard_board.get_loc(row, col)


# # Integration test with Move class
# def test_integration_with_move(standard_board):
#     move = Move(loc=(1, 1), player="x")
#     standard_board.update_loc(move.loc.row_idx, move.loc.col_idx, move.player)
#     assert standard_board.get_loc(1, 1) == "x"


# Test different board sizes
@pytest.mark.parametrize("size", [3, 5, 10])
def test_board_sizes(size: int) -> None:
    board = [["-" for _ in range(size)] for _ in range(size)]
    game_board = GameBoard(board)
    assert game_board.n_rows == size
    assert game_board.n_cols == size


# Test display_board method
def test_display_board(standard_board: GameBoard, capsys: Any) -> None:
    standard_board.display_board()
    captured = capsys.readouterr()
    assert "x" in captured.out
