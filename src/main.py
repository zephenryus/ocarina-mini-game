import platform
import sys

import pygame
from gpiozero import Button

from src.ocarina.note import Note
from src.ocarina.notes import Notes
from src.ocarina.sequence_manager import SequenceManager
from src.ocarina.song import Song


def is_raspberry_pi():
    return platform.system() == "Linux" and (
                "raspberrypi" in platform.uname().release or "rpi" in platform.uname().release)

def post_keydown_event(key):
    pygame_event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
    pygame.event.post(pygame_event)

def post_keyup_event(key):
    pygame_event = pygame.event.Event(pygame.KEYUP, {'key': key})
    pygame.event.post(pygame_event)


def on_press(button_states, button, key):
    if not button_states[button]:  # Only post if the button wasn't already pressed
        post_keydown_event(key)
        button_states[button] = True  # Update state to pressed

# Function to handle button release with state tracking
def on_release(button_states, button, key):
    if button_states[button]:  # Only post if the button was pressed
        post_keyup_event(key)
        button_states[button] = False  # Update state to released


def main():
    pygame.init()

    if is_raspberry_pi():
        button_d2 = Button(17)
        button_a = Button(5)
        button_b = Button(27)
        button_f = Button(22)
        button_d = Button(6)

        button_states = {
            "button_d2": False,
            "button_a": False,
            "button_b": False,
            "button_f": False,
            "button_d": False,
        }

        button_d2.when_pressed = lambda: on_press(button_states, "button_d2", pygame.K_UP)
        button_d2.when_released = lambda: on_release(button_states, "button_d2", pygame.K_UP)
        button_a.when_pressed = lambda: on_press(button_states, "button_a", pygame.K_LEFT)
        button_a.when_released = lambda: on_release(button_states, "button_a", pygame.K_LEFT)
        button_b.when_pressed = lambda: on_press(button_states, "button_b", pygame.K_LEFT)
        button_b.when_released = lambda: on_release(button_states, "button_b", pygame.K_LEFT)
        button_f.when_pressed = lambda: on_press(button_states, "button_f", pygame.K_DOWN)
        button_f.when_released = lambda: on_release(button_states, "button_f", pygame.K_DOWN)
        button_d.when_pressed = lambda: on_press(button_states, "button_d", pygame.K_a)
        button_d.when_released = lambda: on_release(button_states, "button_d", pygame.K_a)

    note_d2 = Note(Notes.D2, "assets/audio/OOT_Notes_Ocarina_D2")
    note_a = Note(Notes.A, "assets/audio/OOT_Notes_Ocarina_A")
    note_b = Note(Notes.B, "assets/audio/OOT_Notes_Ocarina_B")
    note_f = Note(Notes.F, "assets/audio/OOT_Notes_Ocarina_F")
    note_d = Note(Notes.D, "assets/audio/OOT_Notes_Ocarina_D")

    songs = [
        Song(
            "Zelda's Lullaby",
            [Notes.D, Notes.D, Notes.D],
            "assets/songs/Zeldas Lullaby.mp3"
        ),
        Song(
            "Zelda's Lullaby2",
            [Notes.F, Notes.F, Notes.F],
            "assets/songs/Zeldas Lullaby.mp3"
        ),
    ]
    sequence_manager = SequenceManager()

    screen = pygame.display.set_mode((800, 600))

    running = True
    current_song = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                if not current_song:
                    if event.key == pygame.K_UP:
                        note_d2.play()
                        sequence_manager.add_note(Notes.D2)
                    elif event.key == pygame.K_RIGHT:
                        note_a.play()
                        sequence_manager.add_note(Notes.A)
                    elif event.key == pygame.K_LEFT:
                        note_b.play()
                        sequence_manager.add_note(Notes.B)
                    elif event.key == pygame.K_DOWN:
                        note_f.play()
                        sequence_manager.add_note(Notes.F)
                    elif event.key == pygame.K_a:
                        note_d.play()
                        sequence_manager.add_note(Notes.D)

                    for song in songs:
                        if sequence_manager.check(song.sequence):
                            print(f"Matched {song.name}")
                            song.play()
                            current_song = song

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    note_d2.stop()
                if event.key == pygame.K_RIGHT:
                    note_a.stop()
                if event.key == pygame.K_LEFT:
                    note_b.stop()
                if event.key == pygame.K_DOWN:
                    note_f.stop()
                if event.key == pygame.K_a:
                    note_d.stop()

        if current_song:
            current_song.update()
            if not current_song.playing():
                current_song = None

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()