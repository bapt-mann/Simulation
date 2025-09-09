import pygame

class Field:
    
    def __init__(self, length=720, width=1000):
        self.size = [length, width]
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
        pygame.display.set_caption("Mon terrain")
        self.invert = False
        # couleurs du dégradé sombre
        self.top_color = (30, 30, 40)    # bleu nuit/gris très foncé
        self.bottom_color = (60, 60, 80) # gris bleuté un peu plus clair
#top_color = (40, 20, 60) bottom_color = (80, 40, 120)
    def draw_background(self):
        """Dessine un dégradé vertical"""
        height = self.screen.get_height()
        for y in range(height):
            ratio = y / height
            if not self.invert:
                r = int(self.top_color[0] * (1 - ratio) + self.bottom_color[0] * ratio)
                g = int(self.top_color[1] * (1 - ratio) + self.bottom_color[1] * ratio)
                b = int(self.top_color[2] * (1 - ratio) + self.bottom_color[2] * ratio)
            else:
                r = int(self.bottom_color[0] * (1 - ratio) + self.top_color[0] * ratio)
                g = int(self.bottom_color[1] * (1 - ratio) + self.top_color[1] * ratio)
                b = int(self.bottom_color[2] * (1 - ratio) + self.top_color[2] * ratio)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen.get_width(), y))

    def draw(self):
        """Dessine le contenu du terrain"""
        self.screen.fill(0,0,0) 
        pygame.display.flip()  # Met à jour l'écran

