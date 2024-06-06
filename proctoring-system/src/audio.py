import sounddevice as sd
import numpy as np
import threading

# Placeholders and global variables
SOUND_AMPLITUDE = 0
AUDIO_CHEAT = 0

# Sound variables
CALLBACKS_PER_SECOND = 38               # Callbacks per second (system dependent)
SUS_FINDING_FREQUENCY = 2               # Calculate SUS *n* times every sec
SOUND_AMPLITUDE_THRESHOLD = 20          # Amplitude considered for SUS calc

# Packing *n* frames to calculate SUS
FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)
AMPLITUDE_LIST = [0] * FRAMES_COUNT
SUS_COUNT = 0
count = 0

def print_sound(indata, outdata, frames, time, status):
    global SOUND_AMPLITUDE, SUS_COUNT, count, AUDIO_CHEAT

    # Calculate the norm of the incoming audio data
    vnorm = int(np.linalg.norm(indata) * 10)
    AMPLITUDE_LIST.append(vnorm)
    count += 1
    AMPLITUDE_LIST.pop(0)
    
    if count == FRAMES_COUNT:
        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT
        SOUND_AMPLITUDE = avg_amp
        
        if avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            SUS_COUNT += 1
            if SUS_COUNT >= 2:
                AUDIO_CHEAT = 1
                SUS_COUNT = 0
        else:
            SUS_COUNT = 0
            AUDIO_CHEAT = 0
        count = 0

def sound():
    with sd.Stream(callback=print_sound):
        sd.sleep(int(1000 * 60 * 60 * 24))  # Run for 24 hours

def main():
    sound_thread = threading.Thread(target=sound)
    sound_thread.start()

    try:
        while True:
            if AUDIO_CHEAT:
                print("!!!!!!!!!!!! FBI OPEN UP !!!!!!!!!!!!")
            else:
                print("Silence or normal noise.")
            sd.sleep(1000)  # Check every second
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
