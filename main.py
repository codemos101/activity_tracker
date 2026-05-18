from pynput import keyboard

def on_press(key):
    try:
        print(f"Key pressed: {key.char}")
    except:
        print(f"Special key pressed: {key}")

    # Stop program if ESC is pressed
    if key == keyboard.Key.esc:
        print("Stopping tracker...")
        return False

listener = keyboard.Listener(on_press=on_press)

listener.start()
listener.join()