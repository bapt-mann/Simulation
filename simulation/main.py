import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block

pygame.init()


clock = pygame.time.Clock()

running = True
field = Field(650, 800)  # Création d'une instance avec taille personnalisée
field.screen.fill((250, 250, 250))

block_size = (40, 40)  # Taille des blocs
image_size = (60, 60)  # Taille des images
Block.load_images(image_size)
Block.load_sounds()
block_list = []


bot_placement_l = int (field.size[0] / 2)

placement_w = int (field.size[1]/3)



#pygame.draw.line(field, [255,255,255], start_pos, end_pos)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(10, field.size[0]-10), random.randint(0, placement_w), 1)
    block_list.append(block)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(10, bot_placement_l), random.randint(placement_w, field.size[1]-10), 2)
    block_list.append(block)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(bot_placement_l, field.size[0]-10), random.randint(placement_w, field.size[1]-10), 0)
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






