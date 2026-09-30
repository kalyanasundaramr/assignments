import pyautogui
import time
import pyscreeze

print('Switch to a text editor within 10 seconds; do not leave focus on this terminal.')
time.sleep(10)

pyautogui.typewrite('Hello World!', interval=0.25)  # Type 'Hello World!' with a quarter-second pause in between each key

#hotkey operations

pyautogui.hotkey('ctrl', 'c')  # Press the Ctrl+C hotkey combination


pyautogui.hotkey('ctrl', 's')  # Press the Ctrl+S hotkey combination


#single key operations
pyautogui.press('enter')

screenshot = pyautogui.screenshot()
screenshot.save('final_screenshot.png')  # Save the screenshot as 'final_screenshot.png'Hello World!
