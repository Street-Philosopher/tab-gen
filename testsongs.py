
from constants import BASS_STANDARD_TUNE_4, BASS_ONE_OCTAVE_UP_4
from structs import *

riff = measure(metronome=120, meter=timevalue.common_time(), title="riff")
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
variation = measure(metronome=None, meter=None, title="variation")
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
bridge_riff = measure(metronome=120, meter=timevalue.common_time(), title="bridge to pre-chorus")
bridge_riff.notes = [
    note(fret=0, string=1, beginning=timevalue(0, 8)),
    note(fret=7, string=2, beginning=timevalue(1, 8)),
    note(fret=7, string=1, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=0, string=1, beginning=timevalue(4, 8)),
    note(fret=2, string=1, beginning=timevalue(5, 8)),
    note(fret=3, string=1, beginning=timevalue(6, 8)),
    note(fret=2, string=2, beginning=timevalue(7, 8)),
]

prechorus_1 = measure(metronome=None, meter=None, title="pre-chorus")
prechorus_1.notes = [
    note(fret=3, string=2, beginning=timevalue(0, 8)),
    note(fret=3, string=2, beginning=timevalue(1, 8)),
    note(fret=3, string=2, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=5, string=2, beginning=timevalue(4, 8)),
    note(fret=5, string=2, beginning=timevalue(5, 8)),
    note(fret=5, string=2, beginning=timevalue(6, 8)),
    note(fret=5, string=2, beginning=timevalue(7, 8)),
]
prechorus_2 = measure(metronome=None, meter=None, title="")
prechorus_2.notes = [
    note(fret=5, string=2, beginning=timevalue(0, 8)),
    note(fret=5, string=2, beginning=timevalue(1, 8)),
    note(fret=5, string=2, beginning=timevalue(2, 8)),
    note(fret=7, string=2, beginning=timevalue(3, 8)),
    note(fret=7, string=2, beginning=timevalue(4, 8)),
    note(fret=7, string=2, beginning=timevalue(5, 8)),
]
prechorus_3 = measure(metronome=None, meter=None, title="")
prechorus_3.notes = [
    note(fret=3, string=2, beginning=timevalue(0, 8)),
    note(fret=3, string=2, beginning=timevalue(1, 8)),
    note(fret=3, string=2, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=5, string=2, beginning=timevalue(4, 8)),
    note(fret=5, string=2, beginning=timevalue(5, 8)),
    note(fret=5, string=2, beginning=timevalue(6, 8)),
    note(fret=0, string=1, beginning=timevalue(7, 8)),
]
prechorus_4 = measure(metronome=None, meter=None, title="")
prechorus_4.notes = [
    note(fret=5, string=2, beginning=timevalue(0, 8)),
    note(fret=7, string=2, beginning=timevalue(1, 8)),
    note(fret=5, string=3, beginning=timevalue(2, 8)),
    note(fret=4, string=3, beginning=timevalue(3, 8)),
    note(fret=7, string=2, beginning=timevalue(4, 8)),
    note(fret=7, string=2, beginning=timevalue(5, 8)),
    note(fret=7, string=2, beginning=timevalue(6, 8)),
]
prechorus_5 = measure(metronome=None, meter=None, title="")
prechorus_5.notes = [
    note(fret=3, string=2, beginning=timevalue(0, 8)),
    note(fret=3, string=2, beginning=timevalue(1, 8)),
    note(fret=3, string=2, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=5, string=2, beginning=timevalue(4, 8)),
    note(fret=5, string=2, beginning=timevalue(5, 8)),
    note(fret=5, string=2, beginning=timevalue(6, 8)),
    note(fret=5, string=2, beginning=timevalue(7, 8)),
]
prechorus_6 = measure(metronome=None, meter=None, title="")
prechorus_6.notes = [
    note(fret=5, string=2, beginning=timevalue(0, 8)),
    note(fret=5, string=2, beginning=timevalue(1, 8)),
    note(fret=5, string=2, beginning=timevalue(2, 8)),
    note(fret=7, string=2, beginning=timevalue(3, 8)),
    note(fret=7, string=2, beginning=timevalue(4, 8)),
    note(fret=5, string=2, beginning=timevalue(5, 8)),
]
prechorus_7 = measure(metronome=120, meter=timevalue.common_time(), title="")
prechorus_7.notes = [
    note(fret=3, string=2, beginning=timevalue(0, 8)),
    note(fret=3, string=1, beginning=timevalue(1, 8)),
    note(fret=5, string=1, beginning=timevalue(2, 8)),
    note(fret=3, string=2, beginning=timevalue(3, 8)),
    note(fret=3, string=1, beginning=timevalue(5, 8)),
    note(fret=5, string=1, beginning=timevalue(6, 8)),
    note(fret=3, string=2, beginning=timevalue(7, 8)),
]
prechorus_8 = measure(metronome=None, meter=None, title="")
prechorus_8.notes = [
    note(fret=5, string=2, beginning=timevalue(0, 16), duration=timevalue(3, 32)),
    note(fret=5, string=2, beginning=timevalue(3, 16), duration=timevalue(3, 32)),
    note(fret=5, string=2, beginning=timevalue(6, 16), duration=timevalue(1, 16)),
    note(fret=5, string=2, beginning=timevalue(8, 16), duration=timevalue(3, 32)),
    note(fret=3, string=2, beginning=timevalue(6, 8)),		#there's supposed to be a slide here
]

variation2 = measure(metronome=None, meter=None, title="variation")
variation2.notes = [
    note(fret=0, string=1, beginning=timevalue(0, 8)),
    note(fret=7, string=2, beginning=timevalue(1, 8)),
    note(fret=7, string=1, beginning=timevalue(2, 8)),
    note(fret=5, string=2, beginning=timevalue(3, 8)),
    note(fret=5, string=3, beginning=timevalue(4, 8)),
    note(fret=4, string=3, beginning=timevalue(5, 8)),
    note(fret=7, string=2, beginning=timevalue(6, 8)),
    note(fret=5, string=2, beginning=timevalue(7, 8)),
]


bonjovi_measures = [riff for i in range(23)] + [variation] + [riff for i in range(7)] + [bridge_riff] + [prechorus_1, prechorus_2, prechorus_3, prechorus_4, prechorus_5, prechorus_6, prechorus_7, prechorus_8]
ggg = song(measures=[prechorus_7, prechorus_8], name="", author="", tuning=BASS_ONE_OCTAVE_UP_4)


bonjovi = song (
    measures = bonjovi_measures,
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


# from musicengine import PlaySong
# PlaySong(ggg)

