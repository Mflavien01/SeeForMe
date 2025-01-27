import pygame
from pydub import AudioSegment
from pydub.playback import play

class AdvancedSoundPlayer:
    def __init__(self, screen_width):
        pygame.mixer.init()
        self.screen_width = screen_width

    def load_sound(self, sound_file, pitch_factor=1.0):
        # Charger le son avec pydub pour ajuster le pitch
        original_sound = AudioSegment.from_file(sound_file)
        altered_sound = original_sound._spawn(
            original_sound.raw_data, overrides={"frame_rate": int(original_sound.frame_rate * pitch_factor)}
        )
        # Exporter le son avec le nouveau pitch et le charger avec Pygame
        altered_sound.export("temp_pitch.wav", format="wav")
        return pygame.mixer.Sound("temp_pitch.wav")

    def play_sound(self, sound, x_position, volume=1.0):
        # Normaliser la position x entre -1.0 (gauche) et 1.0 (droite)
        x_normalized = (x_position / (self.screen_width / 2)) - 1.0
        left_volume = (1.0 - x_normalized) / 2.0 * volume
        right_volume = (1.0 + x_normalized) / 2.0 * volume

        # Jouer le son sur un canal libre
        channel = sound.play()
        if channel is not None:
            channel.set_volume(left_volume, right_volume)

# Utilisation de la classe pour jouer plusieurs sons avec des paramètres individuels
if __name__ == "__main__":
    # Initialiser AdvancedSoundPlayer
    sound_player = AdvancedSoundPlayer(screen_width=640)

    # Charger des sons avec différentes fréquences
    sound1 = sound_player.load_sound("son/boop.wav", pitch_factor=1.2)  # Pitch augmenté
    sound2 = sound_player.load_sound("son/beep.wav", pitch_factor=0.8)  # Pitch diminué

    # Jouer les sons à des positions et volumes différents
    sound_player.play_sound(sound1, x_position=100, volume=0.8)  # Son 1 à gauche
    pygame.time.delay(100)
    sound_player.play_sound(sound2, x_position=500, volume=1.0)  # Son 2 à droite
    pygame.time.delay(1000)  # Délai pour écouter les sons
