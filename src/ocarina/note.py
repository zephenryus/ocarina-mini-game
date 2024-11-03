from src.ocarina.audio import Audio
from src.ocarina.note_state import NoteState


class Note:
    def __init__(self, name, audio_path, state=NoteState.NOT_PLAYING):
        self.name = name
        self._audio = Audio(audio_path)
        self.state = state

    def play(self):
        self._audio.play()

    def stop(self):
        self._audio.stop()