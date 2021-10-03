  
#This script saves the image of the region 660,350,600,400 as savedimage.png in the path "C:\Users\Antec\Desktop\Tutorial\savedimage.png"

import pyautogui
x,y = pyautogui.size()

im1 = pyautogui.screenshot(region=(0,0, x-500, y-200))
im1.save(r"C:\Users\aleke\OneDrive\Desktop\Tetris Bot\savedimage.png")
