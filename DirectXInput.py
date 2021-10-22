from ctypes import c_long as Long
from ctypes import c_short as Short
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

class KeyboardInput(Struct): #C Struct with necessary field to send input as Keyboard
    _fields_ = \
    [
        ("wVk", UShort),
        ("wScan", UShort),
        ("dwFlags", ULong),
        ("time", ULong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(Struct):#C Struct with necessary field to send input as hardware
    _fields_ =\
    [
        ("uMsg", ULong),
        ("wParamL", Short),
        ("wParamH", UShort)
    ]

class MouseInput(Struct): #C Struct with necessary field to send input as mouse #this class is necessary otherwise input won't be registered as valid
    _fields_ =\
    [
        ("dx", Long),
        ("dy", Long),
        ("mouseData", ULong),
        ("dwFlags", ULong),
        ("time", ULong),
        ("dwExtraInfo", PUL)
    ]

class ReqInput(SUnion): #C Struct for input request from normal to DirectX input
    _fields_ =\
    [
        ("InputKeyboard", KeyboardInput),
        ("InputMouse", MouseInput),
        ("InputHardWare", HardwareInput)
    ]

class Input(Struct): #C Struct for DirectX Input
    _fields_ =\
    [
        ("type", ULong),
        ("RequestInput", ReqInput)
    ]

def PressKey(HexKeyCode): #this function send the input of key press
    FillInput = ULong(0) #pointer of a number to fill the input
    InputRequest = ReqInput() #normal input request creation
    InputRequest.InputKeyboard = KeyboardInput(0, HexKeyCode, 0x0008, 0, Pointer(FillInput)) #setting the Keyboard input attribute field properly
    DirectInput = Input(ULong(1), InputRequest) # input conversion
    SendInput(1, Pointer(DirectInput), Sizeof(DirectInput)) #sending the input for pressing the key


def ReleaseKey(HexKeyCode): #this function send the input of key release
    FillInput = ULong(0) #pointer of a number to fill the input
    InputRequest = ReqInput() #normal input request creation
    InputRequest.InputKeyboard = KeyboardInput(0, HexKeyCode, 0x0008 | 0x0002, 0, Pointer(FillInput)) #setting the Keyboard input attribute field properly
    DirectInput = Input(ULong(1), InputRequest) # input conversion
    SendInput(1, Pointer(DirectInput), Sizeof(DirectInput)) #sending the input for releasing the key

if __name__ == '__main__':
    for i in range(3):
        print(3 - i)
        Sleep(1)

    for i in range(3):
        PressKey(0x11)
        print('key pressed')
        Sleep(1)
        ReleaseKey(0x11)
        print('key released')
        Sleep(1)
