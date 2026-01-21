import pygame
import random
from constants import ELEMENT_RULES, MAX_FORCE, MAX_SPEED
from core.ContaminationWave import ContaminationWave
from core.managers.ResourceManager import ResourceManager
from core.Wall import Wall

class Block:
    def __init__(self, x, y, size, element_type):
        # Utilisation de Vector2 pour la position et la vélocité
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0) # On commence à l'arrêt
        self.acc = pygame.Vector2(0, 0) # Accélération (force cumulée)
        self.key = (0, 0)  # Clé de la grille spatiale

        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.type = element_type
        self.image = pygame.transform.smoothscale(ResourceManager.get_img(element_type), (size, size))
        self.color = ELEMENT_RULES[element_type]["color"]
        self.waves = []
        self.contamination_radius = 50

    def apply_force(self, force: pygame.Vector2):
        self.acc += force

    def seek(self, target_pos: pygame.Vector2):
        """Calcule une force vers une cible"""
        desired = (target_pos - self.pos)
        if desired.length() > 0:
            desired = desired.normalize() * MAX_SPEED
            steer = desired - self.vel
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
            return steer
        return pygame.Vector2(0, 0)

    def flee(self, predator_pos: pygame.Vector2):
        """Calcule une force à l'opposé d'un prédateur"""
        return -self.seek(predator_pos)

    def move(self, screen_rect, black_block = False):
        if black_block==False and self.type == "black":
            return  # Le bloc noir ne bouge pas
        
        # Application de l'accélération
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        
        self.pos += self.vel
        self.acc *= 0 # Réinitialise l'accélération à chaque frame
        # Synchronisation du rect avant les tests
        self.rect.topleft = (self.pos.x, self.pos.y)

        # Bords Gauche / Droite
        if self.rect.left < 0:
            self.pos.x = 0
            self.vel.x *= -1
        elif self.rect.right > screen_rect.width:
            self.pos.x = screen_rect.width - self.rect.width # On utilise la largeur réelle du rect
            self.vel.x *= -1

        # Bords Haut / Bas
        if self.rect.top < 0:
            self.pos.y = 0
            self.vel.y *= -1
        elif self.rect.bottom > screen_rect.height:
            # Correction ici : on s'assure que le bas du rect touche exactement le bord
            self.pos.y = screen_rect.height - self.rect.height
            self.vel.y *= -1

        # Mise à jour finale pour le dessin
        self.rect.topleft = (self.pos.x, self.pos.y)
    
    # collision avec un autre bloc
    def resolve_collision(self, other: "Block"):
        """Calcule la force de collision entre deux blocs"""
        if self.rect.colliderect(other.rect):
            # Calcul de l'overlap (votre logique d'origine)
            dx = self.rect.centerx - other.rect.centerx
            dy = self.rect.centery - other.rect.centery
            overlap_x = (self.size / 2 + other.size / 2) - abs(dx)
            overlap_y = (self.size / 2 + other.size / 2) - abs(dy)

            # Définir la normale de collision (direction de la force)
            if overlap_x < overlap_y:
                normal = pygame.Vector2(1 if dx > 0 else -1, 0)
                separation = overlap_x
            else:
                normal = pygame.Vector2(0, 1 if dy > 0 else -1)
                separation = overlap_y

            if other.type == "otherType":
                # Le bloc noir ne bouge pas : on repousse 'self' de TOUTE la distance
                self.pos += normal * separation
                # On reflète la vélocité par rapport à la normale pour un rebond parfait
                self.vel = self.vel.reflect(normal)
            elif self.type == "otherType":
                # Cas inverse (peu probable si black est immobile, mais utile pour la solidité)
                other.pos -= normal * separation
                other.vel = other.vel.reflect(normal)
            else:
                # Collision normale entre deux blocs mobiles : on partage la séparation
                self.pos += normal * (separation / 2)
                other.pos -= normal * (separation / 2)

                # Correction de position (Anti-glitch : on sépare les blocs)
                self.pos += normal * (separation / 2)
                other.pos -= normal * (separation / 2)

                # Calcul du rebond vectoriel (Elastic Collision)
                # On projette la vélocité relative sur la normale
                relative_velocity = self.vel - other.vel
                velocity_along_normal = relative_velocity.dot(normal)

                # Si les blocs s'éloignent déjà, on ne fait rien
                if velocity_along_normal > 0:
                    return False

                # On applique l'impulsion (force de rebond)
                # Pour des masses égales, on échange simplement les composantes le long de la normale
                impulse = normal * velocity_along_normal
                self.vel -= impulse
                other.vel += impulse
            
            return True
        return False

    def collide_with_wall(self, wall: Wall):
        """Logique d'overlap corrigée pour murs longs/fins"""
        if self.rect.colliderect(wall.rect):
            # Calcul des distances entre les centres
            dx = self.rect.centerx - wall.rect.centerx
            dy = self.rect.centery - wall.rect.centery
            
            # Calcul des chevauchements réels
            overlap_x = (self.rect.width / 2 + wall.rect.width / 2) - abs(dx)
            overlap_y = (self.rect.height / 2 + wall.rect.height / 2) - abs(dy)

            # On compare quel axe est le plus "petit" pour déterminer la face d'impact
            # Si le mur est horizontal (très large), overlap_y sera le plus petit sur les faces haut/bas
            if overlap_x < overlap_y:
                # Collision Latérale (Gauche ou Droite du mur)
                self.pos.x += overlap_x if dx > 0 else -overlap_x
                self.vel.x *= -1
            else:
                # Collision Verticale (Haut ou Bas du mur)
                self.pos.y += overlap_y if dy > 0 else -overlap_y
                self.vel.y *= -1
            
            # Application immédiate de la correction de position
            self.rect.topleft = (self.pos.x, self.pos.y)

    def collide_with_block(self, other):
        """Logique d'overlap pour les blocs"""
        if self.rect.colliderect(other.rect):
            dx = self.rect.centerx - other.rect.centerx
            dy = self.rect.centery - other.rect.centery
            overlap_x = (self.rect.width / 2 + other.rect.width / 2) - abs(dx)
            overlap_y = (self.rect.height / 2 + other.rect.height / 2) - abs(dy)

            # Pour éviter que les blocs restent collés, on les sépare tous les deux
            if overlap_x < overlap_y:
                separation = overlap_x / 2
                self.pos[0] += separation if dx > 0 else -separation
                other.pos[0] -= separation if dx > 0 else -separation
                self.velocity[0], other.velocity[0] = -self.velocity[0], -other.velocity[0]
            else:
                separation = overlap_y / 2
                self.pos[1] += separation if dy > 0 else -separation
                other.pos[1] -= separation if dy > 0 else -separation
                self.velocity[1], other.velocity[1] = -self.velocity[1], -other.velocity[1]
            
            self.rect.topleft = self.pos
            other.rect.topleft = other.pos
            return True
        return False

    def change_type(self, new_type):
        if self.type != new_type:
            self.type = new_type
            self.image = pygame.transform.smoothscale(ResourceManager.get_img(new_type), (self.size, self.size))
            self.color = ELEMENT_RULES[new_type]["color"]
            ResourceManager.play_sound(new_type)

    def emit_wave(self):
        """Crée une nouvelle onde au centre du bloc"""
        if self.type == "black" and len(self.waves) < 3: # Max 3 ondes simultanées
            self.waves.append(ContaminationWave(self.rect.centerx, self.rect.centery, self.contamination_radius))

    def update_visuals(self):
        """Met à jour toutes les ondes actives"""
        for w in self.waves[:]:
            if not w.update():
                self.waves.remove(w)

    def draw(self, screen):
        for w in self.waves:
            w.draw(screen)
        
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)