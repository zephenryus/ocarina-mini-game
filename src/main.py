import sys

import pygame
from gpiozero import Button

from src.ocarina.note import Note
from src.ocarina.notes import Notes
from src.ocarina.sequence_manager import SequenceManager
from src.ocarina.song import Song


def main():
    pygame.init()

    button_d2 = Button(6)
    button_a = Button(22)
    button_b = Button(5)
    button_f = Button(17)
    button_d = Button(27)

    button_d2.when_pressed = lambda: keypress(pygame.K_UP)
    button_d2.when_released = lambda: keyrelease(pygame.K_UP)
    button_a.when_pressed = lambda: keypress(pygame.K_LEFT)
    button_a.when_released = lambda: keyrelease(pygame.K_LEFT)
    button_b.when_pressed = lambda: keypress(pygame.K_LEFT)
    button_b.when_released = lambda: keyrelease(pygame.K_LEFT)
    button_f.when_pressed = lambda: keypress(pygame.K_DOWN)
    button_f.when_released = lambda: keyrelease(pygame.K_DOWN)
    button_d.when_pressed = lambda: keypress(pygame.K_a)
    button_d.when_released = lambda: keyrelease(pygame.K_a)

    note_d2 = Note(Notes.D2, "assets/audio/OOT_Notes_Ocarina_D2")
    note_a = Note(Notes.A, "assets/audio/OOT_Notes_Ocarina_A")
    note_b = Note(Notes.B, "assets/audio/OOT_Notes_Ocarina_B")
    note_f = Note(Notes.F, "assets/audio/OOT_Notes_Ocarina_F")
    note_d = Note(Notes.D, "assets/audio/OOT_Notes_Ocarina_D")

    songs = [
        Song(
            "Zelda's Lullaby",
            [Notes.A, Notes.D2, Notes.B, Notes.A, Notes.D2, Notes.B],
            "assets/songs/Zeldas Lullaby.mp3"
        )
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


def keypress(key):
    pygame_event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
    pygame.event.post(pygame_event)

def keyrelease(key):
    pygame_event = pygame.event.Event(pygame.KEYUP, {'key': key})
    pygame.event.post(pygame_event)


if __name__ == '__main__':
    main()