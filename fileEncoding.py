
import os
from structs import song, note, timevalue, measure
from constants import BASS_STANDARD_TUNE_4
from typing import BinaryIO
from varname import nameof

FILE_BYTE_ORDER = "big"

TAB_FILE_VERSION = 0x00
MAGIC_NUMBER = "TAB"

HEADER_END_OFFSET = SONG_NAME_START_OFFSET = 0x20
SONG_NAME_MAX_LENGTH = 0x40
SONG_NAME_END_OFFSET = SONG_AUTH_START_OFFSET = 0x60
SONG_AUTH_MAX_LENGTH = 0x40
SONG_AUTH_END_OFFSET = SONG_TUNING_START_OFFSET = 0xA0

MAX_STRINGS_FOR_TUNE = 0x0F
SONG_TUNING_END_OFFSET = 0xB0

MEASURE_LIST_HEADER_END = 0xC0

MEASURE_ENTRY_SIZE = 0x30
MEASURE_TITLE_MAX_LENGTH = 0x20

NOTE_LIST_HEADER_SIZE = 0x10
NOTE_LIST_ENTRY_SIZE = 0x10

MAX_SONG_MEASURES = 0xFFFF



class InvalidFile(Exception):
	pass
DEFAULT_INVALID_FILE = InvalidFile("the file is corrupted or unreadable")


# MAIN FUNCTIONS

def DecodeSongFile(path: str) -> song:
	retval = song(None, None, None, None)

	with open(path, "rb") as file:
		# check header
		magic_number_read = _StrFromBytes(file.read(len(MAGIC_NUMBER)))
		print(magic_number_read)
		if magic_number_read != MAGIC_NUMBER:
			raise DEFAULT_INVALID_FILE
		
		FILE_VERSION = _IntFromBytes(file.read(1))
		print(FILE_VERSION)

		file.read(HEADER_END_OFFSET - file.tell())

		function_name = (f"_Decoder_v{FILE_VERSION}({nameof(file)})")
		print("executing:", function_name)

		try:
			retval = eval(function_name)
		except NameError:
			raise InvalidFile("invalid file version")

	return retval

def EncodeSongToFile(song: song, path: str) -> bool | Exception:
	# from time import time
	# starttime = time()
	try:
		# chooses the temp file name. this is bad but it ensures we don't overwrite something that already exists
		temp_file_path = path + ".temp"
		while os.path.isfile(temp_file_path):
			temp_file_path = temp_file_path + ".temp"
		
		# we write all the stuff to a temp file, to not overwrite any file with the given name if it exists and the process ends up erroring out
		with open(temp_file_path, "wb") as file:
			# header
			file.write(_StrToBytes(MAGIC_NUMBER))
			file.write(_IntToBytes(TAB_FILE_VERSION))
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
			if len(song.tuning) == 0:
				raise ValueError("Can't have zero strings for the tuning")
			file.write(_IntToBytes(len(song.tuning)))
			for string_tune in song.tuning:
				file.write(_IntToBytes(string_tune, signed=True))		#this has to be signed, because it could be tuned negative relative to central Do
			_ZeroPadToOffset(file, SONG_TUNING_END_OFFSET)

			# measures
			if len(song.measures) > MAX_SONG_MEASURES:
				raise ValueError(f"The song is too long (max length: {MAX_SONG_MEASURES} measures)")
			file.write(_IntToBytes(len(song.measures), length=2))
			_ZeroPadToOffset(file, MEASURE_LIST_HEADER_END)

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
					file.write(_IntToBytes(measure_e.metronome))
				
				# write timesig change
				file.write(_TimeSigToBytes(measure_e.meter))

				# address pointing to the list of notes. will be written later
				note_list_dependencies.append( (file.tell(), measure_e) )
				_ZeroPadBy(file, 4)		# this is in place of the actual address

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
				file.write(_IntToBytes(note_list_start_addr, length=4))
				file.seek(note_list_start_addr)

				# list header
				file.write(_IntToBytes(len(measure_e.notes)))
				_ZeroPadToOffset(file, (note_list_start_addr + NOTE_LIST_HEADER_SIZE))

				# add the actual notes
				for note in measure_e.notes:
					note_entry_start_addr = file.tell()

					# string and fret
					file.write(_IntToBytes(note.string))
					file.write(_IntToBytes(note.fret))

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
	finally:
		# endtime = time() - starttime
		# print(endtime)
		pass
