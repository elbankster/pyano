from pygame import midi
from pymongo import MongoClient
from datetime import datetime
from random import randint

sessionChordCount = 0
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

    print(f"{rootNote} {chordQuality} {chordInversion}")
    return [rootNote, chordQuality, chordInversion]

def buildChordPool():
    rootNotes = []
    chordQualities = []
    chordInversions = []

    includeNaturals = True
    includeSharps = False
    includeFlats = False
    
    includeMajor = True
    includeMinor = False
    includeDiminished = False
    includeAugmented = False
    includeMajor7th = False
    includeMinor7th = False
    includeDominant7th = False
    includeHalfDiminished7th = False

    includeRoot = True
    include1stInversion = True
    include2ndInversion = True
    include3rdInversion = False

    if includeNaturals:
        rootNotes.append("A")
        rootNotes.append("B")
        rootNotes.append("C")
        rootNotes.append("D")
        rootNotes.append("E")
        rootNotes.append("F")
        rootNotes.append("G")

    if includeSharps:
        rootNotes.append("A#")
        rootNotes.append("C#")
        rootNotes.append("D#")
        rootNotes.append("F#")
        rootNotes.append("G#")
        
    if includeFlats:
        rootNotes.append("Ab")
        rootNotes.append("Bb")
        rootNotes.append("Db")
        rootNotes.append("Eb")
        rootNotes.append("Gb")

    if includeMajor:
        chordQualities.append("major")

    if includeMinor:
        chordQualities.append("minor")
    
    if includeDiminished:
        chordQualities.append("diminished")

    if includeAugmented:
        chordQualities.append("augmented")

    if includeDominant7th:
        chordQualities.append("dominant 7th")
    
    if includeMajor7th:
        chordQualities.append("major 7th")

    if includeMinor7th:
        chordQualities.append("minor 7th")

    if includeHalfDiminished7th:
        chordQualities.append("half-diminished 7th")

    if includeRoot:
        chordInversions.append("root")

    if include1stInversion:
        chordInversions.append("1st inversion")

    if include2ndInversion:
        chordInversions.append("2nd inversion")

    if include3rdInversion:
        chordInversions.append("3rd inversion")

    return [rootNotes, chordQualities, chordInversions]

def getSemitonesFromKeysPressed():
    semitones = keysPressed.copy()

    lowestNoteNumber = semitones[0]

    for i in range(len(semitones)):
        semitones[i] -= lowestNoteNumber

    return semitones

