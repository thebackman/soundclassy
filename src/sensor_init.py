""" turn off the leds on the sensors / bricks on restart """

import time
import confs
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster
from tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel

# Create IP connection
ipcon = IPConnection() 

# bricks and bricklets
master = BrickMaster(confs.MASTER_UID, ipcon)
spl = BrickletSoundPressureLevel(confs.SOUND_UID, ipcon)

# connect
ipcon.connect(confs.HOST, confs.PORT)

# turn on the leds

master.enable_status_led()
spl.set_status_led_config(1)

# sleepa while
time.sleep(10)

# turn them off
master.disable_status_led()
spl.set_status_led_config(0)

# when done dsiconnect
ipcon.disconnect()
