from ctypes import windll as WinDLL
from DirectXInput import PressKey
from DirectXInput import ReleaseKey
from keyboard import is_pressed as IsPressed
from MIDICompiler import Compile
from os import listdir as DirList
from os import makedirs as MakeDirs
from os.path import exists as Exists
from pickle import load as Load
from random import randint as Rand
from sys import exit as Exit
from tkinter import Canvas as Canvas
from tkinter import Frame as TkPage
from tkinter import IntVar as IntVar
from tkinter import Label as Label
from tkinter import Listbox as ListBox
from tkinter import PhotoImage as Photo
from tkinter import StringVar as StringVar
from tkinter import Tk as App
from tkinter.ttk import Button as Button
from tkinter.ttk import Checkbutton as Check
from tkinter.ttk import Frame as Page
from tkinter.ttk import Radiobutton as Radio
from tkinter.ttk import Scrollbar as SBar
from time import sleep as Sleep
from threading import active_count as ThreadCount
from threading import currentThread as Current
from threading import enumerate as ThreadList
from threading import Event as ThreadEvent
from threading import get_ident as Identity
from threading import Lock as Call
from threading import main_thread as MainThread
from threading import Thread

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

NotesFlags =\
{
    'C3' : True, 'D3' : True, 'E3' : True, 'F3' : True, 'G3' : True, 'A3' : True, 'B3' : True,
    'C2' : True, 'D2' : True, 'E2' : True, 'F2' : True, 'G2' : True, 'A2' : True, 'B2' : True,
    'C1' : True, 'D1' : True, 'E1' : True, 'F1' : True, 'G1' : True, 'A1' : True, 'B1' : True,
}

PauseFunction = Call()
StopFunction = Call()

def ReleaseResources():
    for Note in NotesFlags: #for loop for every flag
        if not NotesFlags[Note]: #check if the resource is locked
            ReleaseKey(DXCodes[Notes[Note]]) #free the resource
            NotesFlags[Note] = True #set the resource as available

    print('resource released')

def IsAdmin(): #this function check if the script as Admin Priviledges
    try:
        return WinDLL.shell32.IsUserAnAdmin() #attempt to use shell as Admin (rights verification)
    except:
        return False #if the user is not admin an exception will be thrown and catched

def IsMainAlive(): #check if the program is still running
    return MainThread().is_alive()

