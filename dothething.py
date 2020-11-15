import cv2
import numpy as np
import sounddevice as sd
from time import sleep

backgroundFrame = cv2.imread('me.PNG')

# mouth size settings
min_mouth_size = 0
max_mouth_size = 50
mouth_width = 100

# center of mouth coordinates
mouth_x = 735
mouth_y = 525

# mouth size multiplier
mouth_size_multiplier = 2

# time between frames
wait_time = 1

# switch to direct mapping mode
direct_mapping = False

# everything below here only used when not in direct audio translation mode
# volume must exceed talking_threshold to count as talking
talking_threshold = 1

# mouth movement speed (value between 0 and max_mouth_size)
mouth_movement_speed = 20

# max number for timeout. mouth stops moving after timeout runs out. prevents weird stops in the middle of sentences
talking_timeout = 1

# \/dont change these\/
mouth_size = 10
opening = True
current_timeout = talking_timeout


def audio_callback(indata, frames, time, status):
    # literally just to get pycharm to stop complaining that I have too many arguments *rolls eyes*
    frames = frames
    time = time
    status = status
    global backgroundFrame
    global mouth_size
    global opening
    global current_timeout
    volume = np.linalg.norm(indata) * 10

    if not direct_mapping:
        if volume > talking_threshold or current_timeout > 0:
            if opening:
                mouth_size += mouth_movement_speed
                if mouth_size >= max_mouth_size:
                    opening = False
            else:
                mouth_size -= mouth_movement_speed
                if mouth_size <= min_mouth_size:
                    opening = True
            if volume <= talking_threshold:
                current_timeout -= 1
            elif current_timeout < talking_timeout:
                current_timeout += 1
        else:
            mouth_size = 0
            opening = True
    else:
        # mouth size based on volume
        mouth_size = int(volume/50 * max_mouth_size * mouth_size_multiplier)
        if mouth_size > max_mouth_size:
            mouth_size = max_mouth_size

    #print(volume)

    # just verify that mouth_size is within the limits given, prevents weird errors. I'm lazy.
    mouth_size = 0 if mouth_size < 0 else mouth_size
    mouth_size = max_mouth_size if mouth_size > max_mouth_size else mouth_size

    image = cv2.imread('me.PNG')
    image = cv2.ellipse(image, (mouth_x, mouth_y), (mouth_width, mouth_size), 0, 0, 360, (0, 0, 255), 5)
    cv2.imshow('image', image)
    cv2.waitKey(wait_time)


try:
    with sd.InputStream(callback=audio_callback):
        # This is just me screwing around, but now im to lazy to change it so, here is an example of ... reallllllly bad
        # code lol. Like what does it even do? who knows?
        true = True
        while true:
            sd.sleep(1)
            sleep(1)
        cv2.destroyAllWindows()
except Exception:
    cv2.destroyAllWindows()