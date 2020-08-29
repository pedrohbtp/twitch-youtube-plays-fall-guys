# For Windows
# http://stackoverflow.com/questions/1823762/sendkeys-for-python-3-1-on-windows
# https://stackoverflow.com/a/38888131

import win32api
import win32con
import win32gui
import time, sys

keyDelay = 0.1
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
keymap = {
    "up": win32con.VK_UP,
    "down": win32con.VK_DOWN,
    "left": win32con.VK_LEFT,
    "right": win32con.VK_RIGHT,
    "grab": win32con.VK_LSHIFT,
    "jump": win32con.VK_SPACE,
    "dive": win32con.VK_LCONTROL
}

# this way has to keep window in focus
def sendKey(button):
    ''' Sends the button press to the screen in focus
    '''
    win32api.keybd_event(keymap[button], 0, 0, 0)
    time.sleep(keyDelay)
    win32api.keybd_event(keymap[button], 0, win32con.KEYEVENTF_KEYUP, 0)

def SimpleWindowCheck(windowName):
    ''' Tries to find window by name
    '''
    window = None
    try:
        window = win32gui.FindWindow(windowName, None)
    except win32gui.error:
        try: 
            window = win32gui.FindWindow(None, windowName)
        except win32gui.error:
            return False
        else:
            return window
    else:
        return window

def enumHandler(hwnd, extra):
    ''' Function used to append to a list all 
    the windows that have the configured windowName present
    hwnd: handlwer passed automatically by win32gui.EnumWindows
    extra: dictionary like { 'return_list': list, 'window_name': str}
    '''
    if extra['window_name'].lower() in win32gui.GetWindowText(hwnd).lower():
        extra['return_list'].append({'screen_code': hwnd, 'screen_title': win32gui.GetWindowText(hwnd)})

if __name__ == "__main__":
    windowName = sys.argv[1]
    key = sys.argv[2]

    winId = SimpleWindowCheck(windowName)
    # winId = None

    if not (winId):
        windowList = []
        # gets the windows that contain the string in windowName
        win32gui.EnumWindows(enumHandler, { 'return_list': windowList, 'window_name': windowName})
        # only the first id, may need to try the others
        winId = windowList[0]['screen_code']

        # can check with this
        for window in windowList:
            hwndChild = win32gui.GetWindow(window['screen_code'], win32con.GW_CHILD)
            # print("window title/id/child id: ", win32gui.GetWindowText(hwnd), "/", hwnd, "/", hwndChild)

    win32gui.ShowWindow(winId, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(winId)
    sendKey(key)