import pygame
import random
from core.Block import Block
from constants import CHUNK_SIZE, DETECTION_RADIUS, ELEMENT_RULES, COLOR_BG_TOP, COLOR_BG_BOTTOM, MAX_FORCE
from core.Wall import Wall
from core.managers.AiManager import AiManager

class Simulation:
    def __init__(self, width, height):
            self.screen = pygame.display.set_mode((width, height))
            self.rect = self.screen.get_rect()
            self.blocks = []
            self.walls = []
            self.invert_mode = False
            self.grid = {}  # Grille spatiale pour l'optimisation des collisions
            self.start_wall = False
            self.black_blocks = []
            self.max_black_blocks = 600

    def add_wall(self, x, y, w, h):
        wall = Wall(x, y, w, h)
        self.walls.append(wall)

    def remove_walls(self):
        """Vide la liste des murs"""
        self.walls.clear()

    def spawn_block(self, element_type, count, zone_rect, size=40):
        for _ in range(count):
            x = random.randint(zone_rect.left, zone_rect.right - 40)
            y = random.randint(zone_rect.top, zone_rect.bottom - 40)
            self.blocks.append(Block(x, y, size, element_type))

    def implement_black_block(self, x, y, size):
        black_block = Block(x, y, size, 'black')
        self.blocks.append(black_block)
        self.black_blocks.append(black_block)
        print("Bloc noir ajouté aux coordonnées :", black_block.pos.x, black_block.pos.y)
        return

    def infect_to_black(self, target_block):
        """Transforme un bloc en noir et gère la limite de 20"""
        if target_block.type == "black":
            return

        # On mémorise son type actuel pour la retransformation future
        old_type = target_block.type
        
        # Transformation du nouveau bloc
        target_block.change_type("black")
        self.black_blocks.append(target_block)

        # Si on dépasse la limite, on transforme le plus ancien
        if len(self.black_blocks) > self.max_black_blocks:
            oldest_black = self.black_blocks.pop(0)
            # On le retransforme dans le type du bloc qui vient d'être infecté
            oldest_black.change_type(old_type)

    def handle_interactions(self):
        """Optimisation par grille spatiale avec nettoyage"""
        # On vide la grille à chaque frame pour éviter la fuite de mémoire
        self.grid = {} 
        
        for b in self.blocks:
            # Calcul de la cellule (Chunk)
            cx = int(b.rect.centerx // CHUNK_SIZE)
            cy = int(b.rect.centery // CHUNK_SIZE)
            b.key = (cx, cy)

            if b.key not in self.grid:
                self.grid[b.key] = []
            self.grid[b.key].append(b)

        # Gestion des collisions par paires uniques
        checked_pairs = set()
        for (cx, cy), blocks_in_cell in self.grid.items():
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neighbor_key = (cx + dx, cy + dy)
                    if neighbor_key in self.grid:
                        self.check_collision_between_lists(
                            blocks_in_cell, 
                            self.grid[neighbor_key], 
                            checked_pairs
                        )

    def check_collision_between_lists(self, list_a, list_b, checked_pairs):
        """Compare les collisions entre deux listes de blocs"""
        for b1 in list_a:
            for b2 in list_b:
                if b1 == b2:
                    continue      
                # Créer un identifiant unique pour la paire (trié pour l'ordre)
                pair_id = tuple(sorted((id(b1), id(b2))))
                
                if pair_id not in checked_pairs:
                    checked_pairs.add(pair_id)
                    # On utilise ta nouvelle logique vectorielle
                    if b1.resolve_collision(b2):
                        self.resolve_element_fight(b1, b2)

    def resolve_element_fight(self, b1 :Block, b2: Block):
        if b1.type == b2.type: 
            return
            
        # Si l'un des deux est noir, l'autre est infecté
        if b1.type == "black":
            self.infect_to_black(b2)
            return
        if b2.type == "black":
            self.infect_to_black(b1)
            return
        
        winner = b1.type if ELEMENT_RULES[b1.type]["beats"] == b2.type else b2.type
        loser = b2.type if winner == b1.type else b1.type
        
        target_type = winner if not self.invert_mode else loser
        b1.change_type(target_type)
        b2.change_type(target_type)

    def draw_background(self):
        for y in range(self.rect.height):
            ratio = y / self.rect.height
            r = int(COLOR_BG_TOP[0] * (1-ratio) + COLOR_BG_BOTTOM[0] * ratio)
            g = int(COLOR_BG_TOP[1] * (1-ratio) + COLOR_BG_BOTTOM[1] * ratio)
            b = int(COLOR_BG_TOP[2] * (1-ratio) + COLOR_BG_BOTTOM[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.rect.width, y))

    def update(self):
            AiManager.manage_block_ai(self)
            # Mouvement
            for b in self.blocks:
                b.move(self.rect, True if not self.start_wall else False)
                b.update_visuals()

            # On gère les collisions avec les murs
            for b in self.blocks:
                for w in self.walls:
                    b.collide_with_wall(w)

            # Interactions entre blocs
            self.handle_interactions()

    def draw(self):
        self.draw_background()
        for w in self.walls:
            w.draw(self.screen)
                
        for b in self.blocks:
            b.draw(self.screen)
        pygame.display.flip()