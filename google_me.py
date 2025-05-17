import pyautogui
import time
import webbrowser


def search_google(query):
    # Open default browser to google.com
    webbrowser.open("https://www.google.com")

    # Wait for browser and page to load
    time.sleep(5)  # Adjust if needed

    # Click the search bar (approximate coordinates)
    # Alternatively, just start typing if search bar is auto-focused on page load
    # So we skip clicking and just type directly

    # Type the query with a little delay between keys
    pyautogui.write(query, interval=0.1)

    # Press Enter to search
    pyautogui.press('enter')


if __name__ == "__main__":
    search_google("Lovnish Verma")
