# test_game_service.py

import pytest
from src.game_board import GameBoard
from src.models import BoardLocation, Move
from src.game_service import GameService, InvalidMoveException


@pytest.fixture
def empty_board() -> GameBoard:
    return GameBoard([[" " for _ in range(3)] for _ in range(3)])


@pytest.fixture
def game_service() -> GameService:
    return GameService()


def test_make_valid_move(game_service: GameService, empty_board: GameBoard) -> None:
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="x")
    new_board = game_service.make_move(empty_board, move)
    assert new_board.get_cell(0, 0) == "x"


def test_make_invalid_move_out_of_bounds(
    game_service: GameService, empty_board: GameBoard
) -> None:
    move = Move(cell=BoardLocation(row_idx=-1, col_idx=0), char="x")
    with pytest.raises(InvalidMoveException):
        game_service.make_move(empty_board, move)


def test_empty_spot_is_valid_move(
    game_service: GameService, empty_board: GameBoard
) -> None:
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="x")
    assert game_service.is_valid_move(empty_board, move)


def test_non_empty_spot_is_invalid_move(
    game_service: GameService, empty_board: GameBoard
) -> None:
    empty_board.update_cell(0, 0, "x")
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert not game_service.is_valid_move(empty_board, move)


def test_move_within_boundaries_is_valid(
    game_service: GameService, empty_board: GameBoard
) -> None:
    move = Move(cell=BoardLocation(row_idx=2, col_idx=2), char="x")
    assert game_service.is_valid_move(empty_board, move)


def test_move_outside_of_boundaries_is_invalid(
    game_service: GameService, empty_board: GameBoard
) -> None:
    move = Move(cell=BoardLocation(row_idx=10, col_idx=10), char="x")
    assert not game_service.is_valid_move(empty_board, move)


def test_horizontal_valid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", "x", "o", "o"],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert game_service.is_valid_move(board, move)


def test_horizontal_invalid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", "o", "o", "o"],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert not game_service.is_valid_move(board, move)


def test_vertical_valid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", " ", " ", " "],
            ["x", " ", " ", " "],
            ["o", " ", " ", " "],
            ["o", " ", " ", " "],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert game_service.is_valid_move(board, move)


def test_vertical_invalid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", " ", " ", " "],
            ["o", " ", " ", " "],
            ["o", " ", " ", " "],
            ["o", " ", " ", " "],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert not game_service.is_valid_move(board, move)


def test_forward_diagonal_valid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", " ", " ", " "],
            [" ", " ", "x", " "],
            [" ", "o", " ", " "],
            ["o", " ", " ", " "],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=3), char="o")
    assert game_service.is_valid_move(board, move)


def test_forward_diagonal_invalid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", " ", " ", " "],
            [" ", " ", "o", " "],
            [" ", "o", " ", " "],
            ["o", " ", " ", " "],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=3), char="o")
    assert not game_service.is_valid_move(board, move)


def test_backward_diagonal_valid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", " ", " ", " "],
            [" ", "x", " ", " "],
            [" ", " ", "o", " "],
            [" ", " ", " ", "o"],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert game_service.is_valid_move(board, move)


def test_backward_diagonal_invalid_move(game_service: GameService) -> None:
    board = GameBoard(
        [
            [" ", " ", " ", " "],
            [" ", "o", " ", " "],
            [" ", " ", "o", " "],
            [" ", " ", " ", "o"],
        ]
    )
    move = Move(cell=BoardLocation(row_idx=0, col_idx=0), char="o")
    assert not game_service.is_valid_move(board, move)
