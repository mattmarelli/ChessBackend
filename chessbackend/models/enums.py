import enum


class ColorEnum(enum.Enum):
    BLACK = "black"
    WHITE = "white"


class PieceTypeEnum(enum.Enum):
    PAWN = "pawn"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class StartingPositionEnum(enum.Enum):
    STANDARD = "standard"
    FISHER_RANDOM = "fisher_random"
