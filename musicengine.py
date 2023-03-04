
from pysinewave import SineWave
from structs import song, note, measure, timevalue

# each note will be played with a precision in the 64th. this means 128th notes for example won't be played
TIMEKEEPER_BEAT_PRECISION = 64

class timekeeper:
	timesig: timevalue
	metronomeval: int

	current_beat: timevalue

	def __init__(self, metronome, timesig) -> None:
		self.metronomeval, self.timesig = metronome, timesig
		self.current_beat = timevalue(0, TIMEKEEPER_BEAT_PRECISION)

	def measureloop(self, notes):
		"""
		loop that lasts one measure, according to the measure's info
		it plays the notes and stops them, removing them from the list once they're done
		returns when the measure is done playing
		"""

def PlaySong(song: song):
	metronome = timekeeper(song.measures[0].metronome, song.measures[0].meter)

	current_played_notes = []

	for measure in song.measures:
		if measure.metronome is not None:
			metronome.metronomeval = measure.metronome
		if measure.meter is not None:
			metronome.timesig = measure.meter

		# check all notes, schedule their beginning and end
		for note in measure.notes:
			pass

		# plays all scheduled notes according to their info, the metronome and the time signature
		timekeeper.measureloop(current_played_notes)
