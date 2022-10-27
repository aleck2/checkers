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

    def is_simple_move(self, obj) -> int:
        """if row differs by 1, simple jump"""
        return abs(self.r - obj.r) == 1

    def is_kill_move(self, obj) -> int:
        """if row differs by 2, kill"""
        return abs(self.r - obj.r) == 2

    def get_kill_coordinate(self, obj):
        """return coordinate of the leapfrogged space"""
        return Coordinate((self.r + obj.r) // 2, (self.c + obj.c) // 2)

    def is_inbounds(self) -> bool:
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
        if not self.at(coord):
            # if empty (None)
            self.board[coord.r][coord.c] = piece
            return True
        
        return False

    def remove(self, coord: Coordinate) -> bool:
        """ place a Piece/None on coordinate"""
        if self.at(coord):
            # if something at this spot
            self.board[coord.r][coord.c] = None
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
            self.remove(old_coord)

            if new_coord.is_kill_move(old_coord):
                # nullify killed spot
                self.remove(new_coord.get_kill_coordinate(old_coord))

            return True

        return False
    
    def list_moves(self, coord: Coordinate) -> list[Coordinate]:
        """
        Return list of possible coordinates
        New coordinate space must be
            1)
             - in bounds
            2)
             - adjacent diagonal space empty (simple move)
             or
             - adjacent diagonal occupied by enemy and subsequent diagnoal empty (kill)
        """
        candidate_coords = []
        piece = self.at(coord)
        if not piece:
            return candidate_coords

        if piece.direction == Direction.UP:

            candidate = self.list_move_helper(coord, Move.UP_LEFT)
            if candidate:
                candidate_coords.append(candidate)

            candidate = self.list_move_helper(coord, Move.UP_RIGHT)
            if candidate:
                candidate_coords.append(candidate)

        elif piece.direction == Direction.DOWN:

            candidate = self.list_move_helper(coord, Move.DOWN_LEFT)
            if candidate:
                candidate_coords.append(candidate)

            candidate = self.list_move_helper(coord, Move.DOWN_RIGHT)
            if candidate:
                candidate_coords.append(candidate)

        else:
            # log an error
            print('* ERROR: piece at {}, {} has no direction'.format(coord.r, coord.c))

        return candidate_coords

    def list_move_helper(self, coord: Coordinate, move: Move) -> Optional[Coordinate]:
        new_coord = coord.add(move)
        if new_coord.is_inbounds():

            if not self.at(new_coord): # simple move into an empty spot
                return new_coord

            # board new_coord occupied by a non null piece
            elif self.at(new_coord).team != self.at(coord).team: # spot occupied by enemy, jump and kill it
                new_coord = new_coord.add(move)
                if new_coord.is_inbounds() and not self.at(new_coord): # can jump into empty spot and kill
                    return new_coord
            else:
                print("no conditions satisfied")

        return None



if __name__ == '__main__':
    def example_kills():
        board = Board()
        print(board)
        board.move(Coordinate(2,1), Coordinate(3,2))
        print(board)
        board.move(Coordinate(3,2), Coordinate(4,1))
        print(board)
        board.move(Coordinate(5,0), Coordinate(3, 2))
        print(board)
        board.move(Coordinate(2,3), Coordinate(4, 1))
        print(board)
        board.move(Coordinate(5,2), Coordinate(3, 0))
        print(board)

    example_kills()

