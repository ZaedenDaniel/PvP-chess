import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
class Game:

  def __init__(self):
    self.next_player = 'white'
    self.hover_square = None
    self.board = Board()
    self.dragger = Dragger()
    self.config = Config()


  def show_bg(self, surface):
    theme = self.config.theme

    for row in range(ROWS):
      for col in range(COLS):
        color = theme.bg.light if (row + col)  % 2 == 0 else theme.bg.dark

        rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

        pygame.draw.rect(surface, color, rect)

  def show_pieces(self, surface):

    for row in range(ROWS):
      for col in range(COLS):
        if self.board.squares[row][col].has_piece():
          piece = self.board.squares[row][col].piece

          if piece is not self.dragger.piece:
            piece.set_texture()
            img = pygame.image.load(piece.texture)
            img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
            piece.texture_rect = img.get_rect(center = img_center)
            surface.blit(img, piece.texture_rect)

  def show_moves(self, surface):
    theme = self.config.theme

    if self.dragger.dragging:
      piece = self.dragger.piece

      for move in piece.moves:
        color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
        
        rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
        
        pygame.draw.rect(surface, color, rect)

  # def show_last_move(self, surface):
  #   if self.board.last_move:
  #     if isinstance(self.board.last_move, Move):
  #       initial = self.board.last_move.initial
  #       final = self.board.last_move.final

  #     for pos in [initial, final]:
  #       color = (244, 247, 116) if (pos.row + pos.col) %  2 == 0 else (172, 195, 51)
  #       rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
  #       pygame.draw.rect(surface, color, rect)


  def show_last_move(self, surface):
    theme = self.config.theme
    
    if self.board.last_move:
      initial = self.board.last_move.initial
      final = self.board.last_move.final

      for pos in [initial, final]:
          color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
          rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
          pygame.draw.rect(surface, color, rect)


  def show_hover(self, surface):
    if self.hover_square:
      color = (116, 247, 116)
      rect = (self.hover_square.col * SQSIZE, self.hover_square.row * SQSIZE, SQSIZE, SQSIZE)
      pygame.draw.rect(surface, color, rect, width=5)

  def next_turn(self):
    self.next_player = 'black' if self.next_player == 'white' else 'white'

  def set_hover(self, row, col):
    self.hover_square = self.board.squares[row][col]

  def change_theme(self):
    self.config.change__theme()


  def sound_effect(self, capture = False):
    if capture:
      self.config.capure_sound.play()

    else:
      self.config.move_sound.play()

  def reset_game(self):
      self.__init__()
