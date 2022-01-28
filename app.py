from pygame import midi
from pymongo import MongoClient
from datetime import datetime
from random import randint

cluster = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = cluster["pyano"]
collection = db["stats"]

session_chord_count = 0
session_average_time = 0

keys_pressed = []
start_time = 0
chord_to_guess = []

midi_note_number_map = (
    #0-11
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #12-23
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #24-35
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #36-47
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #48-59
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #60-71
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #72-83
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #84-95
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #96-107
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #108-119
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",

    #120-127
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G"
)


def get_random_chord():

    chord_pool = build_chord_pool()

    root_note = chord_pool[0][randint(0,len(chord_pool[0])-1)]
    chord_quality = chord_pool[1][randint(0,len(chord_pool[1])-1)]
    chord_inversion = chord_pool[2][randint(0,len(chord_pool[2])-1)]

    print(f"{root_note} {chord_quality} {chord_inversion}")
    return [root_note, chord_quality, chord_inversion]


def build_chord_pool():

    root_notes = []
    chord_qualities = []
    chord_inversions = []

    include_naturals = True
    include_sharps = False
    include_flats = False
    
    include_major = True
    include_minor = False
    include_diminished = False
    include_augmented = False
    include_major7th = False
    include_minor7th = False
    include_dominant_7th = False
    include_half_diminished_7th = False

    include_root = True
    include_1st_inversion = True
    include_2nd_inversion = True
    include_3rd_inversion = False

    if include_naturals:
        root_notes.append("A")
        root_notes.append("B")
        root_notes.append("C")
        root_notes.append("D")
        root_notes.append("E")
        root_notes.append("F")
        root_notes.append("G")

    if include_sharps:
        root_notes.append("A#")
        root_notes.append("C#")
        root_notes.append("D#")
        root_notes.append("F#")
        root_notes.append("G#")
        
    if include_flats:
        root_notes.append("Ab")
        root_notes.append("Bb")
        root_notes.append("Db")
        root_notes.append("Eb")
        root_notes.append("Gb")

    if include_major:
        chord_qualities.append("major")

    if include_minor:
        chord_qualities.append("minor")
    
    if include_diminished:
        chord_qualities.append("diminished")

    if include_augmented:
        chord_qualities.append("augmented")

    if include_dominant_7th:
        chord_qualities.append("dominant 7th")
    
    if include_major7th:
        chord_qualities.append("major 7th")

    if include_minor7th:
        chord_qualities.append("minor 7th")

    if include_half_diminished_7th:
        chord_qualities.append("half-diminished 7th")

    if include_root:
        chord_inversions.append("root")

    if include_1st_inversion:
        chord_inversions.append("1st inversion")

    if include_2nd_inversion:
        chord_inversions.append("2nd inversion")

    if include_3rd_inversion:
        chord_inversions.append("3rd inversion")

    return [root_notes, chord_qualities, chord_inversions]


def get_semitones_from_keys_pressed():

    semitones = keys_pressed.copy()

    lowest_note_number = semitones[0]

    for i in range(len(semitones)):
        semitones[i] -= lowest_note_number

    return semitones


