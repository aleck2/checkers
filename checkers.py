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

1. For some arbitrary game state of a checkers game, return all possible next moves.
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

    def __str__(self):
        return 'r: {}, c: {}'.format(self.r, self.c)

     # def __contains__():
     # TODO necessary?

    def check_valid(self) -> bool:
        return self.r >= 0 and self.r < ROWS and self.c >= 0 and self.c < COLS
        

class Piece:
    def __init__(self, team: Team, direction: Direction):
        self.team = team
        self.direction = direction
    
    def __str__(self):
        return self.team.value
    
class Board:
    """
    Origin is top left corner at 0,0
    """
    def __init__(self):
        # board filled with pieces
        self.board = [[None for i in range(COLS)] for r in range(ROWS)]
        

    def __str__(self):
        result = ''
        for i in range(ROWS):
            for j in range(COLS):

                if self.board[i][j]:
                    result += str(self.board[i][j])
                else:
                    result += Team.EMPTY.value

            result += '\n'

        return result
    
    def place(self, piece: Piece, coord: Coordinate) -> bool:
        # if empty
        # TDOO check subsetting okay
        if not self.board[coord.r][coord.c]:
            self.board[coord.r][coord.c] = Piece(Team.X, Direction.DOWN)
            return True
        
        return False

    def make_move(self, piece, old_coord: Coordinate, new_coord: Coordinate):
        candidates = self.list_moves(piece)

        if new_coord in candidates:
            # place piece on new spot
            self.board[new_coord.r][new_coord.c] = piece.team

            # remove piece from last spot
            self.board[old_coord.r][old_coord.c] = None

            return True

        return False

    def list_moves(self, coord: Coordinate) -> list[Coordinate]:
        """ Return list of possible coordinates """
        moves = []
        piece = self.board[coord.r][coord.c]
        if not piece:
            return moves

        if piece.direction == Direction.UP:
            if self.check_up_left(piece, coord):
                moves.append(coord.add(Move.UP_LEFT))
            if self.check_up_right(piece, coord):
                moves.append(coord.add(Move.UP_RIGHT))
        else:
            if self.check_down_left(piece, coord):
                moves.append(coord.add(Move.DOWN_LEFT))
            if self.check_down_right(piece, coord):
                moves.append(coord.add(Move.DOWN_RIGHT))

        return moves
               
    def check_up_left(self, piece: Piece, coord: Coordinate) -> bool:
        new_coord = coord.add(Move.UP_LEFT)
        return new_coord.check_valid()

    def check_up_right(self, piece: Piece, coord: Coordinate) -> bool:
        new_coord = coord.add(Move.UP_RIGHT)
        return new_coord.check_valid()

    def check_down_right(self, piece: Piece, coord: Coordinate) -> bool:
        new_coord = coord.add(Move.DOWN_RIGHT)
        return new_coord.check_valid()

    def check_down_left(self, piece: Piece, coord: Coordinate) -> bool:
        new_coord = coord.add(Move.UP_LEFT)
        return new_coord.check_valid()


board = Board()
piece = Piece(Team.X, Direction.DOWN)
board.place(piece, Coordinate(0, 1))
print(board)
moves = board.list_moves(Coordinate(0, 1))
print(moves)
