
from time import sleep
from time import time as currenttime

from pysinewave import SineWave

from structs import song, note, measure, timevalue
from constants import get_note

# each note will be played with a precision in the 64th. this means 128th notes for example won't be played
TIMEKEEPER_BEAT_PRECISION = 64
NOTE_FADEOUT_RATE = 10
NOTE_START_VOLUME = -20
NOTE_TARGT_VOLUME = -100

class music_player:
	timesig: timevalue
	metronomeval: int

	tuning: list[int]

	# id of the note with null duration being played
	note_null_duration_id = None	# it's outside of the loop because if a null duration note lasts more than a measure it could be a problem

	# dict of all wave objects created
	waves_objects = {}
	# list of all note IDs of the notes being currently played
	notes_being_played = []

	def __init__(self, metronome, timesig, tuning) -> None:
		self.metronomeval = metronome
		self.timesig = timesig
		self.tuning = tuning

	def measureloop(self, notes: dict[int, note]):
		"""
		loop that lasts one measure, according to the measure's info

		it plays the notes and stops them, removing them from the list once they're done

		returns when the measure is done playing
		"""
		# `notes` is the argument of the function. it contains all the `note` objects by their note ID, as defined in the PlaySong loop. it's only used when creating the wave objects
		# `self.waves_objects` is the dictionary (by note ID) containing all the SineWave objects to be played, their beginning (as a `timevalue`) and their end (`timevalue` or `None`). it's a class member to allow waves to be played and stopped in different measures. its items are defined at the beginning of the `measureloop`, and used in the for loop
		# `self.notes_being_played` is the list of note IDs of the notes being currently played. it's a class member for the same reason as `self.scheduled_waves`. items are appended and removed in the main loop like `self.scheduled_waves`
		# `scheduled_to_remove` is the list of note IDs of notes that have just ended being played, and that will be removed at the end of the iteration

		# `self.note_null_duration_id` allows notes to not have a duration: a note with a `None` duration will be stopped as soon as another note is played, thus only one can exist at a time. this variable contains its ID (or None) to allow the player to stop it and remove it as soon as another note gets played, regardless of the current measure

		# `measure_duration` is the total duration in seconds this measure is going to last
		# `iterations` is the number of iterations the measureloop is going to make to play all notes in time. this is because the loop is discrete (TODO: make a continuous system possibly?)
		# `time_per_iter` is the time that needs to pass between each iteration
		# `current_time_cycle` is the counter that holds the current time that has passed since the beginning of the measure

		# to get the duration of the measure in seconds we convert the metronome from bpm to bps and then multiply it by the differing duration of the measure given by its meter
		measure_duration = 4 * (60 / self.metronomeval) * self.timesig.fraction()
		# it just works ok?

		# number of notes in the current time signature when converted to 64ths
		iterations = int(TIMEKEEPER_BEAT_PRECISION / self.timesig.value) * self.timesig.notes	# TODO: this only allows times that are multiples of 2
		# seconds to wait after each iteration
		time_per_iter = measure_duration / iterations

		# counter
		current_time_cycle = 0

		def end_note(wave_id, wave):
			print("ending note:", notes[wave_id].fret, notes[wave_id].string, "(", wave_id, ")")
			wave["object"].stop()
			scheduled_to_remove.append(wave_id)

		# create the waves so we don't have to do it later
		for id in notes:
			# don't create another object
			if id in self.waves_objects:
				continue

			wave = SineWave(
				pitch=get_note(notes[id].fret, notes[id].string, self.tuning),
				
				# make them fade out a little
				decibels_per_second=NOTE_FADEOUT_RATE,
				decibels=NOTE_START_VOLUME,
			)
			self.waves_objects[id] = {
				"object": wave,
				"start":  (notes[id].beginning.fraction() * measure_duration),
				"end":    ((notes[id].beginning.fraction() + notes[id].duration.fraction()) * measure_duration) if notes[id].duration is not None else None
			}
			del id, wave
		#END

		scheduled_to_remove = []

		for i in range(iterations):
			starttime = currenttime()
			
			for wave_id in self.waves_objects:
				# play notes
				wave = self.waves_objects[wave_id]
				if current_time_cycle >= wave["start"] and wave_id not in self.notes_being_played:
					print("playing:", notes[wave_id].fret, notes[wave_id].string, "(", wave_id, ")")
					self.notes_being_played.append(wave_id)

					# if there is a null duration note being played, stop it
					if self.note_null_duration_id is not None:
						end_note(self.note_null_duration_id, self.waves_objects[self.note_null_duration_id])
						self.note_null_duration_id = None
					# if this note is a null duration note set it
					if wave["end"] is None:
						self.note_null_duration_id = wave_id

					# play the wave
					wave["object"].play()
					wave["object"].set_volume(NOTE_TARGT_VOLUME)
				# check for each note being played if we need to stop it
				elif wave["end"] is not None and current_time_cycle >= wave["end"]:
					end_note(wave_id, wave)
			# del(wave, wave_id)

			# remove based on the ID from ALL lists that contain the notes or anything similar
			for wave_id in scheduled_to_remove:
				notes.pop(wave_id)
				self.waves_objects.pop(wave_id)
				self.notes_being_played.remove(wave_id)
				del wave_id
			scheduled_to_remove.clear()

			current_time_cycle += time_per_iter
			sleep(time_per_iter - (currenttime() - starttime))
			del(starttime, i)
		#END

		# for each note that still isn't done, subtract the duration of this beat from its end. this way we can ignore what measure we are in or how much time has passed from the beginning
		for note_id in notes:
			self.waves_objects[note_id]["start"] -= measure_duration
			if self.waves_objects[note_id]["end"] is not None:
				self.waves_objects[note_id]["end"] -= measure_duration
			del note_id
	#END FUNC

	def endsong(self):
		"""stop anything still being played, clean up and stop all sounds"""
		print("doing cleanup")
		for id in self.notes_being_played:
			self.waves_objects[id]["object"].stop()
			self.waves_objects.pop(id)
			self.notes_being_played.remove(id)
			print("removed note with ID:", id)
			del id
		from colorama import Fore
		print(Fore.RED + "not done" + Fore.WHITE)

def PlaySong(song: song):
	player = music_player(song.measures[0].metronome, song.measures[0].meter, song.tuning)

	current_played_notes = {}
	next_note_id = 0

	for measure in song.measures:
		if measure.metronome is not None:
			player.metronomeval = measure.metronome
		if measure.meter is not None:
			player.timesig = measure.meter

		# check all notes, schedule their beginning and end
		for note in measure.notes:
			current_played_notes[next_note_id] = (note)
			next_note_id += 1

		# plays all scheduled notes according to their info, the metronome and the time signature
		print("start one measure")
		player.measureloop(current_played_notes)
		print("end one measure")
	player.endsong()


# w = SineWave(pitch=-12, decibels=-20, decibels_per_second=10)
# w.play()
# w.set_volume(-100)
# sleep(10)

