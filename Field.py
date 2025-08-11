import pygame

class Field:
    def __init__(self, length=400, width=400):
        self.length = length
        self.width = width
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption("Mon terrain")

    def draw(self):
        """Dessine le contenu du terrain"""
        self.screen.fill((0, 0, 0))  # Fond vert
        pygame.display.flip()  # Met à jour l'écran
