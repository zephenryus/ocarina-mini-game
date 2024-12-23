import platform
import sys
from time import sleep

import pygame
from gpiozero import Button, LED, OutputDevice

from src.ocarina.note import Note
from src.ocarina.notes import Notes
from src.ocarina.sequence_manager import SequenceManager
from src.ocarina.song import Song


def is_raspberry_pi():
    return platform.system() == "Linux" and (
                "raspberrypi" in platform.uname().release or "rpi" in platform.uname().release)

def post_keydown_event(key):
    print(f"Posting key down: {key}")
    pygame_event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
    pygame.event.post(pygame_event)

def post_keyup_event(key):
    print(f"Posting key up: {key}")
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
    status_led = None
    puzzle_signal = None
    reset_signal = None

    if is_raspberry_pi():
        status_led = LED(6)
        reset_button = Button(5, bounce_time=0.05)
        puzzle_signal = OutputDevice(13)
        reset_signal = OutputDevice(26)
        reset_signal.off()
        button_d2 = Button(24, bounce_time=0.05) # White
        button_a = Button(17, bounce_time=0.05)  # Green
        button_b = Button(23, bounce_time=0.05)  # Yellow
        button_f = Button(27, bounce_time=0.05)  # Red
        button_d = Button(22, bounce_time=0.05)  # Blue

        button_states = {
            "button_d2": False,
            "button_a": False,
            "button_b": False,
            "button_f": False,
            "button_d": False,
        }

        button_d2.when_pressed = lambda: on_press(button_states, "button_d2", pygame.K_UP)
        button_d2.when_released = lambda: on_release(button_states, "button_d2", pygame.K_UP)
        button_a.when_pressed = lambda: on_press(button_states, "button_a", pygame.K_RIGHT)
        button_a.when_released = lambda: on_release(button_states, "button_a", pygame.K_RIGHT)
        button_b.when_pressed = lambda: on_press(button_states, "button_b", pygame.K_LEFT)
        button_b.when_released = lambda: on_release(button_states, "button_b", pygame.K_LEFT)
        button_f.when_pressed = lambda: on_press(button_states, "button_f", pygame.K_DOWN)
        button_f.when_released = lambda: on_release(button_states, "button_f", pygame.K_DOWN)
        button_d.when_pressed = lambda: on_press(button_states, "button_d", pygame.K_a)
        button_d.when_released = lambda: on_release(button_states, "button_d", pygame.K_a)
        reset_button.when_pressed = lambda: post_keydown_event(pygame.K_r)
        reset_button.when_released = lambda: post_keyup_event(pygame.K_r)

    note_d2 = Note(Notes.D2, "src/assets/audio/OOT_Notes_Ocarina_D2")
    note_a = Note(Notes.A, "src/assets/audio/OOT_Notes_Ocarina_A")
    note_b = Note(Notes.B, "src/assets/audio/OOT_Notes_Ocarina_B")
    note_f = Note(Notes.F, "src/assets/audio/OOT_Notes_Ocarina_F")
    note_d = Note(Notes.D, "src/assets/audio/OOT_Notes_Ocarina_D")

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
            [Notes.A, Notes.D2, Notes.B, Notes.A, Notes.D2, Notes.B],
            "src/assets/songs/zeldas-lullaby.mp3"
        ),
        Song(
            "Epona's Song",
            [Notes.A, Notes.B, Notes.D2, Notes.A, Notes.B, Notes.D2],
            "src/assets/songs/eponas-song.mp3"
        ),
        Song(
            "Saria's Song",
            [Notes.B, Notes.A, Notes.F, Notes.B, Notes.A, Notes.F],
            "src/assets/songs/sarias-song.mp3"
        ),
        Song(
            "Sun's Song",
            [Notes.D2, Notes.F, Notes.A, Notes.D2, Notes.F, Notes.A],
            "src/assets/songs/suns-song.mp3"
        ),
        Song(
            "Song of Time",
            [Notes.F, Notes.D, Notes.A, Notes.F, Notes.D, Notes.A],
            "src/assets/songs/song-of-time.mp3"
        ),
        Song(
            "Song of Storms",
            [Notes.D2, Notes.F, Notes.D, Notes.D2, Notes.F, Notes.D],
            "src/assets/songs/song-of-storms.mp3"
        ),
        Song(
            "Minuet of Forest",
            [Notes.A, Notes.B, Notes.A, Notes.B, Notes.D2, Notes.D],
            "src/assets/songs/minuet-of-forest.mp3"
        ),
        Song(
            "Bolero of Fire",
            [Notes.F, Notes.A, Notes.F, Notes.A, Notes.D, Notes.F, Notes.D, Notes.F],
            "src/assets/songs/bolero-of-fire.mp3"
        ),
        Song(
            "Serenade of Water",
            [Notes.B, Notes.A, Notes.A, Notes.F, Notes.D],
            "src/assets/songs/serenade-of-water.mp3"
        ),
        Song(
            "Nocturne of Shadow",
            [Notes.F, Notes.A, Notes.B, Notes.D, Notes.A, Notes.A, Notes.B],
            "src/assets/songs/nocturne-of-shadow.mp3"
        ),
        Song(
            "Requiem of Spirit",
            [Notes.D, Notes.F, Notes.A, Notes.D, Notes.F, Notes.D],
            "src/assets/songs/requiem-of-spirit.mp3"
        ),
        Song(
            "Prelude of Light",
            [Notes.D2, Notes.B, Notes.A, Notes.D2, Notes.A, Notes.D2],
            "src/assets/songs/prelude-of-light.mp3"
        ),
    ]

    screen = pygame.display.set_mode((800, 600))

    current_song, note_playing, running, sequence_manager, puzzle_solved = reset()

    try:
        if is_raspberry_pi():
            status_led.on()
            reset_signal.off()
            puzzle_signal.off()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    if is_raspberry_pi():
                        reset_signal.on()
                        status_led.on()
                    return
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
                        if is_raspberry_pi():
                            puzzle_signal.on()
                    if current_song == songs[5]:
                        print("Song of Storms easter egg")
                    current_song = None
    except KeyboardInterrupt:
        print("Exiting Loop.")

    finally:
        if is_raspberry_pi():
            status_led.off()

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
    while True:
        try:
            main()
        except KeyboardInterrupt:
            exit(0)

