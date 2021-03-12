""" test wrting data to the attached stick """

import os


# -- globals

USB_DRIVE = "/media/pi/FILE_STOR16/"
FILENAME = "mango.txt"

# -- write a random file

test = os.path.join(USB_DRIVE, FILENAME)
print(test)

with open(test, 'w') as filehandle:
    filehandle.write('A line of text\n')
    filehandle.write('A second line of text ÅÄÖ åäö\n')




