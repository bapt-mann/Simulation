import pygame
import os

class ResourceManager:
    _images = {}
    _sounds = {}

    @classmethod
    def load(cls, element_types, size):
        base_path = os.path.dirname(__file__)
        print(base_path)
        img_dir = os.path.join(base_path, "../assets", "images")
        snd_dir = os.path.join(base_path, "../assets", "sounds")

        for name in element_types:
            # Chargement Image
            path_img = os.path.join(img_dir, f"{name}.png")
            if os.path.exists(path_img):
                img = pygame.image.load(path_img).convert_alpha()
                cls._images[name] = pygame.transform.smoothscale(img, size)
            
            # Chargement Son
            path_snd = os.path.join(snd_dir, f"{name}_sound.mp3")
            if os.path.exists(path_snd):
                cls._sounds[name] = pygame.mixer.Sound(path_snd)
                cls._sounds[name].set_volume(0.2)

    @classmethod
    def get_img(cls, name): return cls._images.get(name)
    
    @classmethod
    def play_sound(cls, name):
        if name in cls._sounds: cls._sounds[name].play()