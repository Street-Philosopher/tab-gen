

print("importing")

import tkinter as tk
from tkinter import filedialog as fd

print("beginning")

def CreateMenuBar():
	menubar = tk.Menu(window)
	window.config(menu=menubar)

	CreateFileMenu(menubar)
#END
def CreateFileMenu(menubar: tk.Menu):
	from mainmenu import LoadSong, ResetSong
	from filemanager import GetRecentFiles

	filemenu = tk.Menu(menubar)
	menubar.add_cascade(label="File", menu=filemenu)
	
	# create new
	filemenu.add_command(
		label="Create new",
		command=ResetSong
	)

	# open file
	filemenu.add_command(
		label="Open",
		command=LoadSong
	)

	# recent files
	recent_files = GetRecentFiles()
	rf_menu = tk.Menu(menubar)
	for file in recent_files:
		rf_menu.add_command(
			label=file,
			command=lambda f=file: LoadSong(f)
		)
	filemenu.add_cascade(
		label="Open recent file",
		menu=rf_menu
	)


def main():
	print("yes?")
	global window
	window = tk.Tk()
	window.geometry("1000x600")
	window.resizable(False, False)
	frame = tk.Frame(window)

	CreateMenuBar()

	from mainmenu import mainmenu
	mainmenu(window, frame)

	window.mainloop()
#END

if __name__ == "__main__":
	main()
