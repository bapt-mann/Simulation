from pydub import AudioSegment
from pydub.utils import which

# Chemins complets vers ffmpeg et ffprobe
AudioSegment.converter = r"C:\ffmpeg\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe   = r"C:\ffmpeg\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffprobe.exe"

# Charger le fichier audio
son = AudioSegment.from_file(r"E:/python/Simulation/simulation/assets/sounds/water_sound.mp3")

# Couper 0.5 secondes (500 ms)
son_coupe = son[500:]

# Sauvegarder le résultat
son_coupe.export("water_sound_better.mp3", format="mp3")
