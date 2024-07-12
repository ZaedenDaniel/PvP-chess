import pygame
import os
################################################################
from sound import Sound
from theme import Theme
#################################################################
class Config:

  def __init__(self):
    self.themes = []
    self._add_themes()
    self.idx = 0
    self.theme = self.themes[self.idx]

    self.move_sound = Sound(
      os.path.join('assets/sounds/move.wav'))
    self.capure_sound = Sound(
      os.path.join('assets/sounds/capture.wav'))


  def change__theme(self):
    self.idx += 1
    self.idx %= len(self.themes)
    self.theme = self.themes[self.idx]


  def _add_themes(self):
    red = Theme(
          light_bg=(255, 200, 200), dark_bg=(200, 0, 0),
          light_trace=(255, 150, 150), dark_trace=(150, 0, 0),
          light_moves=(40, 40, 40), dark_moves=(10, 10, 10)
      )
    black = Theme(
          light_bg=(220, 220, 220), dark_bg=(50, 50, 50),
          light_trace=(180, 180, 180), dark_trace=(30, 30, 30),
          light_moves=(140, 190, 180), dark_moves=(40, 90, 80)
      )
    brown = Theme(
          light_bg=(222, 184, 135), dark_bg=(139, 69, 19),
          light_trace=(210, 180, 140), dark_trace=(160, 82, 45),
          light_moves=(40, 40, 40), dark_moves=(10, 10, 10)
      )
    green = Theme(
          light_bg=(144, 238, 144), dark_bg=(34, 139, 34),
          light_trace=(152, 251, 152), dark_trace=(60, 179, 113),
          light_moves=(40, 40, 40), dark_moves=(10, 10, 10)
      )

    self.themes = [green, red, black, brown]