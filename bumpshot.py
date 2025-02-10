import mss
#import pystray
#from pystray import Menu, MenuItem
from PIL import Image, ImageGrab
from datetime import datetime

import pygetwindow as gw
import keyboard
import pyautogui
import os, sys, time

from infi.systray import SysTrayIcon

import configparser
Config = configparser.ConfigParser()
Config.read(os.getcwd() + "\\myconfig.ini")

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
path = desktop + "\\ScreenShots"


def make_directory():
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    
def exit_action(icon):
    #icon.stop()
    os._exit(1)


def capture_screenshot():

    # isExist = os.path.exists(path)
    # if not isExist:
    #     os.makedirs(path)

    with mss.mss() as sct:

        make_directory()

        fmt = '%Y-%m-%d_%H.%M.%S'
        now = datetime.now()
        current_time = now.strftime(fmt)

        active_window = gw.getActiveWindow()
        if active_window == None or active_window == False:
            sct_img = sct.grab(monitor[1])
        else:
            monitor = {
                "top": active_window.top,
                "left": active_window.left,
                "width": active_window.width,
                "height": active_window.height
                }
            sct_img = sct.grab(monitor)

        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.save(desktop + "\\ScreenShots\\" + current_time + "-screenshot.png", "PNG")

        time.sleep(0.3)


def capture_area_screenshot():

    # isExist = os.path.exists(path)
    # if not isExist:
    #     os.makedirs(path)

    make_directory()

    left_x, left_y = pyautogui.position()
    while True:

        if keyboard.is_pressed("esc"):
            break
        
        
        screenarea2 = Config.get('DEFAULT', 'ScreenArea2')
        if keyboard.is_pressed(str(screenarea2)):
            right_x, right_y = pyautogui.position()

            fmt = '%Y-%m-%d_%H.%M.%S'
            now = datetime.now()
            current_time = now.strftime(fmt)

            img_path = desktop + "\\ScreenShots\\" + current_time + "-screenshot.png"
            img = ImageGrab.grab(bbox=(left_x, left_y, right_x, right_y))
            img.save(img_path, "PNG")
            
            time.sleep(0.3)
            break
            
        
if __name__ == '__main__':
    screenshot = Config.get('DEFAULT', 'Screenshot')
    screenarea1 = Config.get('DEFAULT', 'ScreenArea1')

    keyboard.add_hotkey(str(screenshot), capture_screenshot)
    keyboard.add_hotkey(str(screenarea1), capture_area_screenshot)
    
    # image = Image.open("icon.ico")

    # icon = pystray.Icon('Bumpshot')
    # icon.menu = Menu(
    #     MenuItem('Close Bumpshot', lambda : exit_action(icon)),
    # )
    # icon.icon = image
    # icon.title = 'Bumpshot 1.0.7'
    # icon.run()

    menu_options = ""
    icon = SysTrayIcon("icon.ico", "Bumpshot 1.0.8", menu_options, on_quit=exit_action)
    icon.start()
