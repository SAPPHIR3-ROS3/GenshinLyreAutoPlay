from ctypes import c_ulong as ULong
from ctypes import c_ushort as UShort
from ctypes import pointer as Pointer
from ctypes import POINTER as Ptr
from ctypes import sizeof as Sizeof
from ctypes import Structure as Struct
from ctypes import Union as SUnion
from ctypes import windll as WinDLL
from time import sleep as Sleep

SendInput = WinDLL.user32.SendInput

PUL = Ptr(ULong)


class KeyBdInput(Struct):
    _fields_ =\
    [
        ("wVk", UShort),
        ("wScan", UShort),
        ("dwFlags", ULong),
        ("time", ULong),
        ("dwExtraInfo", PUL)
    ]

class ReqInput(SUnion):
    _fields_ = [("ki", KeyBdInput)]


class Input(Struct):
    _fields_ =\
    [
        ("type", ULong),
        ("ii", ReqInput)
    ]

def PressKey(hexKeyCode):
    extra = ULong(0)
    InputRequest = ReqInput()
    InputRequest.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, Pointer(extra))
    RealInput = Input(ULong(1), InputRequest)
    SendInput(1, Pointer(RealInput), Sizeof(RealInput))


def ReleaseKey(hexKeyCode):
    extra = ULong(0)
    InputRequest = ReqInput()
    InputRequest.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, Pointer(extra))
    RealInput = Input(ULong(1), InputRequest)
    SendInput(1, Pointer(RealInput), Sizeof(RealInput))

if __name__ == '__main__':
    while (True):
        PressKey(0x11)
        Sleep(1)
        ReleaseKey(0x11)
        Sleep(1)