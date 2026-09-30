import pyautogui
import pyperclip
import time
import os
import re
from datetime import datetime


# ---------------------------------------------------------
# 1. SETTINGS
# ---------------------------------------------------------

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# Current date and time

# Folder where this Python file is located
folder = os.path.dirname(os.path.abspath(__file__))

today = datetime.now().strftime("%Y-%m-%d")
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

excel_file = os.path.join(
    folder,
    f"daily_report_{today}.xlsx"
)

screenshot_file = os.path.join(
    folder, 
    f"daily_report_{today}.png"
)

# ---------------------------------------------------------
# 2. START
# ---------------------------------------------------------

print("Starting Daily Report Bot...")
print("Please wait 5 seconds...")

time.sleep(5)


# ---------------------------------------------------------
# 3. OPEN CHROME
# ---------------------------------------------------------

print("Opening Chrome...")

pyautogui.hotkey("win", "r")
time.sleep(1)

pyautogui.write(
    "https://wttr.in/Chennai?format=3",
    interval=0.02
)

pyautogui.press("enter")

print("Waiting for weather page...")
time.sleep(7)


# ---------------------------------------------------------
# 4. COPY WEATHER DATA FROM BROWSER
# ---------------------------------------------------------

print("Copying weather information...")

# Select everything on the webpage
pyautogui.hotkey("ctrl", "a")
time.sleep(1)

# Copy selected text
pyautogui.hotkey("ctrl", "c")
time.sleep(1)

# Read copied text
weather_text = pyperclip.paste()

print("Weather information:")
print(weather_text)


# Extract temperature
temperature_match = re.search(
    r"[+-]?\d+\s*°?C",
    weather_text
)

if temperature_match:
    temperature = temperature_match.group()
else:
    temperature = "Temperature not found"

print("Temperature:", temperature)


# ---------------------------------------------------------
# 5. OPEN XLSX OPEN PLUS
# ---------------------------------------------------------

print("Opening XLSX Open PLUS...")

pyautogui.press("win")
time.sleep(2)

pyautogui.write(
    "XLSX Open PLUS",
    interval=0.05
)

time.sleep(2)

pyautogui.press("enter")

print("Waiting for XLSX Open PLUS...")
time.sleep(8)


# ---------------------------------------------------------
# 6. CLOSE POSSIBLE POPUP
# ---------------------------------------------------------

print("Closing popup if present...")

pyautogui.press("esc")
time.sleep(2)

# If the popup exists at this location, close it
pyautogui.click(1344, 349)
time.sleep(2)


# ---------------------------------------------------------
# 7. CREATE NEW WORKBOOK
# ---------------------------------------------------------

print("Using the spreadsheet...")

time.sleep(5)

# Click spreadsheet area
pyautogui.click(300, 250)

# Go to first cell
pyautogui.hotkey("ctrl", "home")

time.sleep(1)


# ---------------------------------------------------------
# 8. ENTER HEADER ROW
# ---------------------------------------------------------

print("Entering headers...")

headers = (
    "Date & Time\t"
    "Temperature\t"
    "Comment"
)

pyperclip.copy(headers)

pyautogui.hotkey("ctrl", "v")

time.sleep(2)

pyautogui.press("enter")


# ---------------------------------------------------------
# 9. ENTER DATA ROW
# ---------------------------------------------------------

print("Entering report data...")

comment = "Weather information fetched automatically"

data = (
    f"{date_time}\t"
    f"{temperature}\t"
    f"{comment}"
)

pyperclip.copy(data)

pyautogui.hotkey("ctrl", "v")

time.sleep(3)


# ---------------------------------------------------------
# 10. SAVE XLSX FILE
# ---------------------------------------------------------

print("Saving Excel file...")

pyautogui.hotkey("ctrl", "shift", "s")

time.sleep(4)

# Enter file path
pyautogui.hotkey("ctrl", "a")

pyautogui.write(
    excel_file,
    interval=0.01
)

pyautogui.press("enter")

time.sleep(5)

# Handle possible confirmation
pyautogui.press("enter")

time.sleep(3)


# ---------------------------------------------------------
# 11. CHECK FILE
# ---------------------------------------------------------

if os.path.exists(excel_file):

    print("Excel file saved successfully:")
    print(excel_file)

else:

    print("WARNING: Excel file was not found.")


# ---------------------------------------------------------
# 12. TAKE SCREENSHOT
# ---------------------------------------------------------

print("Taking screenshot...")

# Click spreadsheet area
pyautogui.click(500, 400)

time.sleep(2)

pyautogui.screenshot(screenshot_file)

print("Screenshot saved:")
print(screenshot_file)


# ---------------------------------------------------------
# 13. CLOSE XLSX OPEN PLUS
# ---------------------------------------------------------

print("Closing XLSX Open PLUS...")

pyautogui.hotkey("alt", "f4")
time.sleep(3)

# If a save confirmation appears
pyautogui.press("right")
pyautogui.press("enter")

time.sleep(3)


# ---------------------------------------------------------
# 14. CLOSE CHROME
# ---------------------------------------------------------

print("Closing Chrome...")

pyautogui.hotkey("alt", "f4")
time.sleep(3)


# ---------------------------------------------------------
# 15. FINISHED
# ---------------------------------------------------------

print()
print("========================================")
print("DAILY REPORT COMPLETED")
print("========================================")

print("Date & Time :", date_time)
print("Temperature :", temperature)
print("Excel File  :", excel_file)
print("Screenshot  :", screenshot_file)

print()
print("Browser and spreadsheet closed.")
print("Done!")