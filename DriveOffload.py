import os
import shutil
import tkinter as tk

# TODO !!! WHEN BUILDING FIX LINES 9 AND 15 !!!

# -------------- IMPORTANT STUFF --------------

database_path = "C:\\Users\\timot\\python\\Scouting Stuff\\all_matches"
# database_path = "C:\\Users\\theop\\OneDrive\\Desktop\\scouting_database"

# locates the path of flash drive
def get_drive_paths() -> dict:
    # gets all drives on device
    # drives = os.popen("wmic logicaldisk get name").read().split()
    drives =["fake_drive"]

    paths = {
        "matches": [],
        "pits": []
    }

    for drive in drives:
        if(os.path.isdir(f"{drive}\\Matches") == True):
            paths["matches"].append(f"{drive}\\Matches")
            paths["pits"].append(f"{drive}\\Pits")
    
    return paths

# checks if the correct database 
def check_directory(team_num: str) -> str:
    folder_path = f"{database_path}\\{team_num}"
    pit_path = f"{folder_path}\\Pits"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        os.makedirs(pit_path)
    
    return folder_path, pit_path

def read_drives() -> None:
    drive_paths = get_drive_paths()
    for drive_match_path in drive_paths["matches"]:
        read_drive(drive_match_path, False)
    
    for drive_pit_path in drive_paths["pits"]:
        read_drive(drive_pit_path, True)

    # for drive_pit_path in drive_paths["pits"]:
    #     drive_pit_dir = os.listdir(driv)

def read_drive(dir_source: str, is_pit: bool) -> None:
    drive_dir = os.listdir(dir_source)

    for file_name in drive_dir:
        team_num = get_team_num(file_name)

        copy_source = f"{dir_source}\\{file_name}"

        data_match_path, data_pit_path = check_directory(team_num)

        if is_pit:
            copy_destination = f"{data_pit_path}\\{file_name}"
        else:
            copy_destination = f"{data_match_path}\\{file_name}"
        
        if os.path.exists(copy_destination): continue

        shutil.copyfile(copy_source, copy_destination)
        
        
# finds the team number in file name and returns it
def get_team_num(file_name: str) -> str:
    start_id = file_name.rfind("T")
    end_id = file_name.find("-", start_id)
    team_num = file_name[start_id + 1:end_id]
    return team_num



# --------------- TKINTER STUFF --------------

root = tk.Tk()

def initialize_tk_window() -> None:
    root.title = "Drive Offloader"
    root.attributes("-topmost", True)
    root.geometry("300x300")

    text = tk.Label(root, text="Do you have the drive plugged in?")
    text.pack()

    button = tk.Button(
                        root, text="YES", command=read_drives, 
                        height=10, width=30,
                        bg="#afb7c4"
                       )
    button.pack()

    root.mainloop()


def main(): 
    initialize_tk_window()

if __name__ == "__main__":
    main()