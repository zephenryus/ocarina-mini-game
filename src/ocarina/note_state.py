from enum import Enum, auto


class NoteState(Enum):
    NOT_PLAYING = auto()
    STARTING = auto()
    PLAYING = auto()
    STOPPING = auto()