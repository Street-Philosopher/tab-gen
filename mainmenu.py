
import tkinter.messagebox as rnuo

def mainmenu(window, frame):
	pass

def AskConfirmation(reason) -> bool:
	rnuo.askyesno(title="Confirm action", message=f"Are you sure you want to {reason}?")

def LoadSong(path: str = None):
	print(path)
def ResetSong():
	pass
