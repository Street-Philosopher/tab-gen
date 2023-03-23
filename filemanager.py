
import os


_RECENT_FILES_PATH = "./.recent"


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