def chordCheck(timestamp):
    global startTime, chordToGuess, sessionChordCount, sessionAverageTime

    semitones = getSemitonesFromKeysPressed()

    chordRoot = None
    chordQuality = None
    chordInversion = None

    isQuadrad = False
    isFlat = False

    if "7th" in chordToGuess[1]:
        isQuadrad = True
    
    ## MAJOR CHORD INTERVALS
    if semitones == [0, 4, 7] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "major"
        chordInversion = "root"

    elif semitones == [0, 5, 9] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "major"
        chordInversion = "1st inversion"
    
    elif semitones == [0, 3, 8] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "major"
        chordInversion = "2nd inversion"

    ## MINOR CHORD INTERVALS
    elif semitones == [0, 3, 7] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "minor"
        chordInversion = "root"

    elif semitones == [0, 5, 8] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "minor"
        chordInversion = "1st inversion"
    
    elif semitones == [0, 4, 9] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "minor"
        chordInversion = "2nd inversion"

    ## DIMINISHED CHORD INTERVALS
    elif semitones == [0, 3, 6] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "diminished"
        chordInversion = "root"

    elif semitones == [0, 6, 9] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "diminished"
        chordInversion = "1st inversion"
    
    elif semitones == [0, 3, 9] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "diminished"
        chordInversion = "2nd inversion"

    ## AUGMENTD CHORD INTERVALS
    elif semitones == [0, 4, 8] and isQuadrad == False:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "augmented"
        # every augmented inversion == 0 4 8

    ## MAJOR 7TH CHORD INTERVALS
    elif semitones == [0, 4, 7, 11] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "major 7th"
        chordInversion = "root"

    elif semitones == [0, 3, 7, 8] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[3]]
        chordQuality = "major 7th"
        chordInversion = "1st inversion"

    elif semitones == [0, 4, 5, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "major 7th"
        chordInversion = "2nd inversion"

    elif semitones == [0, 1, 5, 8] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "major 7th"
        chordInversion = "3rd inversion"

    ## MINOR 7TH CHORD INTERVALS
    elif semitones == [0, 3, 7, 10] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "minor 7th"
        chordInversion = "root"

    elif semitones == [0, 4, 7, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[3]]
        chordQuality = "minor 7th"
        chordInversion = "1st inversion"

    elif semitones == [0, 3, 5, 8] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "minor 7th"
        chordInversion = "2nd inversion"

    elif semitones == [0, 2, 5, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "minor 7th"
        chordInversion = "3rd inversion"

    ## DOMINANT SEVENTH CHORD INTERVALS
    elif semitones == [0, 4, 7, 10] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "dominant 7th"
        chordInversion = "root"

    elif semitones == [0, 3, 6, 8] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[3]]
        chordQuality = "dominant 7th"
        chordInversion = "1st inversion"

    elif semitones == [0, 3, 5, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "dominant 7th"
        chordInversion = "2nd inversion"

    elif semitones == [0, 2, 6, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "dominant 7th"
        chordInversion = "3rd inversion"

    ## HALF-DIMINISHED 7TH CHORD INTERVALS
    elif semitones == [0, 3, 6, 10] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[0]]
        chordQuality = "half-diminished 7th"
        chordInversion = "root"

    elif semitones == [0, 3, 7, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[3]]
        chordQuality = "half-diminished 7th"
        chordInversion = "1st inversion"

    elif semitones == [0, 4, 6, 9] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[2]]
        chordQuality = "half-diminished 7th"
        chordInversion = "2nd inversion"

    elif semitones == [0, 2, 5, 8] and isQuadrad == True:
        chordRoot = midiNoteNumberMap[keysPressed[1]]
        chordQuality = "half-diminished 7th"
        chordInversion = "3rd inversion"

    ## DO DIMINISHED 7TH?

    if chordRoot != None:
        
        ## handle flats
        if "b" in chordToGuess[0]:
            isFlat = True

            if chordRoot == "A#":
                chordRoot = "Bb"
            elif chordRoot == "C#":
                chordRoot = "Db"
            elif chordRoot == "D#":
                chordRoot = "Eb"
            elif chordRoot == "F#":
                chordRoot = "Gb"
            elif chordRoot == "G#":
                chordRoot = "Ab"

        if chordRoot == chordToGuess[0] and chordQuality == chordToGuess[1] and chordInversion == chordToGuess[2]:

            # add record to db
            print(f"Correct!")

            sessionChordCount += 1
            sessionAverageTime += round((timestamp - startTime) / 1000.0, 2)

            chordToGuess = getRandomChord()
            startTime = timestamp
        else:
            print(f"You played a {chordRoot} {chordQuality} {chordInversion}. \nTry again!")


def handleNoteOn(value, ts):
    keysPressed.append(value)
    keysPressed.sort()

    if len(keysPressed) >= 3:
        chordCheck(ts)

def handleNoteOff(value):
    keysPressed.remove(value)

def handleEvents(events):

    for x in range(len(events)):
        message = events[x][0][0]
        value = events[x][0][1]
        ts = events[x][1]

        if message == 144:
            handleNoteOn(value, ts)
        elif message == 128:
            handleNoteOff(value)

midi.init()

midiInput = None
defaultId = midi.get_default_input_id()

chordToGuess = getRandomChord()

if defaultId != -1:
    midiInput = midi.Input(device_id=defaultId)
    startime = 0

try:
    while True:
        if midiInput.poll():
            handleEvents(midiInput.read(num_events=16))

except KeyboardInterrupt:
    if sessionChordCount > 0:
        print(f"You played {sessionChordCount} chords this session.")
        print(f"On average, it took you {round(sessionAverageTime / sessionChordCount, 2)} seconds to find the chord after prompted.")
        