import pygame
import random
from Field import Field  # Import direct de la classe
from Block import Block
pygame.init()

      
clock = pygame.time.Clock()
W, H = 650, 800

running = True
field = Field(W, H)  # Création d'une instance avec taille personnalisée
field.screen.fill((250, 250, 250))

block_size = (40, 40)  # Taille des blocs
image_size = (60, 60)  # Taille des images
Block.load_images(image_size)
Block.load_sounds()
block_list = []


H_top = H // 3  # exemple : 1/3 de l'écran pour la bande du haut

# Bande horizontale du haut
top_rect = (0, 0, W, H_top)

# Colonne gauche en bas
left_rect = (0, H_top, W // 2, H - H_top)

# Colonne droite en bas
right_rect = (W // 2, H_top, W // 2, H - H_top)

bot_placement_l = int (field.size[0] / 2)

placement_w = int (field.size[1]/3)

def set_invert():
    Field.invert = Block.invert = not Field.invert


#pygame.draw.line(field, [255,255,255], start_pos, end_pos)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(image_size[0], field.size[0]-image_size[0]), random.randint(image_size[1], placement_w-image_size[1]), 1)
    block_list.append(block)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(image_size[0], bot_placement_l-image_size[0]), random.randint(placement_w, field.size[1]-image_size[1]), 2)
    block_list.append(block)

for _ in range(10):
    block = Block(block_size[0], block_size[1], random.randint(bot_placement_l-image_size[0], field.size[0]-image_size[0]), random.randint(placement_w, field.size[1]-image_size[1]), 0)
    block_list.append(block)
click = False

while running:
    clock.tick(20)
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
            block.detect_collision(field.size)
            field.screen.blit(block.image, block.image_rect)

    pygame.display.flip()  # Met à jour l'affichage
pygame.quit()






