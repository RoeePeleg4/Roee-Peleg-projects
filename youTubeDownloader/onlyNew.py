import os

#removing all the not new songs from the new directory
def changeBetween(allDirectory , newDirectory):
    allList = os.listdir(allDirectory)
    newList = os.listdir(newDirectory)
    for file in newList:
        if (file in allList):
            print(f"{newDirectory}\\{file}")
            os.remove(f"{newDirectory}\\{file}")

# moving the new songs from the new directory to the all directory
def updateAllDirectory(allDirectory , newDirectory):
    #os.rename(current, destination)
    #new is current and detination is all
    newList = os.listdir(newDirectory)
    for file in newList:
        print(f"{newDirectory}\\{file}", f"{allDirectory}\\{file}")
        os.rename(f"{newDirectory}\\{file}", f"{allDirectory}\\{file}")

def main():
    # D:\music\allSongs
    allDirectory = input("enter the directory that all of the songs are in: ")
    # D:\music\newSongs
    newDirectory = input("enter the directory that you want only the new in: ")
    choise = input("to remove the old songs press 1\nto update the directory of all songs to include also the new press 2\nenter your choise: ")
    while choise not in ["1","2"]:
        choise = input("invalid answer please reEnter: ")
    choise = int(choise)
    if choise == 1:
        changeBetween(allDirectory , newDirectory)
    else:
        updateAllDirectory(allDirectory , newDirectory)
    print("[SYSTEM] finished successFully")
    
if __name__ == "__main__":
    main()