import random
import time
import os
import sys

# ANSI escape sequences for colors
colors = [
    "\033[91m",  # Red
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[94m",  # Blue
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
]

reset = "\033[0m"

try:
    while True:
        # Generate a random line of random colored characters
        line = "".join(random.choice(colors) +
                       chr(random.randint(33, 126)) + reset for _ in range(80))
        print(line)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nExiting... Stay safe! 👾")
    sys.exit(0)
