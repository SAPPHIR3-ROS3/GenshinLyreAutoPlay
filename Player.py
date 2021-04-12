from concurrent import futures as Exec
from ctypes import windll as WinDLL
from DirectXInput import PressKey
from DirectXInput import ReleaseKey
from MIDIInterface import Compile
from multiprocessing import Manager
from os import listdir as DirList
from pickle import load as Load
from random import randint as Rand
from tkinter.ttk import Button as Button
from tkinter import Canvas as Canvas
from tkinter import Frame as TkPage
from tkinter import Label as Label
from tkinter import Listbox as ListBox
from tkinter import PhotoImage as Photo
from tkinter import StringVar as StringVar
from tkinter import Tk as App
from time import sleep as Sleep
from tkinter.ttk import Frame as Page
from tkinter.ttk import Scrollbar as SBar
from urllib.request import urlopen as URL

Notes=\
{
    'C3' : 'q', 'D3' : 'w', 'E3' : 'e', 'F3' : 'r', 'G3' : 't', 'A3' : 'y', 'B3' : 'u',
    'C2' : 'a', 'D2' : 's', 'E2' : 'd', 'F2' : 'f', 'G2' : 'g', 'A2' : 'h', 'B2' : 'j',
    'C1' : 'z', 'D1' : 'x', 'E1' : 'c', 'F1' : 'v', 'G1' : 'b', 'A1' : 'n', 'B1' : 'm',
} #Notes/Keyboard Mapping

DXCodes =\
{
    'q' : 0x10, 'w' : 0x11, 'e' : 0x12, 'r' : 0x13, 't' : 0x14, 'y' : 0x15, 'u' : 0x16,
    'a' : 0x1E, 's' : 0x1F, 'd' : 0x20,  'f' : 0x21, 'g' : 0x22, 'h' : 0x23, 'j' : 0x24,
    'z' : 0x2C, 'x' : 0x2D, 'c' : 0x2E, 'v' : 0x2F, 'b' : 0x30, 'n' : 0x31, 'm' : 0x32,
} #Keyboard/DirectX Mapping

def IsAdmin(): #this function check if the script as Admin Priviledges
    try:
        return WinDLL.shell32.IsUserAnAdmin() #attempt to use shell as Admin (rights verification)
    except:
        return False # if the user is not admin an exception will be thrown and catched

class ScrollableFrame(Page):
    def __init__(self, Parent, *args, **kwargs):
        super().__init__(Parent, *args, **kwargs)
        FullFrame = Canvas(self)
        SideBar = SBar(self, orient="vertical", command=FullFrame.yview)
        self.ViewFrame = Page(FullFrame)
        self.ItemList = dict()
        self.ViewFrame.bind( "<Configure>", lambda Event: FullFrame.configure(scrollregion = FullFrame.bbox("all")))
        FullFrame.create_window((0, 0), window=self.ViewFrame, anchor="nw")
        FullFrame.configure(yscrollcommand=SideBar.set)
        FullFrame.pack(side="left", fill="both", expand=True)
        SideBar.pack(side="right", fill="y")

    def Add(self, ItemName, Item, *args, **kwargs):
        if ItemName in ItemList:
            raise KeyError('key already exists in the dictionary, try using a different value for parameter ItemName instead of ' + ItemName +
            ', instead if you want to remove an item use self.Remove(ItemName)')
        else:
            self.ItemList[ItemName] = Item(self.ViewFrame, *args, **kwargs)
            self.ItemList[ItemName].pack()

    def Remove(self, ItemName):
        if ItemName in ItemList:
            self.ItemList.remove(ItemName)
        else:
            raise KeyError('key does not exists in the dictionary')

