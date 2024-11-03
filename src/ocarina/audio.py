import pygame


class Audio:
    def __init__(self, audio_path):
        # self.starting = pygame.mixer.Sound(f"{audio_path}_start.wav")
        self.playing = pygame.mixer.Sound(f"{audio_path}_loop.wav")
        # self.stopping = pygame.mixer.Sound(f"{audio_path}_end.wav")

    def play(self):
        self.playing.play(-1)

    def stop(self):
        self.playing.stop()