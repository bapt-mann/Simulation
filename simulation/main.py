import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block

pygame.init()
clock = pygame.time.Clock()

running = True
field = Field(720, 1000)  # Création d'une instance avec taille personnalisée
field.screen.fill((200, 200, 200))

block_size = (30, 30)  # Taille des blocs
image_size = (50, 50)  # Taille des images
Block.load_images(image_size)
block_list = []

for _ in range(20):
    block = Block(block_size[0], block_size[1], random.randint(0, 720), random.randint(0, 1000), 1)
    block_list.append(block)

for _ in range(20):
    block = Block(block_size[0], block_size[1], random.randint(0, 720), random.randint(0, 1000), 2)
    block_list.append(block)

for _ in range(20):
    block = Block(block_size[0], block_size[1], random.randint(0, 720), random.randint(0, 1000), 0)
    block_list.append(block)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    field.screen.fill((100, 100, 100))  # Nettoyer écran avant de dessiner

    for block in block_list:
        block.move()
        block.detect_collision(field.size)
        field.screen.blit(block.image, block.image_rect)

    pygame.display.flip()  # Met à jour l'affichage

pygame.quit()






