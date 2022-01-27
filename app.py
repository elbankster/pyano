from pygame import midi
from pymongo import MongoClient
from datetime import datetime
from random import randint

sessionChordCount - 0
sessionAverageTime = 0

keysPressed = []
startTime = 0
chordToGuess = []

midiNoteNumberMap = (
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

def getRandomChord():
    chordPool = buildChordPool()

    rootNote = chordPool[0][randint(0,len(chordPool[0])-1)]
    chordQuality = chordPool[1][randint(0,len(chordPool[1])-1)]
    chordInversion = chordPool[2][randint(0,len(chordPool[2])-1)]