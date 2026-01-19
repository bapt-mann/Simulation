import pygame

# Configuration Écran
SCREEN_WIDTH, SCREEN_HEIGHT = 540, 960
FPS = 60
CHUNK_SIZE = 80

# Couleurs (Thème sombre)
COLOR_BG_TOP = (30, 30, 40)
COLOR_BG_BOTTOM = (60, 60, 80)

# Types et Règles
# Format : TYPE: {"color": (R, G, B), "beats": TYPE_QUI_PERD}
ELEMENT_RULES = {
    "red":  {"color": (255, 50, 50), "beats": "green"},
    "green": {"color": (50, 255, 50), "beats": "blue"},
    "blue": {"color": (50, 50, 255), "beats": "red"},
    "black": {"color": (20, 20, 20), "beats": None}  # Bloc noir neutre
}