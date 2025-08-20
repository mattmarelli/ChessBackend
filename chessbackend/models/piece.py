from django.db import models

from chessbackend.models.base import BaseModel
from chessbackend.models.game import Game
from chessbackend.models.enums import ColorEnum, PieceTypeEnum


class Piece(BaseModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="pieces")
    color = models.CharField(
        max_length=25, choices=[(color.value, color.name) for color in ColorEnum]
    )
    type = models.CharField(
        max_length=25,
        choices=[(piece_type.value, piece_type.name) for piece_type in PieceTypeEnum],
    )
    starting_row = models.IntegerField()
    starting_column = models.IntegerField()
    current_row = models.IntegerField()
    current_column = models.IntegerField()
    captured = models.BooleanField(default=False)
    captured_by = models.ForeignKey(
        "self",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="captured_pieces",
    )
    defended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.color} {self.type} current column: {self.current_column}, current_row: {self.current_row}"

    def get_all_surrounding_tiles(self) -> dict:
        row_tiles = {
            "east": [],
            "west": [],
        }
        column_tiles = {
            "north": [],
            "south": [],
        }
        diagonal_tiles = {
            "ne": [],
            "se": [],
            "sw": [],
            "nw": [],
        }
        for i in range(1, 8):
            if self.current_column + i < 8:
                row_tiles["east"].append(
                    self.position_string(self.current_column + i, self.current_row)
                )

            if self.current_column - i >= 0:
                row_tiles["west"].append(
                    self.position_string(self.current_column - i, self.current_row)
                )

            if self.current_row + i < 8:
                column_tiles["north"].append(
                    self.position_string(self.current_column, self.current_row + i)
                )

            if self.current_row - i >= 0:
                column_tiles["south"].append(
                    self.position_string(self.current_column, self.current_row - i)
                )

            if self.current_row + i < 8 and self.current_column + i < 8:
                diagonal_tiles["ne"].append(
                    self.position_string(self.current_column + i, self.current_row + i)
                )

            if self.current_row - i >= 0 and self.current_column + i < 8:
                diagonal_tiles["se"].append(
                    self.position_string(self.current_column + i, self.current_row - i)
                )

            if self.current_row - i >= 0 and self.current_column - i >= 0:
                diagonal_tiles["sw"].append(
                    self.position_string(self.current_column - i, self.current_row - i)
                )

            if self.current_row + i < 8 and self.current_column - i >= 0:
                diagonal_tiles["nw"].append(
                    self.position_string(self.current_column - i, self.current_row + i)
                )

        return {
            "row_tiles": row_tiles,
            "column_tiles": column_tiles,
            "diagonal_tiles": diagonal_tiles,
        }

    def get_knight_move_tiles(self) -> list:
        knight_tiles = []

        if self.current_column - 1 >= 0 and self.current_row + 2 < 8:
            pos = self.position_string(self.current_column - 1, self.current_row + 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column - 2 >= 0 and self.current_row + 1 < 8:
            pos = self.position_string(self.current_column - 2, self.current_row + 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column - 2 >= 0 and self.current_row - 1 >= 0:
            pos = self.position_string(self.current_column - 2, self.current_row - 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column - 1 >= 0 and self.current_row - 2 >= 0:
            pos = self.position_string(self.current_column - 1, self.current_row - 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column + 1 < 8 and self.current_row + 2 < 8:
            pos = self.position_string(self.current_column + 1, self.current_row + 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column + 2 < 8 and self.current_row + 1 < 8:
            pos = self.position_string(self.current_column + 2, self.current_row + 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column + 2 < 8 and self.current_row - 1 >= 0:
            pos = self.position_string(self.current_column + 2, self.current_row - 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        if self.current_column + 1 < 8 and self.current_row - 2 >= 0:
            pos = self.position_string(self.current_column + 1, self.current_row - 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"]["piece_color"] != self.color
            ):
                knight_tiles.append(pos)
            elif (self.game.current_board[pos]["piece"]) is None:
                knight_tiles.append(pos)

        return knight_tiles

    def get_bishop_move_tiles(self, diagonal_tiles) -> list:
        bishop_tiles = []

        for direction in ["ne", "se", "sw", "nw"]:
            for tile in diagonal_tiles[direction]:
                if not self.game.current_board[tile]["piece"]:
                    bishop_tiles.append(tile)
                else:
                    other_piece = self.game.current_board[tile]["piece"]
                    if other_piece["piece_color"] == self.opposite_color():
                        bishop_tiles.append(tile)
                    break

        return bishop_tiles

    def get_rook_move_tiles(self, row_tiles, column_tiles) -> list:
        rook_tiles = []

        for direction in ["east", "west"]:
            for tile in row_tiles[direction]:
                if not self.game.current_board[tile]["piece"]:
                    rook_tiles.append(tile)
                else:
                    other_piece = self.game.current_board[tile]["piece"]
                    if other_piece["piece_color"] == self.opposite_color():
                        rook_tiles.append(tile)
                    break

        for direction in ["north", "south"]:
            for tile in column_tiles[direction]:
                if not self.game.current_board[tile]["piece"]:
                    rook_tiles.append(tile)
                else:
                    other_piece = self.game.current_board[tile]["piece"]
                    if other_piece["piece_color"] == self.opposite_color():
                        rook_tiles.append(tile)
                    break

        # TODO need to include castling at some point!!!!!

        return rook_tiles

    def get_queen_move_tiles(self, diagonal_tiles, row_tiles, column_tiles) -> list:
        queen_tiles = []
        queen_tiles += self.get_rook_move_tiles(row_tiles, column_tiles)
        queen_tiles += self.get_bishop_move_tiles(diagonal_tiles)
        return queen_tiles

    def get_king_move_tiles(self) -> list:
        # TODO need to add a check in here if the piece is defended or not!
        # If the piece is defended then a king cannot move there!
        king_moves = []
        if self.current_column + 1 < 8:
            if self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(self.current_column + 1, self.current_row)
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column + 1, self.current_row)
                )

        if self.current_column + 1 < 8 and self.current_row + 1 < 8:
            if self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row + 1)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row + 1)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(
                            self.current_column + 1, self.current_row + 1
                        )
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column + 1, self.current_row + 1)
                )

        if self.current_row + 1 < 8:
            if self.game.current_board[
                self.position_string(self.current_column, self.current_row + 1)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column, self.current_row + 1)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(self.current_column, self.current_row + 1)
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column, self.current_row + 1)
                )

        if self.current_column - 1 >= 0 and self.current_row + 1 < 8:
            if self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row + 1)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row + 1)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(
                            self.current_column - 1, self.current_row + 1
                        )
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column - 1, self.current_row + 1)
                )

        if self.current_column - 1 >= 0:
            if self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(self.current_column - 1, self.current_row)
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column - 1, self.current_row)
                )

        if self.current_column - 1 >= 0 and self.current_row - 1 >= 0:
            if self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row - 1)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row - 1)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(
                            self.current_column - 1, self.current_row - 1
                        )
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column - 1, self.current_row - 1)
                )

        if self.current_row - 1 >= 0:
            if self.game.current_board[
                self.position_string(self.current_column, self.current_row - 1)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column, self.current_row - 1)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(self.current_column, self.current_row - 1)
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column, self.current_row - 1)
                )

        if self.current_column + 1 < 8 and self.current_row - 1 >= 0:
            if self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row - 1)
            ]["piece"]:
                piece = self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row - 1)
                ]["piece"]
                if (
                    piece["piece_color"] == self.opposite_color()
                    and not piece["defended"]
                ):
                    king_moves.append(
                        self.position_string(
                            self.current_column + 1, self.current_row - 1
                        )
                    )
            else:
                king_moves.append(
                    self.position_string(self.current_column + 1, self.current_row - 1)
                )

        # TODO Need to include castling and filtering moves from check at some point!!!!

        return king_moves

    def get_pawn_move_tiles(self) -> list:
        # TODO need to catch error of going out of bound here and also how to promote pawns!!!!
        row_multiplier = 1 if self.color == ColorEnum.WHITE.value else -1
        pawn_moves = []
        if (
            self.current_column + 1 < 8
            and 0 <= self.current_row + (1 * row_multiplier) < 7
        ):
            if self.game.current_board[
                self.position_string(
                    self.current_column + 1, self.current_row + (1 * row_multiplier)
                )
            ]["piece"]:
                if (
                    self.game.current_board[
                        self.position_string(
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    ]["piece"]["piece_color"]
                    == self.opposite_color()
                ):
                    pawn_moves.append(
                        self.position_string(
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    )

        if (
            self.current_column - 1 >= 0
            and 0 <= self.current_row + (1 * row_multiplier) < 7
        ):
            if self.game.current_board[
                self.position_string(
                    self.current_column - 1, self.current_row + (1 * row_multiplier)
                )
            ]["piece"]:
                if (
                    self.game.current_board[
                        self.position_string(
                            self.current_column - 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    ]["piece"]["piece_color"]
                    == self.opposite_color()
                ):
                    pawn_moves.append(
                        self.position_string(
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    )

        if 0 <= self.current_row + (1 * row_multiplier) < 7:
            if not self.game.current_board[
                self.position_string(
                    self.current_column, self.current_row + (1 * row_multiplier)
                )
            ]["piece"]:
                pawn_moves.append(
                    self.position_string(
                        self.current_column, self.current_row + (1 * row_multiplier)
                    )
                )

        if self.color == ColorEnum.WHITE.value:
            if self.current_row == 1:
                if not self.game.current_board[
                    self.position_string(
                        self.current_column, self.current_row + (2 * row_multiplier)
                    )
                ]["piece"]:
                    pawn_moves.append(
                        self.position_string(
                            self.current_column, self.current_row + (2 * row_multiplier)
                        )
                    )

        if self.color == ColorEnum.BLACK.value:
            if self.current_row == 6:
                if not self.game.current_board[
                    self.position_string(
                        self.current_column, self.current_row + (2 * row_multiplier)
                    )
                ]["piece"]:
                    pawn_moves.append(
                        self.position_string(
                            self.current_column, self.current_row + (2 * row_multiplier)
                        )
                    )

        return pawn_moves

    def in_alignment_with_own_king(self) -> bool:
        king_piece = self.game.pieces.get(
            color=self.color, type=PieceTypeEnum.KING.value
        )
        row_diff = abs(self.current_row - king_piece.current_row)
        column_diff = abs(self.current_column - king_piece.current_column)
        if not row_diff or not column_diff or row_diff == column_diff:
            return True
        return False

    def is_checking_king(self) -> bool:
        opposite_king = self.game.pieces.get(
            color=self.opposite_color(),
            type=PieceTypeEnum.KING.value,
        )

        possible_moves = self.possible_moves()

        if self.type == PieceTypeEnum.PAWN.value:
            if (
                opposite_king.current_column - 1,
                opposite_king.current_row,
            ) in possible_moves or (
                opposite_king.current_column + 1,
                opposite_king.current_row,
            ) in possible_moves:
                return True
            return False

        if (opposite_king.current_column, opposite_king.current_row) in possible_moves:
            return True

        return False

    def is_pinned_to_king(self, surrounding_tiles) -> int:
        pinning_pieces = []
        if not self.in_alignment_with_own_king():
            return pinning_pieces

        current_board = self.game.current_board

        # Check row tiles for an opposing rook or queen
        for direction in ["east", "west"]:
            for row_tile in surrounding_tiles["row_tiles"][direction]:
                piece = current_board[row_tile]["piece"]
                if piece:
                    if piece["piece_color"] == self.opposite_color and self.type in [
                        PieceTypeEnum.ROOK.value,
                        PieceTypeEnum.QUEEN.value,
                    ]:
                        pinning_pieces.append(piece)
                    else:
                        break

        # Check column tiles for an opposing rook or queen
        for direction in ["north", "south"]:
            for coulmn_tile in surrounding_tiles["column_tiles"][direction]:
                piece = current_board[coulmn_tile]["piece"]
                if piece:
                    if piece["piece_color"] == self.opposite_color and self.type in [
                        PieceTypeEnum.ROOK.value,
                        PieceTypeEnum.QUEEN.value,
                    ]:
                        pinning_pieces.append(piece)
                    else:
                        break

        # Check diagonal tiles for an opposing bishop or queen
        for direction in ["ne", "se", "sw", "nw"]:
            for diagonal_tile in surrounding_tiles["diagonal_tiles"][direction]:
                piece = current_board[diagonal_tile]["piece"]
                if piece:
                    if piece["piece_color"] == self.opposite_color and self.type in [
                        PieceTypeEnum.BISHOP.value,
                        PieceTypeEnum.QUEEN.value,
                    ]:
                        pinning_pieces.append(piece)
                    else:
                        break

        return pinning_pieces

    def is_king_next_to_me(self) -> bool:
        if (
            self.current_column + 1 < 8
            and self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_column + 1 < 8
            and self.current_row - 1 >= 0
            and self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row - 1)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row - 1)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row - 1)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_column + 1 < 8
            and self.current_row + 1 < 8
            and self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row + 1)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row + 1)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column + 1, self.current_row + 1)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_row + 1 < 8
            and self.game.current_board[
                self.position_string(self.current_column, self.current_row + 1)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column, self.current_row + 1)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column, self.current_row + 1)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_row - 1 >= 0
            and self.game.current_board[
                self.position_string(self.current_column, self.current_row - 1)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column, self.current_row - 1)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column, self.current_row - 1)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_column - 1 >= 0
            and self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_column - 1 >= 0
            and self.current_row - 1 >= 0
            and self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row - 1)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row - 1)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row - 1)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        if (
            self.current_column - 1 >= 0
            and self.current_row + 1 < 8
            and self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row + 1)
            ]["piece"]
        ):
            if (
                self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row + 1)
                ]["piece"]["type"]
                == "king"
                and self.game.current_board[
                    self.position_string(self.current_column - 1, self.current_row + 1)
                ]["piece"]["piece_color"]
                == self.color
            ):
                return True

        return False

    def is_pawn_defending_me(self) -> bool:
        scaler_value = -1 if self.color == ColorEnum.WHITE.value else 1

        if (
            0 <= self.current_column - 1 < 8
            and 0 <= self.current_row + scaler_value < 8
            and self.game.current_board[
                self.position_string(
                    self.current_column - 1, self.current_row + scaler_value
                )
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(
                    self.current_column - 1, self.current_row + scaler_value
                )
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.PAWN.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            0 <= self.current_column + 1 < 8
            and 0 <= self.current_row + scaler_value < 8
            and self.game.current_board[
                self.position_string(
                    self.current_column + 1, self.current_row + scaler_value
                )
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(
                    self.current_column + 1, self.current_row + scaler_value
                )
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.PAWN.value
                and piece["piece_color"] == self.color
            ):
                return True

        return False

    def is_knight_defending_me(self) -> bool:
        if (
            self.current_column - 1 >= 0
            and self.current_row + 2 < 8
            and self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row + 2)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row + 2)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column - 2 >= 0
            and self.current_row + 1 < 8
            and self.game.current_board[
                self.position_string(self.current_column - 2, self.current_row + 1)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column - 2, self.current_row + 1)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column - 2 >= 0
            and self.current_row - 1 >= 0
            and self.game.current_board[
                self.position_string(self.current_column - 2, self.current_row - 1)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column - 2, self.current_row - 1)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column - 1 >= 0
            and self.current_row - 2 >= 0
            and self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row - 2)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column - 1, self.current_row - 2)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column + 1 < 8
            and self.current_row - 2 >= 8
            and self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row - 2)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row - 2)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column + 2 < 8
            and self.current_row - 1 >= 0
            and self.game.current_board[
                self.position_string(self.current_column + 2, self.current_row - 1)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column + 2, self.current_row - 1)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column + 2 < 8
            and self.current_row + 1 < 8
            and self.game.current_board[
                self.position_string(self.current_column + 2, self.current_row + 1)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column + 2, self.current_row + 1)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        if (
            self.current_column + 1 < 8
            and self.current_row + 2 < 8
            and self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row + 2)
            ]["piece"]
        ):
            piece = self.game.current_board[
                self.position_string(self.current_column + 1, self.current_row + 2)
            ]["piece"]
            if (
                piece["type"] == PieceTypeEnum.KNIGHT.value
                and piece["piece_color"] == self.color
            ):
                return True

        return False

    def is_defended(self) -> bool:
        all_surrounding_tiles = self.get_all_surrounding_tiles()
        row_tiles = all_surrounding_tiles["row_tiles"]
        column_tiles = all_surrounding_tiles["column_tiles"]
        diagonal_tiles = all_surrounding_tiles["diagonal_tiles"]

        for direction in ["east", "west"]:
            for tile in row_tiles[direction]:
                if self.game.current_board[tile]["piece"]:
                    piece = self.game.current_board[tile]["piece"]
                    if piece["piece_color"] == self.color and piece["type"] in [
                        PieceTypeEnum.QUEEN.value,
                        PieceTypeEnum.ROOK.value,
                    ]:
                        return True
                    break

        for direction in ["north", "south"]:
            for tile in column_tiles[direction]:
                if self.game.current_board[tile]["piece"]:
                    piece = self.game.current_board[tile]["piece"]
                    if piece["piece_color"] == self.color and piece["type"] in [
                        PieceTypeEnum.QUEEN.value,
                        PieceTypeEnum.ROOK.value,
                    ]:
                        return True
                    break

        for direction in ["ne", "se", "sw", "nw"]:
            for tile in diagonal_tiles[direction]:
                if self.game.current_board[tile]["piece"]:
                    piece = self.game.current_board[tile]["piece"]
                    if piece["piece_color"] == self.color and piece["type"] in [
                        PieceTypeEnum.QUEEN.value,
                        PieceTypeEnum.BISHOP.value,
                    ]:
                        return True
                    break

        if self.is_knight_defending_me():
            return True

        if self.is_king_next_to_me():
            return True

        if self.is_pawn_defending_me():
            return True

        return False

    def can_en_pessant(self) -> bool:
        if self.type != PieceTypeEnum.PAWN.value:
            return False
        # TODO do not forget about implementing this functionality!!!!!

    def moves_that_block_or_take_checking_piece(self, checking_piece, moves):
        king = self.game.pieces.get(color=self.color, type=PieceTypeEnum.KING.value)
        check_position = (
            checking_piece["current_column"],
            checking_piece["current_row"],
        )

        if checking_piece["type"] in [
            PieceTypeEnum.PAWN.value,
            PieceTypeEnum.KNIGHT.value,
        ]:
            if check_position in moves:
                moves = check_position
                return moves

        blocking_positions = []
        if (
            king.current_column != checking_piece["current_column"]
            and king.current_row != checking_piece["current_row"]
        ):
            step_x = 1 if checking_piece["current_column"] > king.current_column else -1
            step_y = 1 if checking_piece["current_row"] > king.current_row else -1
            for i in range(
                1, abs(king.current_column - checking_piece["current_column"])
            ):
                blocking_positions.append(
                    (king.current_column + i * step_x, king.current_row + i * step_y)
                )
        elif king.current_column != checking_piece["current_column"]:
            step = 1 if checking_piece["current_column"] > king.current_column else -1
            for x in range(
                king.current_column + step, checking_piece["current_column"], step
            ):
                blocking_positions.append((x, king.current_row))
        elif king.current_row != checking_piece["current_row"]:
            step = 1 if checking_piece["current_row"] > king.current_row else -1
            for y in range(
                king.current_row + step, checking_piece["current_row"], step
            ):
                blocking_positions.append((king.current_column, y))

        moves = [move for move in moves if move in blocking_positions]
        return moves

    def possible_moves(self):
        all_surrounding_tiles = self.get_all_surrounding_tiles()
        possible_moves = []

        if self.type != PieceTypeEnum.KING.value:
            if self.color == ColorEnum.WHITE.value:
                if len(self.game.white_check_pieces) > 1:
                    return possible_moves
            else:
                if len(self.game.black_check_pieces) > 1:
                    return possible_moves

        if self.type == PieceTypeEnum.KNIGHT.value:
            possible_moves = self.get_knight_move_tiles()

        if self.type == PieceTypeEnum.BISHOP.value:
            possible_moves = self.get_bishop_move_tiles(
                all_surrounding_tiles["diagonal_tiles"]
            )

        if self.type == PieceTypeEnum.ROOK.value:
            possible_moves = self.get_rook_move_tiles(
                all_surrounding_tiles["row_tiles"],
                all_surrounding_tiles["column_tiles"],
            )

        if self.type == PieceTypeEnum.QUEEN.value:
            possible_moves = self.get_queen_move_tiles(
                all_surrounding_tiles["diagonal_tiles"],
                all_surrounding_tiles["row_tiles"],
                all_surrounding_tiles["column_tiles"],
            )

        if self.type == PieceTypeEnum.KING.value:
            possible_moves = self.get_king_move_tiles()

        if self.type == PieceTypeEnum.PAWN.value:
            possible_moves = self.get_pawn_move_tiles()

        moves = []
        for possible_move in possible_moves:
            column, row = possible_move.split(",")
            moves.append((int(column), int(row)))

        pinning_pieces = self.is_pinned_to_king(all_surrounding_tiles)
        if pinning_pieces:
            piece_positions = []
            for pinning_piece in pinning_pieces:
                piece_positions.append(
                    (pinning_piece.current_column, pinning_piece.current_row)
                )
            moves = [move for move in moves if move in piece_positions]

        if self.type != PieceTypeEnum.KING.value:
            checking_piece = None
            if self.game.white_in_check and self.color == ColorEnum.WHITE.value:
                checking_piece = list(self.game.white_check_pieces.values())[0]
            if self.game.black_in_check and self.color == ColorEnum.BLACK.value:
                checking_piece = list(self.game.black_check_pieces.values())[0]

            if checking_piece:
                moves = self.moves_that_block_or_take_checking_piece(
                    checking_piece, moves
                )

        return moves

    def opposite_color(self):
        if self.color == ColorEnum.WHITE.value:
            return ColorEnum.BLACK.value
        elif self.color == ColorEnum.BLACK.value:
            return ColorEnum.WHITE.value

    def board_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "piece_color": self.color,
            "defended": self.defended,
            "current_column": self.current_column,
            "current_row": self.current_row,
        }

    def current_position_string(self):
        return f"{self.current_column},{self.current_row}"

    def position_string(self, column, row):
        return f"{column},{row}"
