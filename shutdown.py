import os


def shutdown_windows():
    os.system("shutdown /s /t 1")  # Shutdown with 1 second delay


if __name__ == "__main__":
    shutdown_windows()
