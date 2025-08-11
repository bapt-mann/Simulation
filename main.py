import pygame
from Field import Field  # Import direct de la classe
from Block import Block

pygame.init()

running = True
field = Field(800, 600)  # Création d'une instance avec taille personnalisée
block = Block(10, 10, 100, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    field.screen.fill((0, 0, 0))  # Nettoyer écran avant de dessiner
    pygame.draw.rect(field.screen, block.color, block.block)
    pygame.display.flip()  # Met à jour l'affichage

pygame.quit()



