
from constants import BASS_STANDARD_TUNE_4
from structs import *

riff = measure(metronome=120, meter=timevalue.common_time())
riff.notes = [
    note(fret=0, string=1, beginning=timevalue(0, 8)),
    note(fret=7, string=2, beginning=timevalue(1, 8)),
    note(fret=7, string=1, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=0, string=1, beginning=timevalue(4, 8)),
    note(fret=0, string=1, beginning=timevalue(5, 8)),
    note(fret=7, string=1, beginning=timevalue(6, 8)),
    note(fret=5, string=2, beginning=timevalue(7, 8)),
]
variation = measure(metronome=120, meter=timevalue.common_time())
variation.notes = [
    note(fret=0, string=1, beginning=timevalue(0, 8)),
    note(fret=7, string=2, beginning=timevalue(1, 8)),
    note(fret=7, string=1, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=5, string=3, beginning=timevalue(4, 8)),
    note(fret=4, string=3, beginning=timevalue(5, 8)),
    note(fret=5, string=3, beginning=timevalue(6, 8)),
    note(fret=4, string=3, beginning=timevalue(7, 8)),
]

print(list(note.string for note in riff.notes))

bonjovi = song (
    measures = [ riff, variation ],
    name = "Livin' On A Prayer",
    author = "Bon Jovi",
    tuning = BASS_STANDARD_TUNE_4
)

notes1 = [note(fret=0, string=1, beginning=timevalue(i, 8)) for i in range(8)]
eighth = song(
    name="",
    author="",
    tuning=BASS_STANDARD_TUNE_4,
    measures = [ measure(metronome=120, meter=timevalue.common_time(), notes=notes1) for i in range(4) ]
)
notes2 = [note(fret=0, string=1, beginning=timevalue(i, 16)) for i in range(16)]
sixteenth = song(
    name="",
    author="",
    tuning=BASS_STANDARD_TUNE_4,
    measures = [ measure(metronome=120, meter=timevalue.common_time(), notes=notes2) for i in range(4) ]
)
