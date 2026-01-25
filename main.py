import pygame
import random
from constants import *
from core.managers.ResourceManager import ResourceManager
from core.Simulation import Simulation
from core.Block import Block

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
    gap = 80  # Taille de l'ouverture (le bloc fait 30, donc 80 laisse de la marge)
    half_gap = gap // 2
    
    # Mur horizontal GAUCHE
    sim.add_wall(0, wall_height_pos, middle_x - half_gap, 10) 
    # Mur horizontal DROIT
    sim.add_wall(middle_x + half_gap, wall_height_pos, SCREEN_WIDTH - (middle_x + half_gap), 10)
    # Mur vertical BAS (on commence plus bas pour laisser le trou)
    sim.add_wall(middle_x, wall_height_pos + half_gap, 10, SCREEN_HEIGHT - (wall_height_pos + half_gap))

    block_number = 150
    block_size = 15

    #region Spawn des blocs par zones
    for _ in range(block_number):
        x = random.randint(20, SCREEN_WIDTH - 60)
        y = random.randint(20, wall_height_pos - 60)
        sim.blocks.append(Block(x, y, block_size, "red"))

    for _ in range(block_number):
        x = random.randint(20, middle_x - 60)
        y = random.randint(wall_height_pos + 20, SCREEN_HEIGHT - 60)
        sim.blocks.append(Block(x, y, block_size, "green"))

    for _ in range(block_number):
        x = random.randint(middle_x + 20, SCREEN_WIDTH - 60)
        y = random.randint(wall_height_pos + 20, SCREEN_HEIGHT - 60)
        sim.blocks.append(Block(x, y, block_size, "blue"))
    #endregion

    sim.implement_black_block(middle_x - 10, wall_height_pos, 30)

    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 1000)
    time_left = 3  # Start with 60 seconds

    running = True

    sim.start_wall = True

    # Boucle principale
    running = True
    while running:
        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and sim.start_wall:
                sim.start_wall = False
                for _ in range(len(sim.walls)):
                    sim.walls.pop(0)

                print("Barrières supprimées")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: # Appuyer sur 'I' pour inverser les règles
                    sim.invert_mode = not sim.invert_mode
                    print(f"Mode Inversé : {sim.invert_mode}")
                if event.key == pygame.K_p: # Appuyer sur 'P' pour afficher les types de blocs
                    for b in sim.blocks:
                        print(f"Bloc Type: {b.type} at Position: {b.pos}")
            
            if event.type == TIMER_EVENT and not sim.start_wall and False:
                if time_left > 0:
                    print(f"Time left: {time_left} seconds")
                    time_left -= 1
                else:
                    # sim.black_block_effect()
                    time_left = 3  # Reset timer
                    print("Time's up!")

        # --- Mise à jour de la physique et des règles ---
        sim.update()

        # --- Dessin ---
        sim.draw()

        # --- Contrôle du framerate ---
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()