class Home(TkPage):
    Name = 'Home' #name of the class (attributes)
    Font = lambda Size: ('Courier', Size) #font of the page

    def __init__(self, Parent, *args, **kwargs):
        super().__init__(Parent, *args, **kwargs) #constructor of super class

        self.Songs = [Song.replace('.mid', '') for Song in DirList('Songs') if Song.endswith('.mid')] #mappable songs
        self.MappedSongs = [Song for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #mapped and compiled song
        self.Playing = ThreadEvent() #pause state
        self.Stop = ThreadEvent() #playing state
        self.Stop.set()

        TopLabel = Label(self, text = 'Genshin Lyre Player', font= Home.Font(24), bd = 10) #top label with a title for the page
        TopLabel.place(anchor= 'n', relx= 0.5, rely = 0.015, relwidth = 1, relheight=0.15) #placing the label

        self.ItemList = ListBox(self) #item list of the song
        for Index,Item in enumerate(self.MappedSongs): #for loop for every compiled comiled song
            self.ItemList.insert(Index, Item) #indexing the song in the list
            self.ItemList.itemconfig(Index, {'bg' : '#C2C2C2'}) #background of itemlist
        self.ItemList.place(anchor= 'n', relx= 0.5, rely = 0.19, relwidth = 1, relheight = 0.46) #placing the item list

        #RefreshLogo = Photo(file = 'Res/Refresh.png') #logo of refresh button (not showing at the moment)
        self.RefreshButton = Button\
        (
            self,
            text = 'Refresh',
            command = lambda : self.Refresh()
        ) #button to refresh the song list
        #self.RefreshButton.image = RefreshLogo ########
        self.RefreshButton.place(anchor= 'nw', relx = 0.01, rely = 0.7, relwidth = 0.18, relheight = 0.2) #placing the button

        self.StopButton = Button\
        (
            self,
            text = 'Stop',
            command = lambda : self.StopSong()
        )
        self.StopButton.place(anchor= 'nw', relx= 0.21, rely = 0.7, relwidth = 0.18, relheight = 0.2)

        #PlayLogo = Photo(file = 'Res/Play.png') #logo of play button (not showing at the moment)
        self.PlayButton = Button\
        (
            self,
            text = 'Play',
        )#button to play the song selected
        self.PlayButton.config\
        (
            command =\
            lambda:
            [
                Thread(target = self.PlayTrack, args = (Track,), name = f'{self.ItemList.get("active")}[{i}]', daemon = True).start()
                for i, Track in enumerate(self.LoadSong())
            ]#lambda: self.Play()
        )
        #self.PlayButton.image = PlayLogo ##########
        self.PlayButton.place(anchor= 'nw', relx= 0.41, rely = 0.7, relwidth = 0.18, relheight = 0.2) #placing the button

        #PauseLogo = Photo(file = '') #logo of the pause button
        self.PauseButton = Button\
        (
            self,
            text = 'Pause',
            command = lambda : self.PauseSong()
        ) #button to pause a song
        self.PauseButton.place(anchor= 'nw', relx= 0.61, rely = 0.7, relwidth = 0.18, relheight = 0.2) #placing the button

        self.CompileButton = Button\
        (
            self,
            text = 'Compilation\n     Screen',
            command = lambda : self.Compile(),
        )
        self.CompileButton.place(anchor = 'nw', relx= 0.81, rely = 0.7, relwidth = 0.18, relheight = 0.2) #placing the button

    def Refresh(self): #this function refresh the song list
        self.MappedSongs = [Song for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #check the folder for the songs
        self.ItemList.delete('0','end') #delete every item of the list
        for Index, Item in enumerate(self.MappedSongs): #loop for every song in the folder
            self.ItemList.insert(Index, Item) #index the song in the item list
            self.ItemList.itemconfig(Index, {'bg' : '#C2C2C2'}) #background of the itemlist

    def Countdown(self): #this function create an initial countdown
        for i in range(3): #3...2...1
            print(3-i)
            self.after(1000)

    def LoadSong(self):
        self.PlayButton.state(['disabled']) #disable the play button (might cause some unexpected behaviours)
        Song = self.ItemList.get('active') #getting the selected song from the list
        self.Stop.clear() #reset the stop state
        self.Playing.set()

        with open('MappedSongs/' + Song, 'rb') as InputFile: #opening the compiled midi file
            Music = Load(InputFile) #load the searialized object

        self.Countdown() #initial countdown to give user time to switch to genshin

        return Music

    def PlayTrack(self, Part = None): #this (THREADED) function play a single part (track) of the selected song
        if Part == None:
            raise ValueError('Part cannot be None')
        else:
            print(f'{Identity()} ready')

        global Notes
        global DXCodes
        global NotesFlags
        Elements = len(Part) #keystrokes to execute
        Actual = 0 #element counter

        def PlayNote(Sound, Duration): #this function play a single note of the part
            NotesFlags[Sound] = False #make the resource unavailable for other threads (to avoid deadlock)
            PressKey(DXCodes[Notes[Sound]]) #press note-corresponding key
            Sleep(abs(Duration)) #wait the duration of the note
            ReleaseKey(DXCodes[Notes[Sound]]) #release note-corresponding key
            NotesFlags[Sound] = True #make the resource available for other threads

        def PlayChord(Sounds, Duration): # function play a single chord of the part
            #print(Duration)
            for Sound in Sounds: #for loop  to make every note of the chord unavailable for other threads (to avoid deadlock)
                NotesFlags[Sound] = False #lock single resource

            for Sound in Sounds: #for loop to press chord-corresponding keys
                PressKey(DXCodes[Notes[Sound]]) #press the note-corresponding key of the chord

            Sleep(abs(Duration)) #wait the duration of the notes

            for Sound in Sounds: #for loop to release chord-corresponding keys
                ReleaseKey(DXCodes[Notes[Sound]]) #release the note-corresponding key of the chord

            for Sound in Sounds:#for loop to make every note of the chord available for other threads
                NotesFlags[Sound] = True #unlock single resource

        while not self.Stop.is_set() and Actual < Elements:
            if IsPressed('ctrl+space'):
                if not PauseFunction.locked():
                    PauseFunction.acquire()
                    self.StopSong()
                    PauseFunction.release()
                break
            if IsPressed('shift'):
                print('resume trigger')
                Sleep(1)
                self.Playing.set()

            while self.Playing.is_set() and Actual < Elements:
                if IsPressed('ctrl+space'):
                    if not PauseFunction.locked():
                        PauseFunction.acquire()
                        self.StopSong()
                        PauseFunction.release()
                    break
                if IsPressed('shift'):
                    print('pause trigger')
                    Sleep(1)
                    self.Playing.clear()
                    break

                Counter = 0

                if Part[Actual]['Type'] == 'Note': #check if the element is a note
                    Duration = float(Part[Actual]['Duration'])
                    PartialDuration = Duration / 10 #duration splitted to check multiple times
                    Note = f'{Part[Actual]["Sound"]}{Part[Actual]["Octave"]}' #extract the note

                    if NotesFlags[Note] and IsMainAlive(): #check if the resource is available
                        PlayNote(Note, Duration) #if the reseourse plays the note at full duration
                    else: #if the resource is not available at the moment
                        while not NotesFlags[Note] or Counter < 10: #check if the note is still playable
                            Sleep(PartialDuration) #waiting the partial duration to check availability
                            Counter += 1 #increasing wastd times

                        if NotesFlags[Note] and Counter < 10: #check if the resource are available and the note is still playable
                            RemainingDuration = Duration - (PartialDuration * Counter) #calculate remaining duration
                            PlayNote(Note, RemainingDuration) #play the note at partial duration
                elif Part[Actual]['Type'] == 'Chord': # check if the element is a chord (multiple notes together)
                    NotesList = Part[Actual]['Sound'] #extract notes of the chord
                    Octaves = Part[Actual]['Octave'] #extract respective octaves of the notes
                    Chord = [f'{Note}{Octave}' for Note, Octave in zip(NotesList, Octaves)] # combine notes and octaves together
                    Duration = float(Part[Actual]['Duration'])
                    PartialDuration = Duration / 10 #duration splitted to check multiple times

                    if all([NotesFlags[Note] for Note in Chord]) and IsMainAlive(): #check if all the notes in the chord are available (otherwise the cord wouldn't make sense)
                        PlayChord(Chord, Duration) #play the chord at full duration
                    else:
                        while not all([NotesFlags[Note] for Note in Chord]): #check if the chord is stil playable
                            Sleep(PartialDuration) #waiting the partial duration to check availability
                            Counter += 1 #increasing wasted times

                        if all([NotesFlags[Note] for Note in Chord]) and IsMainAlive(): #check if the resources are available and the chors is still playable
                            RemainingDuration = Duration - (PartialDuration * Counter) #calculate remaining duration
                            PlayChord(Chord, RemainingDuration) #play the chord at partial duration
                elif Part[Actual]['Type'] == 'Rest': #check if the element is a rest
                    Duration = float(Part[Actual]['Duration'])
                    Sleep(abs(Duration)) #wait the rest

                Actual += 1 #increase the played notes

        Sleep(5)
        print(f'{Identity()} ended')

    def PauseSong(self): #this fucntion pause the song playing
        Sleep(2) #delay to get rid of function call besides the first
        if self.Playing.is_set(): #check if the song is playing
            print(f'{Identity()} is pausing')
            self.Playing.clear() #clear the playing state
        if not self.Playing.is_set(): #check if the song is not playing
            print(f'{Identity()} is resuming')
            self.Playing.set() #set the song as playing

    def StopSong(self): #this fucntion stop the song
        if not StopFunction.locked(): #check if the fucntion has called by multiple thread
            print('Stop called')
            Sleep(1)
            self.Stop.set() #set the stop state
            self.Playing.clear() #clear the playing state
            self.PlayButton.state(['!disabled']) #enable the play button
            self.PlayButton.state(['!pressed']) #reset the play button to the default state
            ReleaseResources() #release possible hanging resources

    def Compile(self): #this function switch to compilation screen
        GenshinLyrePlayer.Raise(CompilationScreen.Name)

class CompilationScreen(TkPage):
    Name = 'Compilation'
    Font = lambda Size: ('Courier', Size) #font of the page

    def __init__(self, Parent, *args, **kwargs):
        super().__init__() #constructor of super class
        self.Songs = [Song for Song in DirList('Songs') if Song.endswith('.mid')] #mappable songs
        self.MappedSongs = [Song for Song in DirList('MappedSongs') if Song.endswith('.cmid')] #mapped and compiled song

        TopLabel = Label(self, text = 'Compile a Song', font= CompilationScreen.Font(24), bd = 10) #top label with a title for the page
        TopLabel.place(anchor= 'n', relx= 0.5, rely = 0.015, relwidth = 1, relheight=0.15) #placing the label

        self.ItemList = ListBox(self) #item list of the song
        for Index, Item in enumerate(self.Songs): #for loop for every compiled comiled song
            self.ItemList.insert(Index, Item) #indexing the song in the list
            self.ItemList.itemconfig(Index, {'bg' : '#C2C2C2'})
        self.ItemList.place(anchor= 'n', relx= 0.5, rely = 0.19, relwidth = 1, relheight = 0.46) #placing the item list

        self.ApproxValue = IntVar()
        self.ApproxValue.set(1)
        self.SingleTracks = IntVar()
        self.SingleTracks.set(0)

        self.Closest = Radio(self, text = 'Closest Approximation (A# = A, A- = A)', variable = self.ApproxValue, value = 1)
        self.Closest.place(anchor = 'nw', relx = 0.008, rely = 0.65, relheight = 0.07, relwidth = 0.6)
        self.Upper = Radio(self, text = 'Upper Approximation (A# = B, A- = A)', variable = self.ApproxValue, value = 0)
        self.Upper.place(anchor = 'nw', relx = 0.008, rely = 0.71, relheight = 0.07, relwidth = 0.6)
        self.Split = Check(self, text = 'Split MIDI into single tracks', variable = self.SingleTracks, onvalue = 1, offvalue = 0)
        self.Split.place(anchor = 'nw', relx = 0.008, rely = 0.77, relheight = 0.07, relwidth = 0.6)

        self.Compilation = Button\
        (
            self,
            text = 'Compile selected song',
            command = lambda : self.CompileSong()
        )
        self.Compilation.place(anchor = 'nw', relx = 0.615, rely = 0.66, relheight = 0.17, relwidth = 0.38)

        self.Back = Button\
        (
            self,
            text = 'Back to Home',
            command = lambda : self.TurnBack()
        )
        self.Back.place(anchor = 'nw', relx = 0.008, rely = 0.84, relheight = 0.07, relwidth = 0.988)

    def CompileSong(self):
        Song = str(self.ItemList.get('active'))
        Approximation = bool(self.ApproxValue.get())
        SplitMIDI = bool(self.SingleTracks.get())

        if Approximation:
            print('closest approximation')
            Compile(Song, True, False, SplitMIDI)
        else:
            print('upper approximation')
            Compile(Song, False, True, SplitMIDI)

    def TurnBack(self):
        GenshinLyrePlayer.Raise(Home.Name)

    def Refresh(self): #this function update the song list
        self.Songs = [Song for Song in DirList('Songs') if Song.endswith('.mid')] #check the folder for the songs
        self.ItemList.delete('0','end') #delete every item of the list
        for Index, Item in enumerate(self.Songs): #loop for every song in the folder
            self.ItemList.insert(Index, Item) #index the song in the item list
            self.ItemList.itemconfig(Index, {'bg' : '#C2C2C2'}) #background of the itemlist

class GenshinLyrePlayer(App): #class for main app
    Screens =\
    {
        CompilationScreen.Name : None,
        Home.Name : None,
    } #dictionary of all the pages

    def __init__(self):
        super().__init__() #constructor of super class
        if not Exists('Songs'):
            MakeDirs('Songs')
        if not Exists('MappedSongs'):
            MakeDirs('MappedSongs')
        try:
            self.iconphoto(True, Photo(file = 'Res/Logo.png')) #setting icon of the app
        except:
            pass

        if IsAdmin(): #checking if the user has admin rights
            HEIGHT = int(self.winfo_screenheight() * 0.3) #getting the height of screen and dividing by 3 and setting it as height of the window
            WIDTH = int(HEIGHT * 1.5) #setting the height * 1.2 as width of the window
            Sizes = str(WIDTH) + 'x' + str(HEIGHT) #converting the sizes in a string
            X = int((self.winfo_screenwidth() - WIDTH) / 2) #setting the starting x as center of the screen
            Y = int((self.winfo_screenheight() - HEIGHT) / 2) #setting the starting y as center of the screen
            Pos = '+' + str(X) + '+' + str(Y) #formatting the position
            self.geometry(Sizes + Pos) # setting size and position of the window
            self.title('Genshin Impact Lyre Autoplay') # setting the title of the window
            GenshinLyrePlayer.Screens[Home.Name] = Home(self) #initializing the home screen
            GenshinLyrePlayer.Screens[CompilationScreen.Name] = CompilationScreen(self) #initializing the compilation screen

            GenshinLyrePlayer.Raise(Home.Name)

            for Screen in GenshinLyrePlayer.Screens:
                GenshinLyrePlayer.Screens[Screen].place(anchor= 'n', relx= 0.5, rely = 0, relheight = 1, relwidth = 1)

        else: #if the user has no admin rights
            self.AlternativeStart() #show a warning to restart with admin rights

    def AlternativeStart(self): #this function is a warning to restart as admin
        self.title('Warning') #setting a different title
        Warning = Label(self, text = 'Restart this program as', font = ('Courier', 24)) #warning label first line
        WarningBottom = Label(self, text = 'Admin', font = ('Courier',24)) #warning label second line
        Warning.pack() #automatically position the first label
        WarningBottom.pack() #automatically positioning the second label
        self.update() #update of the screen (needed for position)
        X = int((self.winfo_screenwidth() - Warning.winfo_width()) / 2) #setting the starting x as center of the screen
        Y = int((self.winfo_screenheight() - Warning.winfo_height() * 2) / 2) #setting the starting y as center of the screen
        Pos = '+' + str(X) + '+' + str(Y) #formatting the position
        self.geometry(Pos) # setting size and position of the window

    def Raise(ScreenName = str()): #raising the selected screen to the top
        GenshinLyrePlayer.Screens[ScreenName].tkraise() #accessing the screen from the dictionary and raising it
        GenshinLyrePlayer.Screens[ScreenName].Refresh() #update the page for eventual changes

if __name__ == '__main__':
    Application = GenshinLyrePlayer() #app initialization
    Application.mainloop()

    Exit(0)
