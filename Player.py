from concurrent import futures as Exec
from ctypes import windll as WinDLL
from DirectXInput import PressKey
from DirectXInput import ReleaseKey
from MIDIInterface import Compile
from multiprocessing import Lock
from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing import Process
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

def PlayPart(Part = [], Locks = dict()): # funtion to play MIDI track (multiprocessing)
    for Element in Part:
        if Element['Type'] == 'Note': #check if the element is a note
            Note = Element['Sound'] + str(Element['Octave']) #full note
            Key = DXCodes[Notes[Note]] #key to press binded to the note
            Duration = Element['Duration'] #element duration in seconds
            Fraction = Duration / 10 #fraction of duration (loop porpuses)

            if Locks[Note].locked(): #check id the resource is not locked by other processes
                while Locks[Note].locked() and Duration > Fraction: #while the note can not be played and can still be played
                    Sleep(Fraction) #sleep a fraction of the duration to check later in time id the resource is free
                    Duration -= Fraction #remove the fraction from the total duration

                if not Locks[Note].locked() and Duration > Fraction: #check the resource is available and has still sense play it
                    Locks[Note].acquire() #lock the resource for other processes
                    PressKey(Key) #press the key binded to the element
                    Sleep(Duration) #wait the (partial) duration of the element
                    Duration = 0 #the note is played and the duration is not needed anymore
                    ReleaseKey(Key) #release the key binded to the element
                    Locks[Note].release() #unlock the resource for other processes

                else: #check if it has no more sense to be played
                    Sleep(Duration) #sleep the remaining duration of the element
            else: #the resource is available right away
                Locks[Note].acquire() #lock the resource for other processes
                PressKey(Key) #press the key binded to the element
                Sleep(Duration) #wait the duration of the element
                ReleaseKey(Key) #release the key binded to the element
                Locks[Note].release() #unlock the resource for other processes

        if Element['Type'] == 'Chord': #check if the element is a chord
            Chord = [Note + str(Octave) for Note, Octave in zip(Element['Sound'], Element['Octave'])] #full chord
            Keys = [DXCodes[Notes[Note]] for Note in Chord] #keys to press binded to the chord
            Duration = Element['Duration'] #element duration in seconds
            Fraction = Duration / 10 #fraction of duration (loop porpuses)

            if all([Locks[Note].locked() for Note in Chord]): #check if all the resources not locked by other processes
                while not all(list([Locks[Note].locked() for Note in Chord])) and Duration > Fraction: #while the note can not be played and can still be played
                    Sleep(Fraction) #sleep a fraction of the duration to check later in time id the resource is free
                    Duration -= Fraction #remove the fraction from the total duration

                if all([not Locks[Note].locked() for Note in Chord]) and Duration > Fraction: #while the note can not be played and can still be played
                    for Note in Chord: #for loop for every note of the chord
                        Locks[Note].aquire() #lock the resource for other processes
                    for Key in Keys: #for loop for every key that need to be pressed
                        PressKey(Key) #press the key binded to the element

                    Sleep(Duration) #wait the (partial) duration of the element

                    for Key, Note in zip(Keys, Chord):
                        ReleaseKey(Key) #release the key binded to the element
                        Locked[Note].release() #unlock the resource for other processes

                else: #check if it has no more sense to be played
                    Sleep(Duration) #sleep the remaining duration of the element
            else: #the resources are available right away
                for Note in Chord: #for loop for evry note of the chord
                    Locks[Note].aquire() #lock the resource for other processes

                for Key in Keys:
                    PressKey(Element) #press the key binded to the element

                Sleep(Duration) #wait the duration of the element

                for Element in Unlocked:
                    ReleaseKey(Element) #release the key binded to the element
                    Locked[Element].release() #unlock the resource for other processes

        if Element['Type'] == 'Rest': #check if the element is a rest
            Duration = Element['Duration'] #element duration in seconds
            Sleep(Duration) #wait the (partial) duration of the element

class Home(TkPage):
    Name = 'Home' #name of the class (attributes)
    Font = lambda Size: ('Courier', Size) #font of the page

    def __init__(self, Parent, *args, **kwargs):
        super().__init__(Parent, *args, **kwargs) #constructor of super class

        self.Songs = [Song.replace('.mid', '') for Song in DirList('Songs') if Song.endswith('.mid')] #mappable songs
        self.MappedSongs = [Song for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #mapped and compiled song

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
            text = 'Play',
            command = lambda : self.Play()
        )#button to play the song selected
        Play.image = PlayLogo ##########
        Play.place(anchor= 'nw', relx= 0.295, rely = 0.71, relwidth = 0.2, relheight = 0.22) #placing the button

        PauseLogo = Photo(file = '') #logo of the pause button
        Pause = Button\
        (
            self,
            text = 'Pause',
            command = lambda : self.Pause()
        ) #button to pause a song
        Pause.place(anchor= 'nw', relx= 0.505, rely = 0.71, relwidth = 0.2, relheight = 0.22) #placing the button

    def Refresh(self): #this function refresh the song list
        self.MappedSongs = [Song for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #check the folder for the songs
        self.ItemList.delete('0','end') #delete every item of the list
        for Item in self.MappedSongs: #loop for every song in the folder
            self.ItemList.insert(self.MappedSongs.index(Item), Item) #index the song in the item list

    def Play(self):
        Song = self.ItemList.get('active') #getting the selected song from the list

        for i in range(5): #countdown
            print(5 - i)
            Sleep(1)

        with open('MappedSongs/' + Song, 'rb') as InputFile: #opening the compiled midi fil
            File = Load(InputFile)

        RM = Manager()
        KeyLocks =\
        {
            'C3' : RM.Lock(), 'D3' : RM.Lock(), 'E3' : RM.Lock(), 'F3' : RM.Lock(), 'G3' : RM.Lock(), 'A3' : RM.Lock(), 'B3' : RM.Lock(),
            'C2' : RM.Lock(), 'D2' : RM.Lock(), 'E2' : RM.Lock(),  'F2' : RM.Lock(), 'G2' : RM.Lock(), 'A2' : RM.Lock(), 'B2' : RM.Lock(),
            'C1' : RM.Lock(), 'D1' : RM.Lock(), 'E1' : RM.Lock(), 'F1' : RM.Lock(), 'G1' : RM.Lock(), 'A1' : RM.Lock(), 'B1' : RM.Lock(),
        } #Keyboard Locks

        Parts = [Process(target = PlayPart, args = (Part, KeyLocks)) for Part in File]

        for Part in Parts:
            Part.start()

        for Part in Parts:
            Part.join()

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

        if IsAdmin(): #checking if the user has admin rights
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
