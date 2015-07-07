# -- coding: utf-8 --
__author__ = 'Xplore'
 
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time
from batterywin import *
 
#CODE FOR WINDOWS BALLOON:
class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",title,200,msg))

        #Destroy & self.show_balloon(title, msg)
        time.sleep(5)#TIME PERIOD FOR BALLOON NOTIFICATION IN seconds.
        DestroyWindow(self.hwnd)
        classAtom = UnregisterClass(classAtom, hinst)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
def balloon_tip(title, msg):
    w=WindowsBalloonTip(msg, title)


#balloon_tip("hello",str(powerclass.BatteryLifePercent))
#print(powerclass.BatteryLifePercent)

#CODE FOR BATTERY ALERT

pwr = powerclass.BatteryLifePercent
ac = powerclass.ACLineStatus


while(True):
    if pwr < 20 and ac!=1:#SPECIFY THE LOWER THRESHOLD
        balloon_tip("Plug the Charger!",str(powerclass.BatteryLifePercent)+"%")
        time.sleep(100) #Do not set this below 100! , it may result in high CPU usage
    elif pwr > 80 and ac==1:#SPECIFY THE UPPER THRESHOLD
        balloon_tip("Remove the Charger!",str(powerclass.BatteryLifePercent)+"%")
        time.sleep(100) #Do not set this below 100! , it may result in high CPU usage
    del sys.modules['batterywin']
    from batterywin import *
    ac = powerclass.ACLineStatus
    pwr = powerclass.BatteryLifePercent



