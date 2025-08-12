import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block

pygame.init()
clock = pygame.time.Clock()

running = True
field = Field(800, 600)  # Création d'une instance avec taille personnalisée
block_list = []

for _ in range(10):
    block = Block(20, 20, random.randint(0, 700), random.randint(0, 500), 1)
    block_list.append(block)

for _ in range(10):
    block = Block(20, 20, random.randint(0, 700), random.randint(0, 500), 2)
    block_list.append(block)

for _ in range(10):
    block = Block(20, 20, random.randint(0, 700), random.randint(0, 500), 0)
    block_list.append(block)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    field.screen.fill((0, 0, 0))  # Nettoyer écran avant de dessiner

    for block in block_list:
        block.move()
        block.detect_collision()
        pygame.draw.rect(field.screen, block.color, block.block)

    pygame.display.flip()  # Met à jour l'affichage

pygame.quit()






