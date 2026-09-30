import asyncio
import json
import random
import os
from datetime import datetime

from playwright.async_api import async_playwright
from openpyxl import load_workbook, Workbook


# =========================================================
# SETTINGS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONTACTS_FILE = os.path.join(
    BASE_DIR,
    "contacts.xlsx"
)

today = datetime.now().strftime("%Y-%m-%d")

JSON_REPORT = os.path.join(
    BASE_DIR,
    f"whatsapp_report_{today}.json"
)

EXCEL_REPORT = os.path.join(
    BASE_DIR,
    f"whatsapp_report_{today}.xlsx"
)

SCREENSHOT_DIR = os.path.join(
    BASE_DIR,
    "whatsapp_screenshots"
)

PROFILE_DIR = os.path.join(
    BASE_DIR,
    "whatsapp_profile"
)

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# =========================================================
# RANDOM HUMAN-LIKE DELAY
# =========================================================

async def human_delay():
    delay = random.uniform(2, 5)

    print(f"Waiting {delay:.1f} seconds...")

    await asyncio.sleep(delay)


# =========================================================
# READ CONTACTS FROM contacts.xlsx
# =========================================================

def read_contacts():

    print("Reading contacts.xlsx...")

    if not os.path.exists(CONTACTS_FILE):

        print("ERROR: contacts.xlsx not found.")

        print("Expected location:")
        print(CONTACTS_FILE)

        return []

    workbook = load_workbook(
        CONTACTS_FILE,
        data_only=True
    )

    sheet = workbook.active

    contacts = []

    # Skip header row
    for row in sheet.iter_rows(
        min_row=2,
        values_only=True
    ):

        name = row[0]
        phone = row[1]
        message = row[2]

        if not name or not phone:
            continue

        # Convert phone to string
        phone = str(phone).strip()

        # Default message
        if not message:
            message = "Hello {name}, this is your daily update."

        contacts.append({
            "name": str(name).strip(),
            "phone": phone,
            "message": str(message).strip()
        })

    workbook.close()

    print(f"Found {len(contacts)} contacts.")

    return contacts


# =========================================================
# SAVE JSON REPORT
# =========================================================

