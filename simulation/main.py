import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block

pygame.init()


clock = pygame.time.Clock()

running = True
field = Field(720, 1000)  # Création d'une instance avec taille personnalisée
field.screen.fill((250, 250, 250))

block_size = (50, 50)  # Taille des blocs
image_size = (80, 80)  # Taille des images
Block.load_images(image_size)
Block.load_sounds()
block_list = []

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(0, 300), random.randint(500, 1000), 1)
    block_list.append(block)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(400, 700), random.randint(500, 1000), 2)
    block_list.append(block)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(100, 600), random.randint(100, 400), 0)
    block_list.append(block)
click = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if event.type == pygame.MOUSEBUTTONDOWN:
        if not click:
            click = True
            field.invert = not field.invert

    if event.type == pygame.MOUSEBUTTONUP:
        click = False

    #if(not field.invert) : field.screen.fill((field.color)) 
    #else: field.screen.fill((field.color_invert))
    field.draw_background()
    
    for block in block_list:
        if Block.test:
            field.screen.blit(block.image, block.image_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click hte mouse to move the block")
                Block.test = False
        else:
            block.move()
            block.detect_collision(field.invert,field.size)
            field.screen.blit(block.image, block.image_rect)

    pygame.display.flip()  # Met à jour l'affichage
pygame.quit()






