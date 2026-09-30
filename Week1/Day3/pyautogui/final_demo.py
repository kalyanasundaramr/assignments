import pyautogui
import time
from datetime import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

print("Step #1: Starting the demo in 5 seconds...")
time.sleep(5)

print("Step #2: Launch the run dialog box using the Win+R hotkey combination.")
pyautogui.hotkey('win', 'r')  # Open the Run dialog
time.sleep(1)

print("Step #3: Type the URL to launch the Chrome browser.")
pyautogui.typewrite('https://www.accuweather.com/en/in/chennai/206671/hourly-weather-forecast/206671')  # Type the URL
time.sleep(1)

print("Step #4: Press Enter to launch the browser.")
pyautogui.press('enter')  # Press Enter to launch the browser

print("Step #5: Wait for the browser to load the page.")    
time.sleep(5)

print("Step #6: Take a screenshot of the browser window.")
screenshot = pyautogui.screenshot() 
screenshot.save('browser_screenshot.png')  # Save the screenshot as 'browser_screenshot.png'   
print("Step #7: Screenshot saved as 'browser_screenshot.png'.") 

print("Step #8: copy the full data from the browser window.")
pyautogui.hotkey('ctrl', 'a')  # Select all text in the browser window
time.sleep(1)

print("Step #9: Copy the selected data to the clipboard.")
pyautogui.hotkey('ctrl', 'c')  # Copy the selected data to the clipboard
time.sleep(1)

print("Step #10: Open a text editor (Notepad) to paste the copied data.")
pyautogui.hotkey('win', 'r')  # Open the Run dialog again   

print ("Step #11: Type 'notepad' to launch Notepad.")
pyautogui.typewrite('notepad')  # Type 'notepad' to launch Notepad
time.sleep(1)

print("Step #12: Press Enter to launch Notepad.")
pyautogui.press('enter')  # Press Enter to launch Notepad

print("Step #13: Wait for Notepad to open.")
time.sleep(2)   

print("Step #14: Paste the copied data into Notepad.")
pyautogui.hotkey('ctrl', 'v')  # Paste the copied data into Notepad
time.sleep(1)

print("Step #15: Save the Notepad file with a timestamped filename.")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate a timestamp for the filename
filename = f"weather_data_{timestamp}.txt"  # Create a filename with the timestamp

print(f"Step #16: Saving the Notepad file as '{filename}'.")
pyautogui.hotkey('ctrl', 's')  # Open the Save dialog in Notepad
time.sleep(1)

print(f"Step #17: Type the filename '{filename}' in the Save dialog.")
pyautogui.typewrite(filename)  # Type the filename in the Save dialog
time.sleep(1)

print("Step #18: Press Enter to save the file.")
pyautogui.press('enter')  # Press Enter to save the file

print(f"Step #19: File saved as '{filename}'. Demo completed successfully.")

print("Step #20: Closing Notepad.")
pyautogui.hotkey('alt', 'f4')  # Close Notepad

print("Step #21: Closing the browser.")
pyautogui.hotkey('alt', 'f4')  # Close the browser 