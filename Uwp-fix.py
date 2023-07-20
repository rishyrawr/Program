import sys
import win32gui
import win32con
import pyautogui
from pynput.mouse import Listener, Button, Controller
from pynput import keyboard
import time

def isuwpfc():
    wd = win32gui.GetForegroundWindow()
    if win32gui.GetWindowLong(wd, win32con.GWL_STYLE) & win32con.WS_VISIBLE:
        class_name = win32gui.GetClassName(wd)
        return "ApplicationFrameWindow" in class_name
    return False

locked = False
mouseX, mouseY = 0, 0
isfc = False

def lc():
    global locked, mouseX, mouseY
    mouseX, mouseY = pyautogui.position().x, pyautogui.position().y
    locked = True
    if isfc:
        print("Locking cursor")

def uc():
    global locked
    if locked and isfc:
        pyautogui.moveTo(mouseX, mouseY)
    locked = False
    if isfc:
        print(f"Unlocking cursor")

def oc(x, y, button, pressed):
    if button == Button.right:
        if pressed:
            lc()
        else:
            uc()

mltn = Listener(oc=oc)
mltn.start()

gInterval = 0.05

running = True
def o_r(k):
    global running, gInterval
    if k == keyboard.Key.Home:
        mlistener.stop()
        running = False
        return False
    elif k == keyboard.Key.End:
        if not locked: gInterval = 0.025; lc()
        else: gInterval = 0.05; uc()

ltn = keyboard.Listener(o_r=o_r)
ltn.start()

print("""
 - เปิดโปรแกรมนี้และปล่อยให้มันอยู่ตลอด
 - กดที่ไหนก็ได้ในเกม

กดปุ่ม Home เพื่อ Unlock/lock เม้าส์ด้วยตัวเอง.
ออกโปรแกรมทันทีกดปุ่ม End
""")

wasfc = False
while running:
    isfc = isuwpfc()
    if locked and isfc:
        if not wasfc:
            print("Window focused")
            wasfc = True
        pyautogui.moveTo(mouseX, mouseY)
    if wasfc and not isfc:
        print("Lost focus")
        wasfc = False
    time.sleep(gInterval)
