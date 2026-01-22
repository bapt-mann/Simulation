import random
import pygame
from constants import ELEMENT_RULES, DETECTION_RADIUS, MAX_FORCE

class AiManager:

    @staticmethod
    def wandering_block_ai(block):
        wander_force = pygame.Vector2(
                        random.uniform(-MAX_FORCE, MAX_FORCE), 
                        random.uniform(-MAX_FORCE, MAX_FORCE)
                    )
        block.apply_force(wander_force)
        
    @staticmethod
    def following_block_ai(block, target_block):
        """Fait suivre un autre bloc au bloc."""
        block.apply_force(block.seek(target_block.pos))

    @staticmethod
    def flee_block_ai(block, simulation):
        closest_danger = None
        min_dist = DETECTION_RADIUS

        # Utilisation des chunks pour optimiser la recherche
        cx, cy = block.key
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_key = (cx + dx, cy + dy)
                if neighbor_key in simulation.grid:
                    for other in simulation.grid[neighbor_key]:
                        if other == block: continue
                        
                        dist = block.pos.distance_to(other.pos)
                        if dist < min_dist:
                            # PRIORITÉ 1 : Le bloc noir est le danger ultime
                            if other.type == "black":
                                closest_danger = other.pos
                                min_dist = dist
                            # PRIORITÉ 2 : Le prédateur naturel (si pas de noir à proximité)
                            elif closest_danger is None and block.type == ELEMENT_RULES[other.type]["beats"]:
                                closest_danger = other.pos
                                min_dist = dist

        # Application de la fuite si un danger est détecté
        if closest_danger:
            # On fuit le bloc noir ou le prédateur
            block.apply_force(block.flee(closest_danger) * 2.0)
            return True
        return False

    @staticmethod
    def pursue_block_ai(block, simulation):
        closest_prey = None
        min_dist = DETECTION_RADIUS

        # Utilisation des chunks pour optimiser la recherche
        cx, cy = block.key
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_key = (cx + dx, cy + dy)
                if neighbor_key in simulation.grid:
                    for other in simulation.grid[neighbor_key]:
                        if other == block: continue
                        
                        dist = block.pos.distance_to(other.pos)
                        if dist < min_dist:
                            # On cherche une proie naturelle
                            if ELEMENT_RULES[block.type]["beats"] == other.type:
                                closest_prey = other.pos
                                min_dist = dist

        # Application de la poursuite si une proie est détectée
        if closest_prey:
            block.apply_force(block.seek(closest_prey) * 1.5)
            return True
        return False

    @staticmethod
    def manage_block_ai(simulation):
        """Gère le comportement AI des blocs dans la simulation."""
        for b in simulation.blocks:
            if simulation.start_wall :
                AiManager.wandering_block_ai(b)
                continue
            if b.type == "black":
                if simulation.first_black_block == b :
                    AiManager.pursue_block_ai(b, simulation)
                else:
                    AiManager.following_block_ai(b, simulation.first_black_block)
                continue
            # CAS 1 : FUIR LES DANGERS
            if AiManager.flee_block_ai(b, simulation):
                continue  # On passe au bloc suivant, pas besoin de chercher de proies
            # CAS 2 : POURSUITE DES PROIES
            if AiManager.pursue_block_ai(b, simulation):
                continue
            # CAS 3 : COMPORTEMENT ERRANT (WANDER)
            wander_force = pygame.Vector2(
                random.uniform(-MAX_FORCE, MAX_FORCE),
                random.uniform(-MAX_FORCE, MAX_FORCE)
            )
            b.apply_force(wander_force)