#END

# UTILITIES

def _IntToBytes(num: int, length: int = 1, signed: bool = False) -> bytes:
	return num.to_bytes(length=length, byteorder=FILE_BYTE_ORDER, signed=signed)
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
		return (_IntToBytes(timesig.notes) + _IntToBytes(timesig.value))
def _IntFromBytes(bytes: bytes, signed: bool = False):
	return int.from_bytes(bytes=bytes, byteorder=FILE_BYTE_ORDER, signed=signed)
def _StrFromBytes(bytes: bytes):
	return (bytes.decode("utf-8")).replace("\0", "")
def _TimeSigFromBytes(bytes: bytes) -> timevalue:
	notes = (bytes[0])
	value = (bytes[1])
	if value == notes == 0:
		return None
	else:
		return timevalue(notes, value)

def _ReadPaddingBytes(file, num):
	if num < 0:
		raise ValueError("invalid file reading")
	x = _IntFromBytes(file.read(num))
	# if x != 0:
	# 	raise


# DECODING FUNCTIONS

def _Decoder_v0(file: BinaryIO) -> song | None:
	# basic info
	song_name = _StrFromBytes(file.read(SONG_NAME_MAX_LENGTH))
	song_auth = _StrFromBytes(file.read(SONG_AUTH_MAX_LENGTH))
	print(song_name, "by", song_auth)

	# tuning
	tuning_length = _IntFromBytes(file.read(1))
	if tuning_length > MAX_STRINGS_FOR_TUNE or tuning_length == 0:
		raise DEFAULT_INVALID_FILE
	
	decoded_tuning = []
	for _ in range(tuning_length):
		decoded_tuning.append(_IntFromBytes(file.read(1), signed=True))

	_ReadPaddingBytes(file, (SONG_TUNING_END_OFFSET - file.tell()))
	
	# list of measures
	measure_number = _IntFromBytes(file.read(2))
	_ReadPaddingBytes(file, (MEASURE_LIST_HEADER_END - file.tell()))

	decoded_measures = []

	for _ in range(measure_number):
		measure_entry_start_addr = file.tell()

		title = _StrFromBytes(file.read(MEASURE_TITLE_MAX_LENGTH))

		metronome = _IntFromBytes(file.read(1))

		timesig = _TimeSigFromBytes(file.read(2))

		notes_addr = _IntFromBytes(file.read(4))

		_ReadPaddingBytes(file, (MEASURE_ENTRY_SIZE - (file.tell() - measure_entry_start_addr)))
		next_addr = file.tell()

		# get notes
		notes = []
		file.seek(notes_addr)

		note_list_len = _IntFromBytes(file.read(1))
		_ReadPaddingBytes(file, (NOTE_LIST_HEADER_SIZE - (file.tell() - notes_addr)))

		for _ in range(note_list_len):
			note_entry_start_addr = file.tell()
			string = _IntFromBytes(file.read(1))
			fret   = _IntFromBytes(file.read(1))
			start  = _TimeSigFromBytes(file.read(2))
			length = _TimeSigFromBytes(file.read(2))

			# how many bytes have we read in this note entry?
			note_entry_read_bytes = file.tell() - note_entry_start_addr
			_ReadPaddingBytes(file, NOTE_LIST_ENTRY_SIZE - note_entry_read_bytes)
			current_note = note(
				fret=fret,
				string=string,
				beginning=start,
				duration=length,
			)
			notes.append(current_note)
			# del(current_note, read_bytes, length, start, fret, string, start_addr)
		#END

		file.seek(next_addr)

		# create the measure
		tmp = measure(title=title, meter=timesig, metronome=metronome, notes=notes)
		decoded_measures.append(tmp)
	#END

	ret_song = song(
		name=song_name,
		author=song_auth,
		tuning=decoded_tuning,
		measures=decoded_measures,
	)
	return ret_song
#END

	
	
from testsongs import bonjovi
x = EncodeSongToFile(bonjovi, "songs/livinonaprayer.tab")
print(x)
# exit()

# from musicengine import PlaySong

# EncodeSongToFile(bonjovi, "songs/livinonaprayer.tab")
# x = DecodeSongFile("songs/livinonaprayer.tab")
# PlaySong(x)
