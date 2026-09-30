import pyautogui
import time

time.sleep(3)  # Wait for 3 seconds before starting the mouse operations

#mouse operations
pyautogui.moveTo(100, 100, duration=1)  # Move the mouse to (100, 100) over 1 second

time.sleep(1)  # Wait for 1 seconds before starting the mouse operations

pyautogui.click(200,200)  # Click the mouse at the (100,100) position  

time.sleep(1)  # Wait for 1 seconds before starting the mouse operations

pyautogui.rightClick(300,300)  # Right click the mouse at the (100,100) position

time.sleep(1)  # Wait for 1 seconds before starting the mouse operations

pyautogui.middleClick(100,100)  # Middle click the mouse at the (100,100) position

time.sleep(1)  # Wait for 1 seconds before starting the mouse operations

pyautogui.leftClick(200,200)  # Left click the mouse at the (100,100) position

time.sleep(1)  # Wait for 1 seconds before starting the mouse operations

#pyautogui.doubleClick(100,100)  # Double click the mouse at the (100,100) position

#pyautogui.dragTo(200, 200, duration=1)  # Drag the mouse to (200, 200) over 1 second

pyautogui.scroll(10)  # Scroll up 10 units
