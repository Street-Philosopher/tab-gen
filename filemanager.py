
import os
from structs import song


_RECENT_FILES_PATH = "./.recent"


def AddToRecentFiles(path):
	pass


def CreateNewSongFile(path: str) -> song:
	print(path)
def OpenSongFile(path: str) -> song:
	pass


def GetRecentFiles() -> list[str]:
	if os.path.isfile(_RECENT_FILES_PATH):
		with open(_RECENT_FILES_PATH) as f:
			raw = f.read(-1)
		items = raw.split("\n")
		return items
	else:
		return []
