from django.db import models

from chessbackend.models.game import Game
from chessbackend.models.enums import ColorEnum, PieceTypeEnum


class Piece(models.Model):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, related_name="pieces")
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
            if self.current_row + i < 8:
                # row_tiles["east"].append((self.current_row + i, self.current_column))
                row_tiles["east"].append((self.current_column, self.current_row + i))

            if self.current_row - i >= 0:
                row_tiles["west"].append((self.current_column, self.current_row - i))

            if self.current_column + i < 8:
                column_tiles["north"].append(
                    (self.current_column + i, self.current_row)
                )

            if self.current_column - i >= 0:
                column_tiles["south"].append(
                    (self.current_column - i, self.current_row)
                )

            if self.current_row + i < 8 and self.current_column + i < 8:
                diagonal_tiles["ne"].append(
                    (self.current_column + i, self.current_row + i)
                )

            if self.current_row - i >= 0 and self.current_column + i < 8:
                diagonal_tiles["se"].append(
                    (self.current_column + i, self.current_row - i)
                )

            if self.current_row - i >= 0 and self.current_column - i >= 0:
                diagonal_tiles["sw"].append(
                    (self.current_column - i, self.current_row - i)
                )

            if self.current_row + i < 8 and self.current_column - i >= 0:
                diagonal_tiles["nw"].append(
                    (self.current_column - i, self.current_row + i)
                )

        return {
            "row_tiles": row_tiles,
            "column_tiles": column_tiles,
            "diagonal_tiles": diagonal_tiles,
        }

    def get_knight_move_tiles(self) -> list:
        knight_tiles = []

        if self.current_column - 1 >= 0 and self.current_row + 2 < 8:
            pos = (self.current_column - 1, self.current_row + 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column - 2 >= 0 and self.current_row + 1 < 8:
            pos = (self.current_column - 2, self.current_row + 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column - 2 >= 0 and self.current_row - 1 >= 0:
            pos = (self.current_column - 2, self.current_row - 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column - 1 >= 0 and self.current_row - 2 >= 0:
            pos = (self.current_column - 1, self.current_row - 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column + 1 < 8 and self.current_row + 2 < 8:
            pos = (self.current_column + 1, self.current_row + 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column + 2 < 8 and self.current_row + 1 < 8:
            pos = (self.current_column + 2, self.current_row + 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column + 2 < 8 and self.current_row - 1 >= 0:
            pos = (self.current_column + 2, self.current_row - 1)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
                knight_tiles.append(pos)

        if self.current_column + 1 < 8 and self.current_row - 2 >= 0:
            pos = (self.current_column + 1, self.current_row - 2)
            if (
                self.game.current_board[pos]["piece"]
                and self.game.current_board[pos]["piece"].color != self.color
            ):
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
                    if other_piece.color == self.opposite_color:
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
                    if other_piece.color == self.opposite_color:
                        rook_tiles.append(tile)
                    break

        for direction in ["north", "south"]:
            for tile in column_tiles[direction]:
                if not self.game.current_board[tile]["piece"]:
                    rook_tiles.append(tile)
                else:
                    other_piece = self.game.current_board[tile]["piece"]
                    if other_piece.color == self.opposite_color:
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
        king_moves = []
        if self.current_column + 1 < 8:
            if self.game.current_board[(self.current_column + 1, self.current_row)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column + 1, self.current_row)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column + 1, self.current_row))
            else:
                king_moves.append((self.current_column + 1, self.current_row))

        if self.current_column + 1 < 8 and self.current_row + 1 < 8:
            if self.game.current_board[(self.current_column + 1, self.current_row + 1)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column + 1, self.current_row + 1)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column + 1, self.current_row + 1))
            else:
                king_moves.append((self.current_column + 1, self.current_row + 1))

        if self.current_row + 1 < 8:
            if self.game.current_board[(self.current_column, self.current_row + 1)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column, self.current_row + 1)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column, self.current_row + 1))
            else:
                king_moves.append((self.current_column, self.current_row + 1))

        if self.current_column - 1 >= 0 and self.current_row + 1 < 8:
            if self.game.current_board[(self.current_column - 1, self.current_row + 1)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column - 1, self.current_row + 1)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column - 1, self.current_row + 1))
            else:
                king_moves.append((self.current_column - 1, self.current_row + 1))

        if self.current_column - 1 >= 0:
            if self.game.current_board[(self.current_column - 1, self.current_row)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column - 1, self.current_row)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column - 1, self.current_row))
            else:
                king_moves.append((self.current_column - 1, self.current_row))

        if self.current_column - 1 >= 0 and self.current_row - 1 >= 0:
            if self.game.current_board[(self.current_column - 1, self.current_row - 1)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column - 1, self.current_row - 1)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column - 1, self.current_row - 1))
            else:
                king_moves.append((self.current_column - 1, self.current_row - 1))

        if self.current_row - 1 >= 0:
            if self.game.current_board[(self.current_column, self.current_row - 1)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column, self.current_row - 1)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column, self.current_row - 1))
            else:
                king_moves.append((self.current_column, self.current_row - 1))

        if self.current_column + 1 < 8 and self.current_row - 1 >= 0:
            if self.game.current_board[(self.current_column + 1, self.current_row - 1)][
                "piece"
            ]:
                if (
                    self.game.current_board[
                        (self.current_column + 1, self.current_row - 1)
                    ]["piece"].color
                    == self.opposite_color
                ):
                    king_moves.append((self.current_column + 1, self.current_row - 1))
            else:
                king_moves.append((self.current_column + 1, self.current_row - 1))

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
                (self.current_column + 1, self.current_row + (1 * row_multiplier))
            ]["piece"]:
                if (
                    self.game.current_board[
                        (
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    ]["piece"].color
                    == self.opposite_color
                ):
                    pawn_moves.append(
                        (
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    )

        if (
            self.current_column - 1 >= 0
            and 0 <= self.current_row + (1 * row_multiplier) < 7
        ):
            if self.game.current_board[
                (self.current_column - 1, self.current_row + (1 * row_multiplier))
            ]["piece"]:
                if (
                    self.game.current_board[
                        (
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    ]["piece"].color
                    == self.opposite_color
                ):
                    pawn_moves.append(
                        (
                            self.current_column + 1,
                            self.current_row + (1 * row_multiplier),
                        )
                    )

        if 0 <= self.current_row + (1 * row_multiplier) < 7:
            if not self.game.current_board[
                (self.current_column, self.current_row + (1 * row_multiplier))
            ]["piece"]:
                pawn_moves.append(
                    (self.current_column, self.current_row + (1 * row_multiplier))
                )

        if self.color == ColorEnum.WHITE.value:
            if self.current_row == 1:
                if not self.game.current_board[
                    (self.current_column, self.current_row + (2 * row_multiplier))
                ]["piece"]:
                    pawn_moves.append(
                        (self.current_column, self.current_row + (2 * row_multiplier))
                    )

        if self.color == ColorEnum.BLACK.value:
            if self.current_row == 6:
                if not self.game.current_board[
                    (self.current_column, self.current_row + (2 * row_multiplier))
                ]["piece"]:
                    pawn_moves.append(
                        (self.current_column, self.current_row + (2 * row_multiplier))
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

    def is_pinned_to_king(self, surrounding_tiles) -> int:
        pin_count = 0
        if not self.in_alignment_with_own_king():
            return pin_count

        current_board = self.game.current_board

        # Check row tiles for an opposing rook or queen
        for direction in ["east", "west"]:
            for row_tile in surrounding_tiles["row_tiles"][direction]:
                piece = current_board[row_tile]["piece"]
                if piece:
                    if piece.color == self.opposite_color and self.type in [
                        PieceTypeEnum.ROOK.value,
                        PieceTypeEnum.QUEEN.value,
                    ]:
                        pin_count += 1
                    else:
                        break

        # Check column tiles for an opposing rook or queen
        for direction in ["north", "south"]:
            for coulmn_tile in surrounding_tiles["column_tiles"][direction]:
                piece = current_board[coulmn_tile]["piece"]
                if piece:
                    if piece.color == self.opposite_color and self.type in [
                        PieceTypeEnum.ROOK.value,
                        PieceTypeEnum.QUEEN.value,
                    ]:
                        pin_count += 1
                    else:
                        break

        # Check diagonal tiles for an opposing bishop or queen
        for direction in ["ne", "se", "sw", "nw"]:
            for diagonal_tile in surrounding_tiles["diagonal_tiles"][direction]:
                piece = current_board[diagonal_tile]["piece"]
                if piece:
                    if piece.color == self.opposite_color and self.type in [
                        PieceTypeEnum.BISHOP.value,
                        PieceTypeEnum.QUEEN.value,
                    ]:
                        pin_count += 1
                    else:
                        break

        return pin_count

    def can_en_pessant(self) -> bool:
        if self.type != PieceTypeEnum.PAWN.value:
            return False

        # TODO do not forget about implementing this functionality!!!!!

    def possible_moves(self):
        # TODO determine if a piece can move (ie not pinned)
        # Once if piece can move is determined then start calcing possible moves.
        all_surrounding_tiles = self.get_all_surrounding_tiles()
        possible_moves = []

        # TODO need to fix this logic is is close to working but does not work.
        # A piece can still move if is pinned to the king (just not double pinned) if the piece moves in the pinned direction!
        # I may need to implement in my move tile checks if the move can unpin instead of returning [] immediatly
        if self.is_pinned_to_king(all_surrounding_tiles):
            return possible_moves

        # TODO return possible moves for a piece depending on what type it is and where it is located on the board!
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

        return possible_moves

    def opposite_color(self):
        if self.color == ColorEnum.WHITE.value:
            return ColorEnum.BLACK.value
        elif self.color == ColorEnum.BLACK.value:
            return ColorEnum.WHITE.value
