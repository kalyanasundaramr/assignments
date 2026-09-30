from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=["--disable-http2"]
    )

    page = browser.new_page()

    page.goto(
        "https://www.accuweather.com/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    text = page.locator("body").inner_text()

    with open("weather.txt", "w", encoding="utf-8") as file:
        file.write(text)

    browser.close()

print("Weather information saved successfully!")