from collections import deque


class SequenceManager:
    _current_sequence = None

    def __init__(self, max_length=8):
        self._max_length = max_length
        self._current_sequence = deque(maxlen=self._max_length)

    def add_note(self, note):
        self._current_sequence.append(note)

    def check(self, sequence):
        current_sequence = list(self._current_sequence)[::-1]
        trimmed_sequence = current_sequence[:len(sequence)]

        return sequence == trimmed_sequence