class Home(TkPage):
    Name = 'Home' #name of the class (attributes)
    Font = lambda Size: ('Courier', Size) #font of the page

    def __init__(self, Parent, *args, **kwargs):
        super().__init__(Parent, *args, **kwargs) #constructor of super class

        self.Songs = [Song.replace('.mid', '') for Song in DirList('Songs') if Song.endswith('.mid')] #mappable songs
        self.MappedSongs = [Song.replace('.cmid', '') for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #mapped and compiled song

        TopLabel = Label(self, text = 'Genshin Lyre Player', font= Home.Font(24), bd = 10) #top label with a title for the page
        TopLabel.place(anchor= 'n', relx= 0.5, rely = 0.015, relwidth = 1, relheight=0.15) #placing the label

        self.ItemList = ListBox(self) #item list of the song
        for Item in self.MappedSongs: #for loop for every compiled comiled song
            self.ItemList.insert(self.MappedSongs.index(Item), Item) #indexing the song in the list
        self.ItemList.place(anchor= 'n', relx= 0.5, rely = 0.2, relwidth = 1, relheight=0.5) #placing the item list

        RefreshLogo = Photo(file = 'Res/Refresh.png') #logo of refresh button (not showing at the moment)
        Refresh = Button\
        (
            self,
            image = RefreshLogo,
            command = lambda : self.Refresh()
        ) #button to refresh the song list
        Refresh.image = RefreshLogo########
        Refresh.place(anchor= 'nw', relx= 0.01, rely = 0.71, relwidth = 0.1, relheight = 0.12) #placing the button

        PlayLogo = Photo(file = 'Res/Play.png') #logo of play button (not showing at the moment)
        Play = Button\
        (
            self,
            image = PlayLogo,
            command = lambda : self.Play()
        )#button to play the song selected
        Play.image = PlayLogo ##########
        Play.place(anchor= 'nw', relx= 0.295, rely = 0.71, relwidth = 0.2, relheight = 0.22) #placing the button

        PauseLogo = Photo(file = '') #logo of the pause button
        Pause = Button\
        (
            self,
            image = PauseLogo,
            command = lambda : self.Pause()
        ) #button to pause a song
        Pause.place(anchor= 'nw', relx= 0.505, rely = 0.71, relwidth = 0.2, relheight = 0.22) #placing the button

    def Refresh(self): #this function refresh the song list
        self.MappedSongs = [Song for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #check the folder for the songs
        self.ItemList.delete('0','end') #delete every item of the list
        for Item in self.MappedSongs: #loop for every song in the folder
            self.ItemList.insert(self.MappedSongs.index(Item), Item) #index the song in the item list

    def Play(self):
        Song = self.ItemList.get('active')
        with open('Mapped/' + Song, 'rb') as InputFile:
            File = Load(InputFile)

        RM = Manager() #locks mannager
        KeyLocks =\
        {
            'q' : RM.Lock(), 'w' : RM.Lock(), 'e' : RM.Lock(), 'r' : RM.Lock(), 't' : RM.Lock(), 'y' : RM.Lock(), 'u' : RM.Lock(),
            'a' : RM.Lock(), 's' : RM.Lock(), 'd' : RM.Lock(),  'f' : RM.Lock(), 'g' : RM.Lock(), 'h' : RM.Lock(), 'j' : RM.Lock(),
            'z' : RM.Lock(), 'x' : RM.Lock(), 'c' : RM.Lock(), 'v' : RM.Lock(), 'b' : RM.Lock(), 'n' : RM.Lock(), 'm' : RM.Lock(),
        } #Keyboard Locks

        with Exec.ProcessPoolExecutor() as Executor: #multi process context manager
            for Part in File: #for loop for every MIDI
                pass

    def PlayPart(self, Part = [], Locks): # funtion to play MIDI track (multi process)
        for Element in Part: # loop for eery element
            Fraction = Duration / 10 # 10% of the duration
            Sleep(Rand(40, 200) / (10**7)) #human randomness simulation

            if Element['Type'] == 'Note': #check if element type is note
                Key = Element['Sound'] + Element['Octave'] #full note
                Duration = Element['Duration'] #copy the duration of the note

                if Locks[Key].locked(): #check if the key binded to the note is locked
                Fraction = Duraion / 100 # 1% of the duration

                    while Duration > 0: # while the note can still be played
                        if Locks[Key].locked(): #check if the key binded to the note is locked
                            Sleep(Fraction) #wait a fraction of the duration
                            Duration -= Fraction #subtract the fraction  from the duration and update the duration
                        else: #if the key binded to the note is free
                            Locks[Key].acquire() #lock the resource for other processes
                            PressKey(DXCodes[Key]) #key press of the note
                            Sleep(Duration + (Rand(-250, 250) / (10**7))) #wait the duration of the note + human randomness
                            ReleaseKey(DXCodes[Key]) #key release of the note
                            Locks[Key].release() #release the resourse for other process
                            Duration = 0

                else: #if the key binded to the note is free
                    Locks[Key].acquire() #lock the resource for other processes
                    PressKey(DXCodes[Key]) #key press of the note
                    Sleep(Element['Duration'] + (Rand(-250, 250) / (10**7))) #wait the duration of the note + human randomness
                    ReleaseKey(DXCodes[Key]) #key release of the note
                    Locks[Key].release() #release the resourse for other process

            if Element['Type'] == 'Chord': # check if the element is a chord
                Duration = Element['Duration'] #copy the duration of the note
                Keys = [Notes[Note + Octave] for Note in zip(Element['Sound'], Element['Octave'])] #list with full notes
                Locked = [] #list of externally locked resources
                Unlocked = [] #list of internally locked resources

                for Key in Keys: #for loop for every key binded to the chord
                    if Locks[Key].locked(): #check if the key is locked
                        Locked.append(Key) #append the locked key to locked resources
                    else: #the resource is not locked
                        Locked[Key].acquire() #the resourse is locked by this section
                        Unlocked.append(Key) #the free key binded to the note of the chord is appended to the list of internally locked resources

                if len(Unlocked) < len(Keys): #check if all required resources are available
                    Fraction = Duration / 100 # 1% of the duration

                    while Duration > 0: #while the note can still be played
                        if len(Locked) > 0: #check if there is some unavailable resources
                            for Key in Locked[:]: #for loop for every locked resource
                                if not Locked[Key].locked(): #check (again) if the resource is (still) locked
                                    Locked[Key].acquire() #locked the resource
                                    Unlocked.insert(Keys.index(Key), Locked.pop(Locked.index(Key))) #remove the item from locked resource and insert it in internally locked resources

                            Sleep(Fraction) #wait the fraction of playable time
                            Duration -= Fraction #remove the fraction from total duration

                        if len(Locked) == 0 or Duration == Fraction: #check if the chord is still playable
                            if Duration == Fraction and not len(Locked) == 0: #check if chord can still be played and all needed resources are available
                                Sleep(Duration + (Rand(-250, 250) / (10**7))) #wait the duration of the note + human randomness
                                Duration = 0 #set the duration to 0 to exit the loop

                            if len(Locked) == 0: #check if all needed resources are available
                                for Key in Keys: #for loop for every note of the chord
                                    PressKey(DXCodes[Key]) #key press of the note
                                    Sleep(Rand(0, 250) / (10**7)) #wait the time of human interaction

                                Sleep(Duration + (Rand(-250, 250) / (10**7))) #wait the duration of the note + human randomness

                                for Key in Unlocked:
                                    ReleaseKey(DXCodes[Key]) #key release of the note
                                    Locks[Key].release() #release the resourse for other process
                                    Sleep(Rand(0, 250) / (10**7)) #wait the time of human interaction

                                Duration = 0#set the duration to 0 to exit the loop

                if len(Unlocked) == len(Keys): #if all the resource are available (first try)
                    for Key in Unlocked: #for loop for every note of the chord (pressing)
                        PressKey(DXCodes[Key]) #key press of the note
                        Sleep(Rand(0, 250) / (10**7)) #wait the time of human interaction

                    Sleep(Duration + (Rand(-250, 250) / (10**7))) #wait the duration of the note + human randomness

                    for Key in Unlocked: #for loop for every note of the chord (releasing)
                        ReleaseKey(DXCodes[Key]) #key release of the note
                        Locks[Key].release() #release the resourse for other process
                        Sleep(Rand(0, 250) / (10**7)) #wait the time of human interaction

                ################################################TODO

    def Pause(self):
        pass

class GenshinLyrePlayer(App): #class for main app
    Screen =\
    {
        Home.Name : None
    } #dictionary of all the pages
    def __init__(self):
        super().__init__() #constructor of super class
        self.iconphoto(True, Photo(file = 'Res/Logo.png')) #setting icon of the app

        if not IsAdmin(): #checking if the user has admin rights
            HEIGHT = int(self.winfo_screenheight() * 0.3) #getting the height of screen and dividing by 3 and setting it as height of the window
            WIDTH = int(HEIGHT * 1.2) #setting the height * 1.2 as width of the window
            Sizes = str(WIDTH) + 'x' + str(HEIGHT) #converting the sizes in a string
            X = int((self.winfo_screenwidth() - WIDTH) / 2) #setting the starting x as center of the screen
            Y = int((self.winfo_screenheight() - HEIGHT) / 2) #setting the starting y as center of the screen
            Pos = '+' + str(X) + '+' + str(Y) #formatting the position
            self.geometry(Sizes + Pos) # setting size and position of the window
            self.title('GenshinImpactLyreAutoplay') # setting the title of the window
            GenshinLyrePlayer.Screen[Home.Name] = Home(self) #initializing the home screen
            GenshinLyrePlayer.Screen[Home.Name].place(relx = 0, rely = 0, relwidth = 1, relheight = 1) #positioning the the home as full window

        else: #if the user has no admin rights
            self.AlternativeStart() #show a warning to restart with admin rights

    def AlternativeStart(self): #this function is a warning to restart as admin
        self.title('Warning') #setting a different title
        Warning = Label(self, text = 'Restart this program as', font = ('Courier', 24)) #warning label first line
        WarningBottom = Label(self, text = 'Admin', font = ('Courier',24)) #warning label second line
        Warning.pack() #automatically position the first label
        WarningBottom.pack() #automatically positioning the second label

    def Raise(ScreenName = str()): #raising the selected screen to the top
        GenshinLyrePlayer.Screen[ScreenName].tkaise() #accessing the screen from the dictionary and raising it

if __name__ == '__main__':
    Application = GenshinLyrePlayer() #app initialization
    Application.mainloop()
