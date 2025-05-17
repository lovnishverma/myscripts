import pyautogui
import psutil
import os
import random
import time

pyautogui.FAILSAFE = True  # Move mouse to top-left to abort

def funny_mouse_movements(duration=10):
    print("😈 Taking over your mouse...")
    start_time = time.time()
    screen_width, screen_height = pyautogui.size()

    while time.time() - start_time < duration:
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=0.3)
        if random.random() > 0.7:
            pyautogui.click()
        time.sleep(0.1)

    print("🖱️ Mouse chaos complete.")

def close_vscode():
    closed = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'code' in proc.info['name'].lower():  # Matches VS Code
                os.kill(proc.info['pid'], 9)
                closed = True
                print("💥 VS Code has been closed. Real devs use Vim.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not closed:
        print("❗VS Code was not running... you're safe... for now 😈")

def main():
    print("🎭 Welcome to the Mouse Mayhem Script!")
    time.sleep(2)
    funny_mouse_movements(duration=7)
    print("🔍 Searching for VS Code to close...")
    time.sleep(2)
    close_vscode()
    print("👋 Done. Hope you saved your files!")

if __name__ == "__main__":
    main()
