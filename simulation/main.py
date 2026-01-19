import pygame
import random
from constants import *
from ResourceManager import ResourceManager
from Simulation import Simulation
from Block import Block

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Création de la simulation (Définit le mode vidéo)
    sim = Simulation(SCREEN_WIDTH, SCREEN_HEIGHT)
    # Chargement des ressources
    ResourceManager.load(ELEMENT_RULES.keys(), (40, 40))

    #  Configuration initiale du terrain
    wall_height_pos = SCREEN_HEIGHT // 3
    middle_x = SCREEN_WIDTH // 2
    
    sim.add_wall(0, wall_height_pos, SCREEN_WIDTH, 10)         # Mur horizontal
    sim.add_wall(middle_x, wall_height_pos, 10, SCREEN_HEIGHT) # Mur vertical bas

    block_number = 30
    block_size = 20

    #region Spawn des blocs par zones
    # Zone 1 : Haut (Feu)
    for _ in range(block_number):
        x = random.randint(20, SCREEN_WIDTH - 60)
        y = random.randint(20, wall_height_pos - 60)
        sim.blocks.append(Block(x, y, block_size, "red"))

    # Zone 2 : Bas Gauche (Plante)
    for _ in range(block_number):
        x = random.randint(20, middle_x - 60)
        y = random.randint(wall_height_pos + 20, SCREEN_HEIGHT - 60)
        sim.blocks.append(Block(x, y, block_size, "green"))

    # Zone 3 : Bas Droite (Eau)
    for _ in range(block_number):
        x = random.randint(middle_x + 20, SCREEN_WIDTH - 60)
        y = random.randint(wall_height_pos + 20, SCREEN_HEIGHT - 60)
        sim.blocks.append(Block(x, y, block_size, "blue"))
    #endregion

    sim.implement_black_block(middle_x - 25, wall_height_pos - 20, 60)

    # Boucle principale
    running = True
    while running:
        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                sim.walls.pop(0)
                sim.walls.pop(0)

                print("Barrières supprimées")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: # Appuyer sur 'I' pour inverser les règles
                    sim.invert_mode = not sim.invert_mode
                    print(f"Mode Inversé : {sim.invert_mode}")

        # --- Mise à jour de la physique et des règles ---
        sim.update()

        # --- Dessin ---
        sim.draw()

        # --- Contrôle du framerate ---
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()