import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block
pygame.init()

      
clock = pygame.time.Clock()
W, H = 540, 960
fps = 40

running = True
field = Field(W, H)  # Création d'une instance avec taille personnalisée
field.screen.fill((250, 250, 250))

block_size = (40, 40)  # Taille des blocs
image_size = (50, 50)  # Taille des images
Block.load_images(image_size)
Block.load_sounds()

bot_placement_l = int (field.size[0] / 2)
placement_w = int (field.size[1]/3)
walls = [[0, placement_w, 1000, 10], [bot_placement_l, placement_w, 10, 1000]]

def set_invert():
    Field.invert = Block.invert = not Field.invert


#pygame.draw.line(field, [255,255,255], start_pos, end_pos)

Block.spawn_random_block( 10, 0, [0,field.size[0]], [0,placement_w])
Block.spawn_random_block( 10, 2, [0,bot_placement_l], [placement_w,field.size[1]] )
Block.spawn_random_block( 10, 1, [bot_placement_l,field.size[0]], [placement_w,field.size[1]])



SPAWN_EVENT = pygame.USEREVENT + 1
set_timer = False

click = False

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == SPAWN_EVENT:
        #     Block.spawn_random_block(block_size, 1, 0, [0,field.size[0]], [0,placement_w])
        #     Block.spawn_random_block(block_size, 1, 1, [0,bot_placement_l], [placement_w,field.size[1]] )
        #     Block.spawn_random_block(block_size, 1, 2, [bot_placement_l,field.size[0]], [placement_w,field.size[1]])


    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     if not click:
    #         click = True
    #         field.invert = not field.invert

    # if event.type == pygame.MOUSEBUTTONUP:
    #     click = False

    #if(not field.invert) : field.screen.fill((field.color)) 
    #else: field.screen.fill((field.color_invert))
    
    field.draw_background()
    
    for block in Block.block_list:
        if Block.test:
            block.move()
            if not block.collide : block.detect_collision(field.size, walls)
            field.screen.blit(block.image, block.image_rect)
            #pygame.draw.rect(field.screen, (0, 0, 0), (block.pos[0], block.pos[1], block.size[0], block.size[1]), 1) 
            for w in walls:
                pygame.draw.rect(field.screen, (0, 0, 0), (w[0], w[1], w[2], w[3]))  # Dessine le mur en noir

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click the mouse to remove walls")
                Block.test = False
        else:
            block.move()
            if not block.collide : block.detect_collision(field.size)
            field.screen.blit(block.image, block.image_rect)
            #pygame.draw.rect(field.screen, (0, 0, 0), (block.pos[0], block.pos[1], block.size[0], block.size[1]), 1)  # Dessine le contour du bloc en noir

        for block in Block.block_list:
            block.collide = False
    
    # if Block.test == False and not set_timer:
    #     pygame.time.set_timer(SPAWN_EVENT, 3000) 
    #     set_timer = True

    pygame.display.flip()  # Met à jour l'affichage
pygame.quit()






