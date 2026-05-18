tracker app project :
phase one :
implementation of key presses using pynput for keyboard mouse listening
psutil system activity tracking later

step 1:
create a new environment and activate environment :
* means code // means comment

*conda create -n tracker python=3.11
//press y for yes
* conda activate tracker
//(tracker) should be visible instead of (base) in left side of terminal 
* pip install pynput 
* pip install psutil
// made a folder activity_tracker at desktop then opened the directory to it 
created a main.py inside the folder
from pynput import keyboard

def on_press(key):
    try:
        print(f"Key pressed: {key.char}")
    except:
        print(f"Special key pressed: {key}")

listener = keyboard.Listener(on_press=on_press)

listener.start()
listener.join()
// run program in terminal 
python main.py
 
output:
Key pressed: h
Key pressed: e
Key pressed: l
Key pressed: l
Key pressed: o 
//even if typing outside terminal 
