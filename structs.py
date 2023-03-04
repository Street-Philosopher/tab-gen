
class timevalue:
	notes: int
	value: int

	def __init__(self, notes, value) -> None:
		self.notes = notes
		self.value = value
#END

class note:
	fret: int
	string: int

	beginning: timevalue
	duration:  timevalue | None

	# staccato: bool = False

	def __init__(self, fret, string, beginning, duration=None) -> None:
		# if fret < 0:
		# 	raise ValueError("can't play a fret below empty string")
		# if string < 0:
		# 	raise ValueError("inappropriate string value")

		self.fret = fret
		self.string = string
		self.duration = duration
		self.beginning = beginning
#END

class measure:
	notes: list[note]
	
	title: str | None

	meter: timevalue | None
	metronome:   int | None

	def __init__(self, title = None, meter = None, metronome = None) -> None:
		self.notes = []
		
		self.title = title
		
		self.meter = meter
		self.metronome = metronome
#END

class song:
	name:   str
	author: str

	tuning: list[int]

	measures: list[measure]
#END