def save_json_report(results):

    with open(
        JSON_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("JSON report saved.")


# =========================================================
# SAVE EXCEL REPORT
# =========================================================

def save_excel_report(results):

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "WhatsApp Report"

    # Header
    sheet.append([
        "Name",
        "Phone",
        "Message",
        "Status",
        "Last 3 Messages",
        "Screenshot",
        "Time"
    ])

    # Data
    for result in results:

        last_messages = "\n".join(
            result.get(
                "last_3_messages",
                []
            )
        )

        sheet.append([
            result.get("name", ""),
            result.get("phone", ""),
            result.get("message", ""),
            result.get("status", ""),
            last_messages,
            result.get("screenshot", ""),
            result.get("time", "")
        ])

    workbook.save(EXCEL_REPORT)


# =========================================================
# FIND WHATSAPP SEARCH BOX
# =========================================================

async def find_search_box(page):

    # First try the accessible name visible
    # in your WhatsApp screenshot.

    try:

        search_box = page.get_by_role(
            "textbox",
            name="Search or start a new chat"
        )

        await search_box.wait_for(
            state="visible",
            timeout=10000
        )

        return search_box

    except Exception:
        pass

    # Fallback
    try:

        search_box = page.locator(
            'div[contenteditable="true"]'
        ).first

        await search_box.wait_for(
            state="visible",
            timeout=10000
        )

        return search_box

    except Exception:

        return None


# =========================================================
# FIND MESSAGE BOX
# =========================================================

async def find_message_box(page):

    # First try accessible name
    try:

        message_box = page.get_by_role(
            "textbox",
            name="Type a message"
        )

        await message_box.wait_for(
            state="visible",
            timeout=10000
        )

        return message_box

    except Exception:
        pass

    # Fallback: message box normally exists inside footer
    try:

        message_box = page.locator(
            'footer div[contenteditable="true"]'
        )

        await message_box.wait_for(
            state="visible",
            timeout=10000
        )

        return message_box

    except Exception:

        return None


# =========================================================
# MAIN PROGRAM
# =========================================================

async def main():

    # -----------------------------------------------------
    # READ CONTACTS
    # -----------------------------------------------------

    contacts = read_contacts()

    if not contacts:

        print("No contacts to process.")

        return

    results = []

    # -----------------------------------------------------
    # OPEN PLAYWRIGHT
    # -----------------------------------------------------

    async with async_playwright() as p:

        print()
        print("Opening WhatsApp Web...")

        browser = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False
        )

        if browser.pages:

            page = browser.pages[0]

        else:

            page = await browser.new_page()

        # -------------------------------------------------
        # OPEN WHATSAPP
        # -------------------------------------------------

        await page.goto(
            "https://web.whatsapp.com/",
            wait_until="domcontentloaded"
        )

        print()
        print("========================================")
        print("WHATSAPP WEB")
        print("========================================")
        print()
        print("If QR code appears, scan it manually.")
        print("Waiting for WhatsApp Web...")
        print()

        # -------------------------------------------------
        # WAIT FOR SEARCH BOX
        # -------------------------------------------------

        search_box = None

        try:

            # First wait for page
            await page.wait_for_timeout(5000)

            search_box = await find_search_box(page)

            if search_box is None:

                print(
                    "Search box not found yet."
                )

                print(
                    "Waiting for manual QR login..."
                )

                # Wait up to 3 minutes
                for i in range(60):

                    await page.wait_for_timeout(3000)

                    search_box = await find_search_box(
                        page
                    )

                    if search_box is not None:

                        break

                    print(
                        f"Waiting for WhatsApp login "
                        f"({i + 1}/60)..."
                    )

            if search_box is None:

                raise Exception(
                    "WhatsApp search box was not found."
                )

            print()
            print("WhatsApp Web is ready.")
            print()

        except Exception as error:

            print()
            print(
                "ERROR: WhatsApp Web did not become ready."
            )

            print(
                "Details:",
                str(error)
            )

            error_screenshot = os.path.join(
                SCREENSHOT_DIR,
                "whatsapp_load_error.png"
            )

            await page.screenshot(
                path=error_screenshot
            )

            print(
                "Screenshot saved:",
                error_screenshot
            )

            await browser.close()

            return

        # -------------------------------------------------
        # PROCESS CONTACTS
        # -------------------------------------------------

        for contact in contacts:

            name = contact["name"]
            phone = contact["phone"]
            template = contact["message"]

            print()
            print("========================================")
            print(f"Processing: {name}")
            print(f"Phone: {phone}")
            print("========================================")

            result = {

                "name": name,

                "phone": phone,

                "message": "",

                "status": "Failed",

                "last_3_messages": [],

                "screenshot": "",

                "time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            try:

                # =========================================
                # SEARCH CONTACT
                # =========================================

                print("Searching contact...")

                search_box = await find_search_box(
                    page
                )

                if search_box is None:

                    raise Exception(
                        "Search box not found."
                    )

                await search_box.click()

                # Clear search
                await page.keyboard.press(
                    "Control+A"
                )

                await page.keyboard.press(
                    "Backspace"
                )

                # Search phone number
                await search_box.fill(
                    phone
                )

                await human_delay()

                # =========================================
                # OPEN SEARCH RESULT
                # =========================================

                print(
                    "Opening search result..."
                )

                await page.keyboard.press(
                    "Enter"
                )

                await human_delay()

                # =========================================
                # FIND MESSAGE BOX
                # =========================================

                print(
                    "Looking for message box..."
                )

                message_box = await find_message_box(
                    page
                )

                if message_box is None:

                    raise Exception(
                        f"Could not open chat for {name}"
                    )

                print(
                    "Message box found."
                )

                # =========================================
                # PERSONALIZE MESSAGE
                # =========================================

                message = template.replace(
                    "{name}",
                    name
                )

                result["message"] = message

                print()
                print("Message:")
                print(message)
                print()

                # =========================================
                # SEND MESSAGE
                # =========================================

                print(
                    f"Sending message to {name}..."
                )

                await message_box.click()

                await message_box.fill(
                    message
                )

                await human_delay()

                await page.keyboard.press(
                    "Enter"
                )

                # Wait for message to be sent
                await page.wait_for_timeout(
                    3000
                )

                print(
                    "Message sent."
                )

                # =========================================
                # SCREENSHOT
                # =========================================

                safe_name = (
                    name
                    .replace("/", "_")
                    .replace("\\", "_")
                    .replace(" ", "_")
                )

                screenshot_file = os.path.join(
                    SCREENSHOT_DIR,
                    f"{safe_name}_{today}.png"
                )

                await page.screenshot(
                    path=screenshot_file
                )

                result["screenshot"] = (
                    screenshot_file
                )

                print(
                    "Screenshot saved:"
                )

                print(
                    screenshot_file
                )

                # =========================================
                # EXTRACT LAST 3 MESSAGES
                # =========================================

                print(
                    "Extracting last 3 messages..."
                )

                await page.wait_for_timeout(
                    2000
                )

                # WhatsApp message containers
                messages = page.locator(
                    'div.message-in, '
                    'div.message-out'
                )

                message_count = (
                    await messages.count()
                )

                last_messages = []

                start = max(
                    0,
                    message_count - 3
                )

                for i in range(
                    start,
                    message_count
                ):

                    try:

                        message_element = (
                            messages.nth(i)
                        )

                        text = await (
                            message_element.inner_text()
                        )

                        text = text.strip()

                        if text:

                            last_messages.append(
                                text
                            )

                    except Exception:

                        pass

                result["last_3_messages"] = (
                    last_messages
                )

                print(
                    "Last 3 messages:"
                )

                for msg in last_messages:

                    print(
                        "-",
                        msg
                    )

                # =========================================
                # SUCCESS
                # =========================================

                result["status"] = "Sent"

                print()
                print(
                    f"SUCCESS: {name}"
                )

            except Exception as error:

                # =========================================
                # ERROR HANDLING
                # =========================================

                print()
                print(
                    f"ERROR processing {name}"
                )

                print(
                    "Details:",
                    str(error)
                )

                result["status"] = (
                    "Failed: " + str(error)
                )

            # Add result
            results.append(result)

            # Save reports after every contact
            save_json_report(results)
            save_excel_report(results)

            # Wait before next contact
            print(
                "Waiting before next contact..."
            )

            await human_delay()

        # -------------------------------------------------
        # CLOSE BROWSER
        # -------------------------------------------------

        print()
        print(
            "All contacts have been processed."
        )

        print(
            "Closing WhatsApp Web..."
        )

        await browser.close()

    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    print()
    print("========================================")
    print("WHATSAPP AUTOMATION COMPLETED")
    print("========================================")

    print()
    print("JSON report:")
    print(JSON_REPORT)

    print()
    print("Excel report:")
    print(EXCEL_REPORT)

    print()
    print("Screenshots:")
    print(SCREENSHOT_DIR)

    print()
    print("Done!")


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())