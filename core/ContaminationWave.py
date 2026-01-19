import pygame
import random

class ContaminationWave:
    def __init__(self, x: float, y: float, max_radius: int):
        self.pos = pygame.Vector2(x, y)
        self.radius = 0.0
        self.max_radius = max_radius
        self.alpha = 150  # Transparence initiale (0-255)
        self.growth_speed = 4.0 # Vitesse d'élargissement

    def update(self) -> bool:
        """Fait grandir l'onde. Retourne False quand l'onde est finie."""
        self.radius += self.growth_speed
        # La transparence diminue à mesure que le cercle grandit
        self.alpha = max(0, 150 - (self.radius / self.max_radius) * 150)
        return self.radius < self.max_radius

    def draw(self, surface: pygame.Surface):
        # Création d'une surface temporaire pour gérer l'alpha (transparence)
        temp_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        # On dessine un cercle vide (épaisseur 2) pour l'effet d'onde
        pygame.draw.circle(temp_surface, (50, 50, 50, int(self.alpha)), (self.max_radius, self.max_radius), int(self.radius), 2)
        # On blit le cercle centré sur la position de l'onde
        surface.blit(temp_surface, (self.pos.x - self.max_radius, self.pos.y - self.max_radius))