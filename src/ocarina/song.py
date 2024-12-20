import threading
import time
from enum import Enum, auto

import pygame.mixer


class SongStates(Enum):
    STOPPED = auto()
    STARTING = auto()
    PLAYING = auto()
    PAUSED = auto()
    STOPPING = auto()


class Song:
    def __init__(self, name, sequence=None, audio_path=None):
        self.name = name
        self.sequence = sequence
        self.path = audio_path
        self._state = SongStates.STOPPED
        self._thread = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
        self.change()

    def load(self):
        pygame.mixer.music.load(self.path)

    def play(self):
        if not self.playing():
            self.load()
            self.state = SongStates.STARTING
            pygame.mixer.music.play()
            self.state = SongStates.PLAYING

    def stop(self):
        self.state = SongStates.STOPPING
        pygame.mixer.music.stop()
        self.state = SongStates.STOPPED

    def playing(self):
        return self.state != SongStates.STOPPED

    def update(self):
        if self.playing:
            if not pygame.mixer.music.get_busy():
                self.stop()

    def change(self):
        print(f"Settings {self.name} song state to: {self.state}")
