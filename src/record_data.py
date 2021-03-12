""" record data based on pressing of buttons """

# -- libs

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2
from tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel
import threading
import time

# -- set up the connections

# the button controller
BUTTON_HOST = "192.168.2.114"
UID_BUTTON = "QnU" # Change XYZ to the UID of your Dual Button Bricklet 2.0

# the spectrum controller
SPECTRUM_HOST = "localhost"
UID_SPECTRUM = "NZ2"

# always the same port
PORT = 4223

# -- globals

last_state = []
last_thread = []
last_state.append("INIT")

# -- functions

# records data and waits for an event
# e is an event that the function is fed
def get_spectrum(arg1, arg2):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print ("recording", arg2)
        the_spectrum = list(spl.get_spectrum())
        print(the_spectrum)
        time.sleep(2)
    print("stop recording", arg2)

# states
# INIT: program initiated
# SRL: start recording left
# BRL: break recording left
# SRR: start recording right
# BRR: break recording right

# callback function trigged by press of button
def button_pressed(button_l, button_r, led_l, led_r):

    print("CALLBACK CALLED --------------------------------------------")

    # print what is coming in from the button sensor
    print("button_l input is ", button_l)
    print("button_r input is", button_l)

    # each time run print the last state
    print("Incoming state (previos call is: ", last_state[-1])
    
    # press left button
    if button_l == BrickletDualButtonV2.BUTTON_STATE_PRESSED:
        print("Left Button: Pressed")
        # if just started
        if last_state[-1] in ["INIT", "BRL", "BRR"]:
            print("begin recording event A")
            last_thread.append(threading.Thread(target=get_spectrum, args=("task", "left")))
            last_thread[-1].start()
            last_state.append("SRL")
        # if recording is running
        elif last_state[-1] == "SRL":
            print("stop recording event A")
            last_state.append("BRL")
            last_thread[-1].do_run = False
            last_thread.pop()
        # all other cases stop recording
        else:
            last_thread[-1].do_run = False
            last_state.append("BRL")
            last_thread.pop()          
    # release left button
    elif button_l == BrickletDualButtonV2.BUTTON_STATE_RELEASED:
        print("Left Button: Released")
        pass  # we should do nothing on release
    # press right button
    if button_r == BrickletDualButtonV2.BUTTON_STATE_PRESSED:
        print("Right Button: Pressed")
        # if not started
        if last_state[-1] in ["INIT", "BRL", "BRR"]:
            print("begin recording event B")
            last_thread.append(threading.Thread(target=get_spectrum, args=("task", "right")))
            last_thread[-1].start()
            last_state.append("SRR")
        # if recording is running stop it
        elif last_state[-1] == "SRR":
            print("stop recording event B")
            last_state.append("BRR")
            last_thread[-1].do_run = False
            last_thread.pop()
        # all other cases stop
        else:
            print("stop recording event B")
            last_state.append("BRR")
            last_thread[-1].do_run = False
            last_thread.pop()
    # relase right button
    elif button_r == BrickletDualButtonV2.BUTTON_STATE_RELEASED:
        print("Right Button: Released")
        pass  # we should do nothing on release
    
    print("Exist state is", last_state[-1])
    n_threads = threading.active_count()
    print("we have ", n_threads, "threads active")

# -- main execution of flow

if __name__ == "__main__":

    # -- button connection and callback

    # set up the connection to the button
    ipcon_button = IPConnection()
    db = BrickletDualButtonV2(UID_BUTTON, ipcon_button)

    # connect to it
    ipcon_button.connect(BUTTON_HOST, PORT)

    # Register the callback, that is 4 params will be fed to cb_state_changed
    # when each of the buttons are pressed
    db.register_callback(db.CALLBACK_STATE_CHANGED, button_pressed)

    # Enable state changed callback
    db.set_state_changed_callback_configuration(True)

    # -- spectrum connection

    # initiate and setup the device
    ipcon_spectrum = IPConnection() # Create IP connection
    ipcon_spectrum.connect(SPECTRUM_HOST, PORT) # Connect to brickd

    # set up the instance and set the type of
    spl = BrickletSoundPressureLevel(UID_SPECTRUM, ipcon_spectrum)
    spl.set_configuration(fft_size=3, weighting=0)

    # suspend the execution indefinately
    input("Press key to exit\n")

    # once released disconnect
    ipcon_button.disconnect()