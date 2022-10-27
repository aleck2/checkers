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

    def __eq__(self, obj):
        return self.r == obj.r and self.c == obj.c

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
        # board filled with no pieces
        self.board = [[None for i in range(COLS)] for r in range(ROWS)]

        # board filed with X's going down
        for r in range(3):
            start = 1 if r % 2 == 0 else 0
            for c in range(start, COLS, 2):
                self.board[r][c] = Piece(Team.X, Direction.DOWN)

        # board filed with O's going up
        for r in range(COLS-1, COLS-4, -1):
            start = 1 if r % 2 == 0 else 0
            for c in range(start, COLS, 2):
                self.board[r][c] = Piece(Team.O, Direction.UP)
        
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
        """ place a piece on coordinate. use primarily for testing"""
        if not self.board[coord.r][coord.c]:
            # if empty (None)
            self.board[coord.r][coord.c] = piece
            return True
        
        return False

    def move(self, old_coord: Coordinate, new_coord: Coordinate) -> bool:
        piece = self.board[old_coord.r][old_coord.c]
        candidates = self.list_moves(old_coord)

        if new_coord in candidates:
            # place piece on new spot
            self.board[new_coord.r][new_coord.c] = piece

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
            if coord.add(Move.UP_LEFT).check_valid():
                moves.append(coord.add(Move.UP_LEFT))
            if coord.add(Move.UP_RIGHT).check_valid():
                moves.append(coord.add(Move.UP_RIGHT))

        elif piece.direction == Direction.DOWN:
            if coord.add(Move.DOWN_LEFT).check_valid():
                moves.append(coord.add(Move.DOWN_LEFT))
            if coord.add(Move.DOWN_RIGHT).check_valid():
                moves.append(coord.add(Move.DOWN_RIGHT))

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
