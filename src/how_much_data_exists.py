""" check how much data is recorded """


import sqlite3
import confs
import pandas as pd


def show_me_the_data():

    query = """

    with interesting as (
        select measureID, event, tstamp
        from decibel )
    select count(*) as obs_count, event, min(tstamp), max(tstamp)
    from interesting
    group by event
    """

    sound_conn = sqlite3.connect(confs.db_path)
    df = pd.read_sql_query(query, sound_conn)
    print(df)
    sound_conn.close()

if __name__ == "__main__":
    show_me_the_data()
