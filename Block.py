import os
import pygame

class Block :
    def __init__(self, width, height, pos_x, pos_y):
        
        self.block = pygame.Rect(pos_x, pos_y, width, height)
        self.color = (255, 0, 0)  # Rouge