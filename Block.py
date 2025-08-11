import os
import pygame
import random

class Block:
    block_list = []
    color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def __init__(self, _width, _height, _pos_x, _pos_y, _color):

        Block.block_list.append(self)  # Ajoute l'instance à la liste des blocs 

        self.size = [_width, _height]
        self.pos = [_pos_x, _pos_y] 
        self.velocity = [random.randint(1, 3), random.randint(1, 3)]

        self.block = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.color = Block.color_list[_color]


    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.block = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def detect_collision(self):
        # Collision avec les bords
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.velocity[0] = -self.velocity[0]
        elif self.pos[0] + self.size[0] > 800:
            self.pos[0] = 800 - self.size[0]
            self.velocity[0] = -self.velocity[0]

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity[1] = -self.velocity[1]
        elif self.pos[1] + self.size[1] > 600:
            self.pos[1] = 600 - self.size[1]
            self.velocity[1] = -self.velocity[1]

        # Collision avec les autres blocs
        for other in Block.block_list:
            if other != self and self.block.colliderect(other.block):
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
                    self.change_color(other)
                else:
                    # Déplacer verticalement pour ne plus être en contact
                    if dy > 0:
                        self.pos[1] += overlap_y
                    else:
                        self.pos[1] -= overlap_y
                    self.velocity[1] = -self.velocity[1]
                    self.change_color(other)

                # Mettre à jour le rect après correction
                self.block.topleft = self.pos

    def change_color(self, other):
        if self.color == (255, 0, 0) and other == (0, 255, 0):
            self.color = (0, 255, 0)

        elif self.color == (255, 0, 0) and other == (0, 0, 255):
            other.color = (255, 0, 0)

        elif self.color == (0, 255, 0) and other == (0, 0, 255):
            self.color = (0, 255, 0)
        