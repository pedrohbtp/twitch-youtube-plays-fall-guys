# For Windows
# http://stackoverflow.com/questions/1823762/sendkeys-for-python-3-1-on-windows
# https://stackoverflow.com/a/38888131

import win32api
import win32con
import win32gui
import time, sys

keyDelay =0.1
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
keymap = {
    "up": 0x57, #w
    "down": 0x53, #s
    "left": 0x41, #a
    "right": 0x44, #d
    "grab": win32con.VK_LSHIFT,
    "jump": win32con.VK_SPACE,
    "dive": win32con.VK_LCONTROL,
    "esc": win32con.VK_ESCAPE
}

def press_for_seconds(button, hold_seconds):
    ''' holds a button for the seconds specified
    '''
    start_time = time.time()
    while time.time() - start_time < hold_seconds:
        send_key(button)

# this way has to keep window in focus
def send_key(button):
    ''' Sends the button press to the screen in focus
    '''
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-keybd_event?redirectedfrom=MSDN
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

    # tests for input validity
    if len(sys.argv) < 3:
        print('Invalid number of arguments!')
        print('Syntax: python key.py <window_title> <action> <optional_hold_time_in_secons>')
        exit(0)

    windowName = sys.argv[1]
    key = sys.argv[2]
    try:
        hold_time_seconds = float(sys.argv[3]) if len(sys.argv) >=4 else None
    except ValueError as e:
        # put = -1 to exit on the next if
        hold_time_seconds = -1


    # limits the hold time to 5 seconds
    if hold_time_seconds!= None and(  hold_time_seconds > 5 or hold_time_seconds < 1):
        print('hold time must be within 1 and 5')
        exit(0)

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
    if hold_time_seconds == None:
        send_key(key)
    else:
        press_for_seconds(key, hold_time_seconds)
