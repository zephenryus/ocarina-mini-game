import platform
import sys
from time import sleep

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
        button_d2 = Button(17, bounce_time=0.05)
        button_a = Button(5, bounce_time=0.05)
        button_b = Button(27, bounce_time=0.05)
        button_f = Button(22, bounce_time=0.05)
        button_d = Button(6, bounce_time=0.05)

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

    notes_map = {
        Notes.D2: note_d2,
        Notes.A: note_a,
        Notes.B: note_b,
        Notes.F: note_f,
        Notes.D: note_d,
    }

    songs = [
        Song(
            "Zelda's Lullaby",
            [Notes.A, Notes.D2, Notes.B, Notes.A, Notes.D2, Notes.A],
            "assets/songs/zeldas-lullaby.mp3"
        ),
        Song(
            "Epona's Song",
            [Notes.A, Notes.B, Notes.D2, Notes.A, Notes.B, Notes.D2],
            "assets/songs/eponas-song.mp3"
        ),
        Song(
            "Saria's Song",
            [Notes.B, Notes.A, Notes.F, Notes.B, Notes.A, Notes.F],
            "assets/songs/sarias-song.mp3"
        ),
        Song(
            "Sun's Song",
            [Notes.D2, Notes.F, Notes.A, Notes.D2, Notes.F, Notes.A],
            "assets/songs/suns-song.mp3"
        ),
        Song(
            "Song of Time",
            [Notes.F, Notes.D, Notes.A, Notes.F, Notes.D, Notes.A],
            "assets/songs/song-of-time.mp3"
        ),
        Song(
            "Song of Storms",
            [Notes.D2, Notes.F, Notes.D, Notes.D2, Notes.F, Notes.D],
            "assets/songs/song-of-storms.mp3"
        ),
        Song(
            "Minuet of Forest",
            [Notes.A, Notes.B, Notes.A, Notes.B, Notes.D2, Notes.D],
            "assets/songs/minuet-of-forest.mp3"
        ),
        Song(
            "Bolero of Fire",
            [Notes.F, Notes.A, Notes.F, Notes.A, Notes.D, Notes.F, Notes.D, Notes.F],
            "assets/songs/bolero-of-fire.mp3"
        ),
        Song(
            "Serenade of Water",
            [Notes.B, Notes.A, Notes.A, Notes.F, Notes.D],
            "assets/songs/serenade-of-water.mp3"
        ),
        Song(
            "Nocturne of Shadow",
            [Notes.F, Notes.A, Notes.B, Notes.D, Notes.A, Notes.A, Notes.B],
            "assets/songs/nocturne-of-shadow.mp3"
        ),
        Song(
            "Requiem of Spirit",
            [Notes.D, Notes.F, Notes.A, Notes.D, Notes.F, Notes.D],
            "assets/songs/requiem-of-spirit.mp3"
        ),
        Song(
            "Prelude of Light",
            [Notes.D2, Notes.B, Notes.A, Notes.D2, Notes.A, Notes.D2],
            "assets/songs/prelude-of-light.mp3"
        ),
    ]

    screen = pygame.display.set_mode((800, 600))

    current_song, note_playing, running, sequence_manager, puzzle_solved = reset()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                current_song, note_playing, running, sequence_manager, puzzle_solved = reset()
            elif event.type == pygame.KEYDOWN and not puzzle_solved:
                if not current_song:
                    # Stop currently playing note if any
                    if note_playing:
                        notes_map[note_playing].stop()
                        note_playing = None

                    # Play the new note
                    if event.key == pygame.K_UP:
                        note_d2.play()
                        sequence_manager.add_note(Notes.D2)
                        note_playing = Notes.D2
                    elif event.key == pygame.K_RIGHT:
                        note_a.play()
                        sequence_manager.add_note(Notes.A)
                        note_playing = Notes.A
                    elif event.key == pygame.K_LEFT:
                        note_b.play()
                        sequence_manager.add_note(Notes.B)
                        note_playing = Notes.B
                    elif event.key == pygame.K_DOWN:
                        note_f.play()
                        sequence_manager.add_note(Notes.F)
                        note_playing = Notes.F
                    elif event.key == pygame.K_a:
                        note_d.play()
                        sequence_manager.add_note(Notes.D)
                        note_playing = Notes.D

                    for song in songs:
                        if sequence_manager.check(song.sequence):
                            print(f"Matched {song.name}")
                            print(f"Playing {song.path}")
                            song.play()
                            current_song = song

            elif event.type == pygame.KEYUP:
                if note_playing:
                    if event.key == pygame.K_UP and note_playing == Notes.D2:
                        note_d2.stop()
                        note_playing = None
                    elif event.key == pygame.K_RIGHT and note_playing == Notes.A:
                        note_a.stop()
                        note_playing = None
                    elif event.key == pygame.K_LEFT and note_playing == Notes.B:
                        note_b.stop()
                        note_playing = None
                    elif event.key == pygame.K_DOWN and note_playing == Notes.F:
                        note_f.stop()
                        note_playing = None
                    elif event.key == pygame.K_a and note_playing == Notes.D:
                        note_d.stop()
                        note_playing = None

        if current_song:
            current_song.update()
            if not current_song.playing():
                if current_song == songs[1]:
                    print("Puzzle Solved!")
                if current_song == songs[5]:
                    print("Song of Storms easter egg")
                current_song = None

    pygame.quit()
    sys.exit()


def reset():
    print("Resetting...")
    sequence_manager = SequenceManager()
    running = True
    current_song = None
    note_playing = None  # Track the currently playing note
    puzzle_solved = False
    print("Reset.")

    return current_song, note_playing, running, sequence_manager, puzzle_solved


if __name__ == '__main__':
    main()

