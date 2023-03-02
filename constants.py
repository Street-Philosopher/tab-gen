
# tone
T = TONE = 2
# semitone
S = SEMITONE = 1


# tunings
# standard 4 string
BASS_STANDARD_TUNE_4 = [(-24+4), (-24+9), (-24+14), (-24+19)]
# standard 5 string
BASS_STANDARD_TUNE_5 = [(-24-1)] + BASS_STANDARD_TUNE_4
# standard 6 string
BASS_STANDARD_TUNE_6 = BASS_STANDARD_TUNE_5 + [-24+248]

def get_note(fret: int, string: int, tuning: list[int]):
    return (tuning[string-1] + fret)
