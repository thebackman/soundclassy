
# -- paths

proj_path = "/home/pi/Projects/soundclassy"

# -- connections to tinkerforge

HOST = "localhost"
PORT = 4223

MASTER_UID = "6Kvmoe"
SOUND_UID = "NZ2"

# -- database connections

# -- variable names

def create_var_names():
    varnames = [f"spec{item}" for item in range(1,513)]
    questions = ["?" for letter in range(1,515)]
    return (varnames, questions)

all_spectrums, all_questions = create_var_names()
len(all_spectrums)
len(all_questions)

all_spectrums = ','.join(all_spectrums)
all_spectrums
all_questions = ','.join(all_questions)
all_questions

insert_query = f"""
INSERT INTO decibel
(tstamp,
event,
{all_spectrums})
VALUES ({all_questions});
"""

with open("Output.sql", "w") as text_file:
    text_file.write(insert_query)

