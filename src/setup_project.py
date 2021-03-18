""" set up project """

import sqlite3
import confs
import os

# -- generate column names that we need to define tables

# loop over names
table_defs = []
for row in range(1, 513):
    table_defs.append(f"'spec{row}' NUMERIC,")

# collapse to strings
table_defs = ''.join(table_defs)

# -- generate the table definition and execute the table creation

decibel_table_def = f"""
CREATE TABLE 'decibel' (
    'measureID' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    'event' TEXT,
    {table_defs}
    'tstamp' TEXT
)
"""

# with open("decibel_def.sql", "w") as text_file:
#     text_file.write(decibel_table_def)

sound_conn = sqlite3.connect(os.path.join(confs.proj_path, "spectrum.db"))
cur = sound_conn.cursor()
cur.execute(decibel_table_def)
sound_conn.commit()
sound_conn.close()
