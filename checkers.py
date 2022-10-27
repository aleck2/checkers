from typing import *
'''
|██X ██X ██X ██X |
|X ██X ██X ██X ██|
|██X ██X ██X ██X |
|  ██  ██  ██  ██|
|██  ██  ██  ██  |
|O ██O ██O ██O ██|
|██O ██O ██O ██O |
|O ██O ██O ██O ██|

'''
ROWS = 8
COLS = 8

from enum import Enum

class Team(Enum):
    EMPTY = '-'
    X = 'X'
    O = 'O'

class Direction(Enum):
    UP = -1
    DOWN = 1
    RIGHT = 1
    LEFT = -1

class Move(Enum):
    UP_LEFT = (Direction.UP, Direction.LEFT)
    UP_RIGHT =(Direction.UP, Direction.RIGHT)
    DOWN_LEFT =(Direction.DOWN, Direction.LEFT)
    DOWN_RIGHT = (Direction.DOWN, Direction.RIGHT)


class Coordinate():
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def add(self, move: Move):
        return Coordinate(self.r + move.value[0].value, self.c + move.value[1].value)

    def __str__(self) -> str:
        return 'r: {}, c: {}'.format(self.r, self.c)

    def __eq__(self, obj):
        """need this when checking if coordinate in list of candidate coordinates """
        return self.r == obj.r and self.c == obj.c

    def check_valid(self) -> bool:
        """checks if coordinates is in bounds of board"""
        return self.r >= 0 and self.r < ROWS and self.c >= 0 and self.c < COLS
        

class Piece:
    def __init__(self, team: Team, direction: Direction):
        self.team = team
        self.direction = direction
    
    def __str__(self) -> str:
        return self.team.value
    
class Board:
    """
    Origin is top left corner at r=0, c=0
    """
    def __init__(self):
        # board filled with no pieces
        self.board = [[None for i in range(COLS)] for r in range(ROWS)]

        # board filed with X's going down
        for r in range(3):
            start = 1 if r % 2 == 0 else 0
            for c in range(start, COLS, 2):
                self.place(Piece(Team.X, Direction.DOWN), Coordinate(r, c))

        # board filed with O's going up
        for r in range(COLS-1, COLS-4, -1):
            start = 1 if r % 2 == 0 else 0
            for c in range(start, COLS, 2):
                self.place(Piece(Team.O, Direction.UP), Coordinate(r, c))

        
    def __str__(self) -> str:
        result = ''
        for r in range(ROWS):
            for c in range(COLS):

                if self.board[r][c]:
                    result += str(self.board[r][c])
                else:
                    result += Team.EMPTY.value

            result += '\n'

        return result

    def at(self, coord: Coordinate) -> Optional[Piece]:
        return self.board[coord.r][coord.c]
    
    def place(self, piece: Optional[Piece], coord: Coordinate) -> bool:
        """ place a Piece/None on coordinate"""
        if not self.board[coord.r][coord.c]:
            # if empty (None)
            self.board[coord.r][coord.c] = piece
            return True
        
        return False

    def move(self, old_coord: Coordinate, new_coord: Coordinate) -> bool:
        """
        move piece from a to b
        """
        
        piece = self.at(old_coord)
        candidates = self.list_moves(old_coord)

        if new_coord in candidates:
            # place piece on new empty spot
            self.place(piece, new_coord)

            # remove piece from last spot
            self.place(None, old_coord)

            return True

        return False

    def list_moves(self, coord: Coordinate) -> list[Coordinate]:
        """
        Return list of possible coordinates
        New coordinate space must be
            - in bounds
            - empty
        """
        moves = []
        piece = self.at(coord)
        if not piece:
            return moves

        if piece.direction == Direction.UP:

            up_left = coord.add(Move.UP_LEFT)
            if up_left.check_valid() and not self.at(up_left):
                moves.append(up_left)

            up_right = coord.add(Move.UP_RIGHT)
            if up_right.check_valid() and not self.at(up_right):
                moves.append(up_right)

        elif piece.direction == Direction.DOWN:

            down_left = coord.add(Move.DOWN_LEFT)
            if down_left.check_valid() and not self.at(down_left):
                moves.append(down_left)

            down_right = coord.add(Move.DOWN_RIGHT)
            if down_right.check_valid() and not self.at(down_left):
                moves.append(down_right)

        else:
            # log an error
            print('* ERROR: piece at {}, {} has no direction'.format(coord.r, coord.c))

        return moves


board = Board()
piece = Piece(Team.X, Direction.DOWN)
board.place(piece, Coordinate(0, 1))
print(board)
moves = board.list_moves(Coordinate(0, 1))
print(moves)
