from const import *
from square import Square
from piece import *
from move import Move
import copy 
class Board:

  def __init__(self):
    self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]

    self.last_move =None
    self._create()
    self._add_pieces('white')
    self._add_pieces('black')


  def move(self, piece, move):
    initial = move.initial
    final = move.final
    self.squares[initial.row][initial.col].piece = None
    self.squares[final.row][final.col].piece = piece

    if isinstance(piece,Pawn):
      self.Promote(piece, final)


    piece.moved = True
    piece.clear_moves()
    self.last_move = Move(initial, final)

  def valid_move(self, piece, move):
    return move in piece.moves

  def calc_moves(self, piece, row, col, bool = True):

    def king_moves():
      adjs = [
        (row+0, col+1),
        (row+0, col-1),
        (row+1, col+1),
        (row+1, col+0),
        (row-1, col+0),
        (row-1, col-1),
        (row+1, col-1),
        (row-1, col+1)
      ]

      for poss in adjs:
        possible_move_row, possible_move_col = poss

        if Square.in_range(possible_move_row, possible_move_col):
          if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
            initial = Square(row, col)
            final = Square(possible_move_row, possible_move_col)
            move = Move(initial, final)
            piece.add_move(move)

      if not piece.moved:
        l_rook = self.squares[row][0].piece
        r_rook = self.squares[row][7].piece
        if isinstance(l_rook, Rook):
          if not l_rook.moved:
            for c in range(1, 4):
              if self.squares[row][c].has_piece():
                break 
              
              if c == 3:
                piece.l_rook = l_rook
                initial = Square(row, 0)
                final = Square(row, 3)
                moveR = Move(initial, final)

                initial = Square(row, col)
                final = Square(row, 2)
                moveK = Move(initial, final)

                if bool:
                  if not self.in_check(piece, moveK) and not self.in_check(l_rook, moveR):
                    l_rook.add_move(moveR)
                    piece.add_move(moveK)

                else:
                  l_rook.add_move(moveR)
                  piece.add_move(moveK)

        if isinstance(r_rook, Rook):
            if not r_rook.moved:
               for c in range(5, 7):
                if self.squares[row][c].has_piece():
                  break 
                if c == 6:
                  piece.r_rook = r_rook
                  initial = Square(row, 7)
                  final = Square(row, 5)
                  moveR = Move(initial, final)

                  initial = Square(row, col)
                  final = Square(row, 6)
                  moveK = Move(initial, final)
            
                  if bool:
                    if not self.in_check(piece, moveK) and not self.in_check(r_rook, moveR):
                      r_rook.add_move(moveR)
                      piece.add_move(moveK)

                  else:
                    r_rook.add_move(moveR)
                    piece.add_move(moveK)



    def straightline_moves(incrs):
      for inc in incrs:
        row_incr, col_incr = inc
        possible_move_row = row + row_incr
        possible_move_col = col + col_incr

        while True:
          if Square.in_range(possible_move_row, possible_move_col):

            initial = Square(row, col)
            final_piece =self.squares[possible_move_row][possible_move_col].piece
            final = Square(possible_move_row, possible_move_col, final_piece)
            move = Move(initial, final)
            
            if self.squares[possible_move_row][possible_move_col].isempty():
              if bool:
                if not self.in_check(piece, move):
                  piece.add_move(move)
              else:
                piece.add_move(move)

            elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
              break

            elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
              if bool:
                if not self.in_check(piece, move):
                  piece.add_move(move)

              else:
                piece.add_move(move)
              break

          else: break

          possible_move_row = possible_move_row + row_incr
          possible_move_col = possible_move_col + col_incr

    def knight_moves():
      possible_moves = [
        (row-2, col+1),
        (row-1, col+2),
        (row+1, col+2),
        (row+2, col+1),
        (row+2, col-1),
        (row+1, col-2),
        (row-2, col-1),
        (row-1, col-2)
      ]

      for poss in possible_moves:
        possible_move_row, possible_move_col = poss

        if Square.in_range(possible_move_row, possible_move_col):
          if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
            initial = Square(row, col)
            final_piece =self.squares[possible_move_row][possible_move_col].piece
            final = Square(possible_move_row, possible_move_col, final_piece)
            move = Move(initial, final)
            
            if bool:
              if not self.in_check(piece, move):
                piece.add_move(move)
              else: break

            else:
              piece.add_move(move)

                      
    def pawn_moves():
      steps = 1 if piece.moved else 2

      #for moving forward
      start = row + piece.dir
      end = row + (piece.dir * (1+steps))
      for possible_move_row in range(start, end, piece.dir):
        if Square.in_range(possible_move_row):
          if self.squares[possible_move_row][col].isempty():
            initial = Square(row, col)
            final = Square(possible_move_row, col)
            move = Move(initial, final)
            
            if bool:
              if not self.in_check(piece, move):
                piece.add_move(move)

            else:
              piece.add_move(move)

          else: break
        
        else: break

      #for attacking
      possible_move_row = row + piece.dir
      possible_move_cols = [col - 1, col + 1]
      for possible_move_col in possible_move_cols:
        if Square.in_range(possible_move_row, possible_move_col):
          if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):

            initial = Square(row, col)
            final_piece =self.squares[possible_move_row][possible_move_col].piece
            final = Square(possible_move_row, possible_move_col, final_piece)
            move = Move(initial, final)
            piece.add_move(move)
    

    if isinstance(piece, Pawn):
      pawn_moves()

    elif isinstance(piece, Knight):
      knight_moves()

    elif isinstance(piece, Bishop):
      straightline_moves([
        (-1, 1),
        (-1, -1),
        (1, 1),
        (1, -1)
      ])

    elif isinstance(piece, Rook):
      straightline_moves([
        (1, 0),
        (-1, 0),
        (0, -1),
        (0, 1)
      ])

    elif isinstance(piece, King):

      king_moves()

    elif isinstance(piece, Queen):
      straightline_moves([
        (-1, 1),
        (-1, -1),
        (1, 1),
        (1, -1),
        (1, 0),
        (-1, 0),
        (0, -1),
        (0, 1)
      ])


  def _create(self):
    for row in range(ROWS):
      for col in range(COLS):
        self.squares[row][col] = Square(row, col)


  def _add_pieces(self, color):

    row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

    for col in range (COLS):
      self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

    self.squares[row_other][1] = Square(row_other, 1, Knight(color))
    self.squares[row_other][6] = Square(row_other, 6, Knight(color))
    
    self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
    self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
    
    self.squares[row_other][0] = Square(row_other, 0, Rook(color))
    self.squares[row_other][7] = Square(row_other, 7, Rook(color))
    
    self.squares[row_other][3] = Square(row_other, 3, Queen(color))
    self.squares[row_other][4] = Square(row_other, 4, King(color))

  def Promote(self, piece, final):
    if final.row == 0 or final.row == 7:
      self.squares[final.row][final.col].piece = Queen(piece.color)


  def castling(self, initial, final):
    return abs(initial.col - final.col) == 2

  def in_check(self, piece, move):
    t_piece= copy. deepcopy(piece)
    t_board = copy.deepcopy(self)
    t_board.move(t_piece, move)

    for row in range(ROWS):
      for col in range(COLS):
        if t_board.squares[row][col].has_rival_piece(t_piece.color):
            pie = t_board.squares[row][col].piece
            t_board.calc_moves(pie, row, col, bool=False)
            for m in pie.moves:
              if isinstance(m.final.piece, King):
                return True
              
    return False
