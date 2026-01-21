import pygame

# Configuration Écran
# 1920x1080 pour écran plein, 540x960 pour fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 540
FPS = 60
CHUNK_SIZE = 80

MAX_SPEED = 3.5      # Vitesse maximale du bloc
MAX_FORCE = 0.2      # Capacité de virage (plus c'est haut, plus c'est agile)
DETECTION_RADIUS = 150 # Distance à laquelle un bloc repère une proie/un prédateur

# Couleurs (Thème sombre)
COLOR_BG_TOP = (30, 30, 40)
COLOR_BG_BOTTOM = (60, 60, 80)

# Types et Règles
# Format : TYPE: {"color": (R, G, B), "beats": TYPE_QUI_PERD}
ELEMENT_RULES = {
    "red":  {"color": (255, 50, 50), "beats": "green"},
    "green": {"color": (50, 255, 50), "beats": "blue"},
    "blue": {"color": (50, 50, 255), "beats": "red"},
    "black": {"color": (0, 0, 0), "beats": "red", "beats": "green", "beats": "blue"} # bat tout le monde
}