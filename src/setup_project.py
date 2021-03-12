""" set up project """

import sqlite3
import confs
import os

# --create database for sound spectrum

sound_conn = sqlite3.connect(os.path.join(confs.proj_path, "spectrum.db"))
cur = sound_conn.cursor()

# -- create decibel table

# TODO: