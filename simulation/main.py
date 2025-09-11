import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block
pygame.init()

      
clock = pygame.time.Clock()
W, H = 650, 800
fps = 60

running = True
field = Field(W, H)  # Création d'une instance avec taille personnalisée
field.screen.fill((250, 250, 250))

block_size = (40, 40)  # Taille des blocs
image_size = (60, 60)  # Taille des images
Block.load_images(image_size)
Block.load_sounds()
block_list = []


bot_placement_l = int (field.size[0] / 2)

placement_w = int (field.size[1]/3)

def set_invert():
    Field.invert = Block.invert = not Field.invert


#pygame.draw.line(field, [255,255,255], start_pos, end_pos)

block_list = Block.spawn_random_block(block_size, 10, 0, [0,field.size[0]], [0,placement_w])
block_list.extend( Block.spawn_random_block(block_size, 10, 1, [0,bot_placement_l], [placement_w,field.size[1]] ))
block_list.extend( Block.spawn_random_block(block_size, 10, 2, [bot_placement_l,field.size[0]], [placement_w,field.size[1]]))


click = False

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     if not click:
    #         click = True
    #         field.invert = not field.invert

    # if event.type == pygame.MOUSEBUTTONUP:
    #     click = False

    #if(not field.invert) : field.screen.fill((field.color)) 
    #else: field.screen.fill((field.color_invert))
    
    field.draw_background()
    
    for block in block_list:
        if Block.test:
            field.screen.blit(block.image, block.image_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click the mouse to move the block")
                Block.test = False
        else:
            block.move()
            if not block.collide : block.detect_collision(field.size)
            field.screen.blit(block.image, block.image_rect)
        for block in block_list:
            block.collide = False

    pygame.display.flip()  # Met à jour l'affichage
pygame.quit()






