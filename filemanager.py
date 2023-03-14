
import os
from structs import song
from constants import BASS_STANDARD_TUNE_4


_RECENT_FILES_PATH = "./.recent"

TAB_FILE_VERSION = 0x00

HEADER_END_OFFSET = SONG_NAME_START_OFFSET = 0x20
SONG_NAME_MAX_LENGTH = 0x40
SONG_NAME_END_OFFSET = SONG_AUTH_START_OFFSET = 0x60
SONG_AUTH_MAX_LENGTH = 0x40
SONG_AUTH_END_OFFSET = SONG_TUNING_START_OFFSET = 0xA0

MAX_STRINGS_FOR_TUNE = 0x0F
SONG_TUNING_END_OFFSET = 0xB0


def OpenSongFile(path: str) -> song:
	pass
def EncodeSongToFile(song: song, path: str) -> bool | Exception:
	try:
		with open(path, "wb") as file:
			# header
			file.write(bytes("TAB", "utf-8"))
			file.write(TAB_FILE_VERSION.to_bytes(length=1, byteorder="big"))
			file.write(bytes("\0" * (HEADER_END_OFFSET - file.tell()), "utf-8"))

			# song title
			if len(song.title) > SONG_NAME_MAX_LENGTH:
				raise ValueError(f"The song's title is too long (max: {SONG_NAME_MAX_LENGTH} characters)")
			file.write(bytes(song.title, "utf-8"))
			Fill(file, SONG_NAME_END_OFFSET)

			# song author
			if len(song.author) > SONG_AUTH_MAX_LENGTH:
				raise ValueError(f"The song's author name is too long (max: {SONG_AUTH_MAX_LENGTH} characters)")
			file.write(bytes(song.author, "utf-8"))
			Fill(file, SONG_AUTH_END_OFFSET)

			# tuning
			if len(song.tuning) > MAX_STRINGS_FOR_TUNE:
				raise ValueError(f"Too many strings in the bass tuning (max: {MAX_STRINGS_FOR_TUNE} strings)")
			file.write(len(song.tuning).to_bytes(length=1, byteorder="big"))
			for string_tune in song.tuning:
				file.write(string_tune.to_bytes(length=1, byteorder="big", signed=True))
			Fill(file, SONG_TUNING_END_OFFSET)

			# measures
	except Exception as e:
		# TODO: probably best to first write to a dummy buffer and at the end write to a file, so we don't delete it if it already existed
		os.remove(path)
		return e
	else:
		return True
def Fill(file, to_offset):
	file.write(bytes("\0" * (to_offset - file.tell()), "utf-8"))


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
