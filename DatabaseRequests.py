import math
import tkinter as tk
import os
import shutil
from DatabaseRundown import get_rundown

# database_path = "C:\\Users\\theop\\OneDrive\\Desktop\\scouting_database"
# database_path = "C:\\Users\\timot\\python\\Scouting Stuff\\fake_database"
# database_path = "C:\\Users\\Liana\\Desktop\\scouting_database"
database_path = "scouting_database"

request_path = f"{database_path}\\Request"

# returns the path of first drive it finds
def get_drive() -> str:
    drives = os.popen("wmic logicaldisk get name").read().split()
    # drives = ["C:\Users\timot\python\Scouting Stuff\fake_drive"]

    for drive in drives:
        if (os.path.isdir(f"{drive}\\Matches")): return drive

# copys from database onto path
def copy_to_drive():
    drive = get_drive()
    if not drive: return
    
    copy_from = database_path
    copy_to = f"{drive}\\Request"

    if os.path.isdir(copy_to): shutil.rmtree(copy_to)    
    shutil.copytree(copy_from, copy_to)

def copy_from_drive():
    drive = get_drive()
    if not drive: return
    
    copy_from = f"{drive}\\Request"
    copy_to = database_path

    if os.path.isdir(copy_to): shutil.rmtree(copy_to)    
    shutil.copytree(copy_from, copy_to)

def query_match(nums: list[str]):
    shutil.rmtree(request_path)
    
    for num in nums:
        if not validate_team_num(num): continue

        copy_from = f"{database_path}\\{num}"
        copy_to = f"{request_path}\\{num}"

        shutil.copytree(copy_from, copy_to)

    print("opening")
    open_request()


def query_team(num: str):
    if not validate_team_num(num): return

    copy_from = f"{database_path}\\{num}"

    shutil.rmtree(request_path)
    shutil.copytree(copy_from, request_path)
    open_request()
    

def open_request():
    os.popen(f"explorer \"{request_path}\"")

def validate_team_num(num: str):
    try:
        int(num)
    except:
        return False
    
    if not os.path.isdir(f"{database_path}\\{num}"):
        return False

    return f"{database_path}\\{num}"

# ----------------- Tkinter Stuff -------------------

root = tk.Tk()
f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(root)
f4 = tk.Frame(root)
f5 = tk.Frame(root)

def raise_frame(frame) -> None:
    frame.tkraise()

def pack_menu() -> None:
    tk.Label(f1, text='Main Menu', ).pack()
    tk.Button(f1, text='view rundown', command=lambda:raise_frame(f5)).pack()
    tk.Button(f1, text='query a team', command=lambda:raise_frame(f2)).pack()
    tk.Button(f1, text='query an upcoming match', command=lambda:raise_frame(f3)).pack()
    tk.Button(f1, text='import/export database', command=lambda:raise_frame(f4)).pack()

def pack_team_query() -> None:
    tk.Label(f2, text="Team Query").grid(column=2, row=0, columnspan=2)
    entry = tk.Entry(f2, width=5)
    entry.grid(column=2, row=1)
    tk.Button(f2, text="query", command=lambda:query_team(entry.get())).grid(column=3, row=1)
    tk.Button(f2, text="<- back", command=lambda:raise_frame(f1)).grid(column=2, row=3)

def pack_match_query() -> None:
    tk.Label(f3, text="Match Query").grid(column=2, row=0, columnspan=2)
    entries = []
    for i in range(6):
        color = "red"
        if i % 2 == 1:
            color = "blue"

        entries.append(tk.Entry(f3, width=5, bg=color))
        entries[-1].grid(column=2 + (i % 2), row=math.floor(i/2))
    
    tk.Button(f3, text="query", command=lambda:query_match([e.get() for e in entries])).grid(column=2, row=3, columnspan=2)
    tk.Button(f3, text="<- back", command=lambda:raise_frame(f1)).grid(column=2, row=4, columnspan=2)

def pack_import_export() -> None:
    tk.Label(f4, text="Import/Export").pack()
    tk.Label(f4, text="Make sure one and only one drive is pulgged in.").pack()
    tk.Label(f4, text="These actions will take a while. \n DO NOT remove the drive or close this program.", fg="red").pack()
    tk.Button(f4, text="Export Database to Drive", command=copy_to_drive).pack()
    tk.Button(f4, text="Import Database from Drive", command=copy_from_drive).pack()
    tk.Button(f4, text="<- back", command=lambda:raise_frame(f1)).pack()

def pack_rundown() -> None:
    tk.Label(f5, text="Rundown").grid(column=2, row=0, columnspan=2)
    entry = tk.Entry(f5, width=5)
    entry.grid(column=2, row=1)
    tk.Button(f5, text="query", command=lambda:get_rundown(database_path,validate_team_num(entry.get()),entry.get())).grid(column=3, row=1)
    tk.Button(f5, text="<- back", command=lambda:raise_frame(f1)).grid(column=2, row=5)

def initialize_tkinter() -> None:
    f2.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    f3.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    f5.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    for frame in (f1, f2, f3, f4, f5):
        frame.config(width=300, height=300)
        frame.grid(row=0, column=0, sticky='news')

    pack_menu()

    pack_team_query()
    pack_match_query()
    pack_import_export()
    pack_rundown()

    raise_frame(f1)
    root.mainloop()


if __name__ == "__main__":
    initialize_tkinter()