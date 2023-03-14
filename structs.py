
class timevalue:
	notes: int
	value: int

	def __init__(self, notes: int = 0, value: int = 4) -> None:
		self.notes = notes
		self.value = value

	def common_time():
		return timevalue(4, 4)
	def waltz_time():
		return timevalue(3, 4)
	def six_eight():
		return timevalue(6, 8)
	
	def one_fourth():
		return timevalue(1, 4)
	def one_eighth():
		return timevalue(1, 8)
	def one_sixteenth():
		return timevalue(1, 16)

	def fraction(self) -> float:
		return self.notes / self.value

	def increase(self):
		self.notes += 1
		return self
	def decrease(self):
		self.notes -= 1
		return self
#END

class note:
	fret: int
	string: int

	beginning: timevalue
	duration:  timevalue | None

	# staccato: bool = False

	# def end(self):
	# 	if self.duration is None:
	# 		return None
	# 	else:
	# 		return self.duration.fraction()

	def __init__(self, fret, string, beginning, duration = None) -> None:
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

	meter: timevalue | None		# the time signature
	metronome:   int | None		# the number of 4th notes per minute

	def __init__(self, title: str = None, meter: timevalue = None, metronome: int = None, notes: list[note] = []) -> None:
		self.notes = notes
		
		self.title = title
		
		self.meter = meter
		self.metronome = metronome
#END

class song:
	title:   str
	author: str

	tuning: list[int]

	measures: list[measure]

	def __init__(self, name: str, author: str, tuning: list[int], measures: list[measure]) -> None:
		self.title, self.author, self.tuning, self.measures = name, author, tuning, measures
#END
