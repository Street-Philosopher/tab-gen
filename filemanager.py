
import os
from structs import song, note, timevalue
from constants import BASS_STANDARD_TUNE_4


_RECENT_FILES_PATH = "./.recent"

TAB_FILE_VERSION = 0x00
MAGIC_NUMBER = "TAB"

HEADER_END_OFFSET = SONG_NAME_START_OFFSET = 0x20
SONG_NAME_MAX_LENGTH = 0x40
SONG_NAME_END_OFFSET = SONG_AUTH_START_OFFSET = 0x60
SONG_AUTH_MAX_LENGTH = 0x40
SONG_AUTH_END_OFFSET = SONG_TUNING_START_OFFSET = 0xA0

MEASURE_LIST_HEADER_END = 0xC0

MAX_STRINGS_FOR_TUNE = 0x0F
SONG_TUNING_END_OFFSET = 0xB0

MEASURE_ENTRY_SIZE = 0x30
MEASURE_TITLE_MAX_LENGTH = 0x20

NOTE_LIST_HEADER_SIZE = 0x10
NOTE_LIST_ENTRY_SIZE = 0x10


def DecodeSongFile(path: str) -> song:
	pass
# TODO: exception handling for custom errors
def EncodeSongToFile(song: song, path: str) -> bool | Exception:
	try:
		# chooses the temp file name. this is bad but it ensures we don't overwrite something that already exists
		temp_file_path = path + ".temp"
		while os.path.isfile(temp_file_path):
			temp_file_path = temp_file_path + ".temp"
		
		# we write all the stuff to a temp file, to not overwrite any file with the given name if it exists and the process ends up erroring out
		with open(temp_file_path, "wb") as file:
			# header
			file.write(_StrToBytes(MAGIC_NUMBER))
			file.write(_IntToSingleByte(TAB_FILE_VERSION))
			_ZeroPadToOffset(file, HEADER_END_OFFSET)

			# song title
			if len(song.title) > SONG_NAME_MAX_LENGTH:
				raise ValueError(f"The song's title is too long (max: {SONG_NAME_MAX_LENGTH} characters)")
			file.write(_StrToBytes(song.title))
			_ZeroPadToOffset(file, SONG_NAME_END_OFFSET)

			# song author
			if len(song.author) > SONG_AUTH_MAX_LENGTH:
				raise ValueError(f"The song's author name is too long (max: {SONG_AUTH_MAX_LENGTH} characters)")
			file.write(_StrToBytes(song.author))
			_ZeroPadToOffset(file, SONG_AUTH_END_OFFSET)

			# tuning
			if len(song.tuning) > MAX_STRINGS_FOR_TUNE:
				raise ValueError(f"Too many strings in the bass tuning (max: {MAX_STRINGS_FOR_TUNE} strings)")
			file.write(_IntToSingleByte(len(song.tuning)))
			for string_tune in song.tuning:
				file.write(string_tune.to_bytes(length=1, byteorder="big", signed=True))		#this has to be signed, because it could be tuned negative relative to central Do
			_ZeroPadToOffset(file, SONG_TUNING_END_OFFSET)

			# measures
			file.write(len(song.measures).to_bytes(length=2, byteorder="big"))
			_ZeroPadToOffset(file, MEASURE_LIST_HEADER_END)

			from structs import measure		# for some reason i have to import here otherwise vscode gets mad
			# in the form of: (address, measure)
			note_list_dependencies: list[tuple[int, measure]] = []

			for measure_e in song.measures:
				measure_end_offset = file.tell() + MEASURE_ENTRY_SIZE

				# write measure title
				measure_title_end_offset = file.tell() + MEASURE_TITLE_MAX_LENGTH
				if len(measure_e.title) > MEASURE_TITLE_MAX_LENGTH:
					raise ValueError(f"The measure's title is too long (max: {MEASURE_TITLE_MAX_LENGTH} characters)")
				file.write(_StrToBytes(measure_e.title))
				_ZeroPadToOffset(file, measure_title_end_offset)

				# write metronome change
				if measure_e.metronome is None:
					_ZeroPadBy(file, 1)
				else:
					file.write(_IntToSingleByte(measure_e.metronome))
				
				# write timesig change
				file.write(_TimeSigToBytes(measure_e.meter))

				# address pointing to the list of notes. will be written later
				note_list_dependencies.append( (file.tell(), measure_e) )
				_ZeroPadBy(file, 4)

				# end with some zero-padding
				_ZeroPadToOffset(file, measure_end_offset)
				del measure_e
			#END

			for entry in note_list_dependencies:
				address_e = entry[0]
				measure_e = entry[1]

				# write the address we left unwritten before
				note_list_start_addr = file.tell()
				file.seek(address_e)
				file.write(note_list_start_addr.to_bytes(length=4, byteorder="big"))
				file.seek(note_list_start_addr)

				# list header
				file.write(_IntToSingleByte(len(measure_e.notes)))
				_ZeroPadToOffset(file, (note_list_start_addr + NOTE_LIST_HEADER_SIZE))

				# add the actual notes
				for note in measure_e.notes:
					note_entry_start_addr = file.tell()

					# string and fret
					file.write(_IntToSingleByte(note.string))
					file.write(_IntToSingleByte(note.fret))

					# beginning and duration
					file.write(_TimeSigToBytes(note.beginning))
					file.write(_TimeSigToBytes(note.duration))

					_ZeroPadToOffset(file, (note_entry_start_addr + NOTE_LIST_ENTRY_SIZE))
			#END
	except Exception as e:
		# an error happened. remove the file
		os.remove(temp_file_path)

		return e
	else:
		# replace the previous file (if any) with the new one
		if os.path.isfile(path):
			os.remove(path)
		os.rename(src=temp_file_path, dst=path)

		return True
#END
def _IntToSingleByte(num: int) -> bytes:
	return num.to_bytes(length=1, byteorder="big", signed=False)
def _StrToBytes(string: str) -> bytes:
	return bytes(string, encoding="utf-8")
def _ZeroPadToOffset(file, to_offset: int):
	file.write(bytes(
		"\0" * (to_offset - file.tell()),
		encoding="utf-8"
	))
def _ZeroPadBy(file, number: int):
	file.write(bytes(
		"\0" * number,
		encoding="utf-8"
	))
def _TimeSigToBytes(timesig: timevalue) -> bytes:
	if timesig is None:
		return _StrToBytes("\0\0")
	else:
		return (_IntToSingleByte(timesig.notes) + _IntToSingleByte(timesig.value))
#END


def AddToRecentFiles(path: str):
	allfiles = GetRecentFiles()
	path = os.path.abspath(path)

	while len(allfiles) > 10:
		allfiles.pop()

	if path not in allfiles:
		if len(allfiles) == 10:
			allfiles.pop()
		allfiles.insert(0, path)
	else:
		newfilelist = []
		newfilelist.append(path)
		for file in allfiles:
			if file != path:
				newfilelist.append(file)
		allfiles = newfilelist
	
	with open(_RECENT_FILES_PATH, "w") as f:
		f.write("\n".join(allfiles))
#END
		
def GetRecentFiles() -> list[str]:
	if os.path.isfile(_RECENT_FILES_PATH):
		with open(_RECENT_FILES_PATH) as f:
			raw = f.read(-1)
		items = raw.split("\n")
		return items
	else:
		return []


from testsongs import bonjovi
raise EncodeSongToFile(bonjovi, "./songs/livinonaprayer.tab")
