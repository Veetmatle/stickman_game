import pygame as py
from buildings import Buildings

class Castle(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(844, 197, 15, 42), )