def chord_check(timestamp):

    global start_time, chord_to_guess, session_chord_count, session_average_time

    semitones = get_semitones_from_keys_pressed()

    chord_check = None
    chord_quality = None
    chord_inversion = None

    chord_is_quadrad = False
    chord_is_flat = False

    if "7th" in chord_to_guess[1]:
        chord_is_quadrad = True
    
    ## MAJOR CHORD INTERVALS
    if semitones == [0, 4, 7] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "major"
        chord_inversion = "root"

    elif semitones == [0, 5, 9] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "major"
        chord_inversion = "1st inversion"
    
    elif semitones == [0, 3, 8] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "major"
        chord_inversion = "2nd inversion"

    ## MINOR CHORD INTERVALS
    elif semitones == [0, 3, 7] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "minor"
        chord_inversion = "root"

    elif semitones == [0, 5, 8] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "minor"
        chord_inversion = "1st inversion"
    
    elif semitones == [0, 4, 9] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "minor"
        chord_inversion = "2nd inversion"

    ## DIMINISHED CHORD INTERVALS
    elif semitones == [0, 3, 6] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "diminished"
        chord_inversion = "root"

    elif semitones == [0, 6, 9] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "diminished"
        chord_inversion = "1st inversion"
    
    elif semitones == [0, 3, 9] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "diminished"
        chord_inversion = "2nd inversion"

    ## AUGMENTD CHORD INTERVALS
    elif semitones == [0, 4, 8] and chord_is_quadrad == False:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "augmented"
        # every augmented inversion == 0 4 8

    ## MAJOR 7TH CHORD INTERVALS
    elif semitones == [0, 4, 7, 11] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "major 7th"
        chord_inversion = "root"

    elif semitones == [0, 3, 7, 8] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[3]]
        chord_quality = "major 7th"
        chord_inversion = "1st inversion"

    elif semitones == [0, 4, 5, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "major 7th"
        chord_inversion = "2nd inversion"

    elif semitones == [0, 1, 5, 8] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "major 7th"
        chord_inversion = "3rd inversion"

    ## MINOR 7TH CHORD INTERVALS
    elif semitones == [0, 3, 7, 10] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "minor 7th"
        chord_inversion = "root"

    elif semitones == [0, 4, 7, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[3]]
        chord_quality = "minor 7th"
        chord_inversion = "1st inversion"

    elif semitones == [0, 3, 5, 8] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "minor 7th"
        chord_inversion = "2nd inversion"

    elif semitones == [0, 2, 5, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "minor 7th"
        chord_inversion = "3rd inversion"

    ## DOMINANT SEVENTH CHORD INTERVALS
    elif semitones == [0, 4, 7, 10] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "dominant 7th"
        chord_inversion = "root"

    elif semitones == [0, 3, 6, 8] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[3]]
        chord_quality = "dominant 7th"
        chord_inversion = "1st inversion"

    elif semitones == [0, 3, 5, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "dominant 7th"
        chord_inversion = "2nd inversion"

    elif semitones == [0, 2, 6, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "dominant 7th"
        chord_inversion = "3rd inversion"

    ## HALF-DIMINISHED 7TH CHORD INTERVALS
    elif semitones == [0, 3, 6, 10] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[0]]
        chord_quality = "half-diminished 7th"
        chord_inversion = "root"

    elif semitones == [0, 3, 7, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[3]]
        chord_quality = "half-diminished 7th"
        chord_inversion = "1st inversion"

    elif semitones == [0, 4, 6, 9] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[2]]
        chord_quality = "half-diminished 7th"
        chord_inversion = "2nd inversion"

    elif semitones == [0, 2, 5, 8] and chord_is_quadrad == True:
        chord_check = midi_note_number_map[keys_pressed[1]]
        chord_quality = "half-diminished 7th"
        chord_inversion = "3rd inversion"

    ## DO DIMINISHED 7TH?

    if chord_check != None:
        
        # handle flats
        if "b" in chord_to_guess[0]:
            chord_is_flat = True

            if chord_check == "A#":
                chord_check = "Bb"
            elif chord_check == "C#":
                chord_check = "Db"
            elif chord_check == "D#":
                chord_check = "Eb"
            elif chord_check == "F#":
                chord_check = "Gb"
            elif chord_check == "G#":
                chord_check = "Ab"

        if chord_check == chord_to_guess[0] and chord_quality == chord_to_guess[1] and chord_inversion == chord_to_guess[2]:

            # add record to db
            post = {"timestamp": datetime.now(), "username": "bbankster", "chord_check": chord_check, "chord_quality": chord_quality, "chord_inversion": chord_inversion, "time": round((timestamp - start_time) / 1000.0, 2)}
            collection.insert_one(post)
            
            print(f"Correct!")

            session_chord_count += 1
            session_average_time += round((timestamp - start_time) / 1000.0, 2)

            chord_to_guess = get_random_chord()
            start_time = timestamp

        else:

            print(f"You played a {chord_check} {chord_quality} {chord_inversion}. \nTry again!")


def handle_note_on(value, ts):

    keys_pressed.append(value)
    keys_pressed.sort()

    if len(keys_pressed) >= 3:
        chord_check(ts)


def handle_note_off(value):

    keys_pressed.remove(value)


def handle_events(events):

    for x in range(len(events)):
        message = events[x][0][0]
        value = events[x][0][1]
        ts = events[x][1]

        if message == 144:
            handle_note_on(value, ts)
        elif message == 128:
            handle_note_off(value)


def main():
    global chord_to_guess

    midi.init()

    midi_input = None
    default_id = midi.get_default_input_id()

    if default_id != -1:
        midi_input = midi.Input(device_id = default_id)

        chord_to_guess = get_random_chord()

        try:
            while True:
                if midi_input.poll():
                    handle_events(midi_input.read(num_events=16))

        except KeyboardInterrupt:
            if session_chord_count > 0:
                print(f"You played {session_chord_count} chords this session.")
                print(f"On average, it took you {round(session_average_time / session_chord_count, 2)} seconds to find the chord after prompted.")
            

if __name__ == '__main__':

    #session = PracticeSession()
    
    main()