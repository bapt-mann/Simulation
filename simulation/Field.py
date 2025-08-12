import pygame

class Field:
    def __init__(self, length=400, width=400):
        self.size = [length, width]
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
        pygame.display.set_caption("Mon terrain")

    def draw(self):
        """Dessine le contenu du terrain"""
        self.screen.fill((0, 0, 0))  # Fond vert
        pygame.display.flip()  # Met à jour l'écran
