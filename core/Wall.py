import pygame
import random
from constants import ELEMENT_RULES
from core.ResourceManager import ResourceManager

class Wall :
    def __init__(self, x, y, w, h, image=None, collidable=True, visible=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (50, 50, 50)  # Gris par défaut
        self.image = image
        self.visible = visible
        self.collidable = collidable

    def draw(self, screen):
            if self.image and self.visible:
                screen.blit(self.image, self.rect)
            if not self.image and self.visible:
                pygame.draw.rect(screen, self.color, self.rect)
            else:
                return
