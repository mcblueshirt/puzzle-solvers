from typing import Literal
from pydantic import BaseModel


class BoardShape(BaseModel):
    rows: int
    cols: int


class BoardLocation(BaseModel):
    row_idx: int
    col_idx: int


class Move(BaseModel):
    cell: BoardLocation
    char: Literal["x", "o"]
