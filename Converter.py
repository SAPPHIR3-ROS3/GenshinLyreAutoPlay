from ctypes import windll as WinDLL
from DirectXInput import PressKey
from DirectXInput import ReleaseKey
from tkinter import Label as Label
from tkinter import Tk as App
from time import sleep as Sleep

Notes=\
{
    'C3' : 'q', 'D3' : 'w', 'E3' : 'e', 'F3' : 'r', 'G3' : 't', 'A3' : 'y', 'B3' : 'u',
    'C2' : 'a', 'D2' : 's', 'E2' : 'd', 'F2' : 'f', 'G2' : 'g', 'A2' : 'h', 'B2' : 'j',
    'C1' : 'z', 'D1' : 'x', 'E1' : 'c', 'F1' : 'v', 'G1' : 'b', 'A1' : 'n', 'B1' : 'm',
} #Notes/Keyboard Mapping

VK_CODE =\
{
    'q':0x51, 'w':0x57, 'e':0x45, 'r':0x52, 't':0x54, 'y':0x59, 'u':0x55,
    'a':0x41, 's':0x53, 'd':0x44,  'f':0x46, 'g':0x47, 'h':0x48, 'j':0x4A,
    'z':0x5A, 'x':0x58, 'c':0x43,'v':0x56, 'b':0x42, 'n':0x4E, 'm':0x4D,
} #Keyboard/DirectX Mapping

def IsAdmin(): #this function check if the script as Admin Priviledges
    try:
        return WinDLL.shell32.IsUserAnAdmin() #attempt to use shell as Admin
    except:
        return False # if the user is not admin an exception will be thrown and catched

if __name__ == '__main__':
    Application = App() #app initialization

    if IsAdmin(): #check of Admin Priviledges
        Application.title('GenshinImpactLyreAutoplay')
        Application.geometry('+800+300')
    else:
        Application.title('Warning')
        Application.geometry('+800+300')
        Warning = Label(Application, text = 'Restart this program with', font = ('Courier', 24))
        WarningBottom = Label(Application, text = 'Admin Proviledges', font = ('Courier',24))
        Warning.pack()
        WarningBottom.pack()
    Application.mainloop() 
