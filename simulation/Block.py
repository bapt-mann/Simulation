import os
import pygame
import random
from block_type import Type
class Block:
    block_list = []
    color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    BASE_DIR = os.path.dirname(__file__)  # Dossier du fichier actuel
    IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
    images = {}

    SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")
    sounds = {}

    test = True
    invert = False

    def __init__(self, _width, _height, _pos_x, _pos_y, _type):

        Block.block_list.append(self)  # Ajoute l'instance à la liste des blocs 

        self.size = [_width, _height]
        self.pos = [_pos_x, _pos_y] 

        self.velocity = [random.randint(1, 3), random.randint(1, 3)]

        self.negative_x = random.randint(0, 1)
        self.negative_y = random.randint(0, 1)

        if self.negative_x == 1: self.velocity[0] = -self.velocity[0]
        if self.negative_y == 1: self.velocity[1] = -self.velocity[1]

        # self.temp1 = random.random()*6
        # self.temp = (3 - self.temp1) if self.temp1 < 3 else (self.temp1 - 6)

        self.block = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.color = Block.color_list[_type]

        self.collide = False

        # Attribution d'une image depuis le cache
        if _type == 0:
            self.image = Block.images["fire"]
            self.type = Type.fire
        elif _type == 1:
            self.image = Block.images["water"]
            self.type = Type.water
        else:
            self.image = Block.images["plant"]
            self.type = Type.plant
        
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.block.center 


    def load_images(size):
        Block.images["water"] = pygame.transform.scale(
            pygame.image.load(os.path.join(Block.IMG_DIR, "water.png")).convert_alpha(),
            size
        )
        Block.images["fire"] = pygame.transform.scale(
            pygame.image.load(os.path.join(Block.IMG_DIR, "fire.png")).convert_alpha(),
            size
        )
        Block.images["plant"] = pygame.transform.scale(
            pygame.image.load(os.path.join(Block.IMG_DIR, "plant.png")).convert_alpha(),
            size
        )

    def load_sounds():
        Block.sounds["water"] = pygame.mixer.Sound(os.path.join(Block.SOUND_DIR, "water_sound.mp3"))
        Block.sounds["water"].set_volume(0.2)

        Block.sounds["fire"] = pygame.mixer.Sound(os.path.join(Block.SOUND_DIR, "fire_sound.mp3"))
        Block.sounds["fire"].set_volume(0.2)

        Block.sounds["plant"] = pygame.mixer.Sound(os.path.join(Block.SOUND_DIR, "plant_sound.mp3"))
        Block.sounds["plant"].set_volume(0.2)

    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.block = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.block.center 

    def detect_collision_field(self, screen_size=[400, 400]):
        # Collision avec les bords
        for i in range(2):
            if self.pos[i] < 0:
                self.pos[i] = 0
                self.velocity[i] = -self.velocity[i]
            elif self.pos[i] + self.size[i] > screen_size[i]:
                self.pos[i] = screen_size[i] - self.size[i]
                self.velocity[i] = -self.velocity[i]


    def detect_collision_blocks(self):
        # Collision avec les autres blocs
        for other in Block.block_list:
            if other != self and self.block.colliderect(other.block):
                self.switch_to(other)
                other.switch_to(self)

                self.collide = True
                other.collide = True

                dx = (self.block.centerx - other.block.centerx)
                dy = (self.block.centery - other.block.centery)

                overlap_x = (self.size[0] / 2 + other.size[0] / 2) - abs(dx)
                overlap_y = (self.size[1] / 2 + other.size[1] / 2) - abs(dy)

                if overlap_x < overlap_y:
                    # Déplacer horizontalement pour ne plus être en contact
                    if dx > 0:
                        self.pos[0] += overlap_x
                    else:
                        self.pos[0] -= overlap_x
                    self.velocity[0] = -self.velocity[0]
                    
                else:
                    # Déplacer verticalement pour ne plus être en contact
                    if dy > 0:
                        self.pos[1] += overlap_y
                    else:
                        self.pos[1] -= overlap_y
                    self.velocity[1] = -self.velocity[1]

                # Mettre à jour le rect après correction
                self.block.topleft = self.pos

    def collision_block(self):
        return

    def detect_collision(self, screen_size=[400, 400]):
        self.detect_collision_field(screen_size)
        self.detect_collision_blocks()

    def switch_to(self, other):
        addition = self.type.value + other.type.value
        # FIRE = 1
        # PLANT = 2
        # WATER = 4
        match addition:
            case 3:  # fire + plant
                self.set_state("fire" if not Block.invert else "plant")
                return
            case 5:  # water + fire
                self.set_state("water" if not Block.invert else "fire")
                return
            case 6:  # plant + water
                self.set_state("plant" if not Block.invert else "water")
                return
            case _:  return
        return

    def set_state(self, type):
        Block.sounds[type].play()
        self.image = Block.images[type]
        self.type = Type[type]

    def spawn_random_block(block_size, block_number, type, range_x=[0,100], range_y=[0,100]):
        block_list = []
        _width = block_size[0]
        _height = block_size[1]

        _pos_x = range_x[1]/2 - block_size[0]/2
        _pos_y = range_y[1]/2 - block_size[1]/2

        for i in range (block_number) :
            
            if i != 0 : 
                _pos_x = random.randint(int (range_x[0]), int(range_x[1] - block_size[0]))
                _pos_y = random.randint(int(range_y[0]), int(range_y[1] - block_size[1]))
            block = Block( _width, _height, _pos_x, _pos_y, type)
            block_list.append(block)

        return block_list
