""" light up the unicorn hat on pizero to show recording status """

import paramiko

def light_up(clss):

    client = paramiko.SSHClient()   
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.2.115", username="pi")
    client.exec_command(f"python3 /home/pi/Projects/TheBlinkt/red_green.py {clss}")
    client.close()
    