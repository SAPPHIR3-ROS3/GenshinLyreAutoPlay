from ctypes import c_ulong as ULong
from ctypes import c_ushort as UShort
from ctypes import pointer as Pointer
from ctypes import POINTER as Ptr
from ctypes import sizeof as Sizeof
from ctypes import Structure as Struct
from ctypes import Union as SUnion
from ctypes import windll as WinDLL
from time import sleep as Sleep

SendInput = WinDLL.user32.SendInput #Win32api input command

PUL = Ptr(ULong) #Pointer type


class KeyboardInput(Struct): #C Struct with necessary field to send input
    _fields_ =\
    [
        ("wVk", UShort),
        ("wScan", UShort),
        ("dwFlags", ULong),
        ("time", ULong),
        ("dwExtraInfo", PUL)
    ]

class ReqInput(SUnion): #C Struct for input request from normal to DirectX input
    _fields_ = [("ki", KeyboardInput)]


class Input(Struct): #C Struct for DirectX Input
    _fields_ =\
    [
        ("type", ULong),
        ("ii", ReqInput)
    ]

def PressKey(hexKeyCode): #this function send the input of key press
    Extra = ULong(0) #pointer of a number to fill the input
    InputRequest = ReqInput() #normal input request creation
    InputRequest.ki = KeyboardInput(0, hexKeyCode, 0x0008, 0, Pointer(Extra)) #setting the Keyboard input attribute field properly
    RealInput = Input(ULong(1), InputRequest) # input conversion
    SendInput(1, Pointer(RealInput), Sizeof(RealInput)) #sending the input


def ReleaseKey(hexKeyCode): # this function send the input of key release
    Extra = ULong(0) #pointer of a number to fill the input
    InputRequest = ReqInput() #normal input request creation
    InputRequest.ki = KeyboardInput(0, hexKeyCode, 0x0008 | 0x0002, 0, Pointer(Extra)) #setting the Keyboard input attribute field properly
    RealInput = Input(ULong(1), InputRequest) #input conversion
    SendInput(1, Pointer(RealInput), Sizeof(RealInput)) #sending the input

if __name__ == '__main__':
    while (True):
        PressKey(0x11)
        Sleep(1)
        ReleaseKey(0x11)
        Sleep(1)