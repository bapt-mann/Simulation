import random
import pygame
from constants import ELEMENT_RULES, DETECTION_RADIUS, MAX_FORCE, MAX_SPEED

class AiManager:

    @staticmethod
    def wandering_block_ai(block):
        # Au lieu d'un random total, on ajoute juste une petite variation à la direction actuelle
        steer = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        block.apply_force(steer)
        
    @staticmethod
    def following_block_ai(block, simulation, target_block):
        """Comportement de meute : forme un cercle dynamique autour du leader"""
        # 1. RAYON DE L'ANNEAU (La zone où ils doivent se situer)
        TARGET_DIST = 70  # Distance idéale par rapport au leader
        dist = block.pos.distance_to(target_block.pos)

        # Force pour rejoindre l'anneau (Seek si trop loin, Flee si trop proche)
        if dist > TARGET_DIST + 10:
            # On utilise 'arrive' pour éviter les secousses
            block.apply_force(block.arrive(target_block.pos, slowing_radius=100))
        elif dist < TARGET_DIST - 10:
            block.apply_force(block.flee(target_block.pos) * 1.5)

        # 2. SÉPARATION (La clé pour former un cercle et pas un pâté)
        # On repousse les autres blocs noirs (sauf le leader)
        personal_space = 15 # Espace entre chaque suiveur
        for other in simulation.black_blocks:
            if other == block or other == target_block:
                continue
            
            dist_other = block.pos.distance_to(other.pos)
            if dist_other < personal_space:
                # Force de répulsion inversement proportionnelle à la distance
                repel_force = (block.pos - other.pos).normalize() * (MAX_FORCE * 2)
                block.apply_force(repel_force)

        # 3. SYNCHRONISATION (Suivre le mouvement du leader)
        if target_block.vel.length() > 0.5:
            # On donne une petite impulsion dans la même direction que le leader
            block.apply_force(target_block.vel.normalize() * (MAX_FORCE * 0.8))

        # On stabilise le bloc dans sa zone
        block.vel *= 0.95

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
                            elif closest_danger is None and block.type in ELEMENT_RULES[other.type]["beats"]:
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
                            if other.type in ELEMENT_RULES[block.type]["beats"]:
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
                AiManager.flee_block_ai(b, simulation)
                continue
            if b.type == "black":
                if simulation.first_black_block == b :
                    AiManager.pursue_block_ai(b, simulation)
                else:
                    b.max_speed = MAX_SPEED * 1.5
                    AiManager.following_block_ai(b, simulation, simulation.first_black_block)
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