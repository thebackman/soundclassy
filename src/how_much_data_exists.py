""" check how much data has been recorded so far """


import sqlite3
import confs
import pandas as pd


def show_me_the_data():

    query = """

    with interesting as (
        select measureID, event, tstamp
        from decibel ),
    intermediate as (
        select count(*) as obs_count, event
        from interesting
        group by event ),
    total as (
        select sum(obs_count) as total_n
        from intermediate
    )
    select
        a.event,
        a.obs_count,
        b.total_n,
        (cast(a.obs_count as real) / cast(b.total_n as real)) * 100 as the_balance
    from intermediate a, total b ;
    """

    sound_conn = sqlite3.connect(confs.db_path)
    df = pd.read_sql_query(query, sound_conn)
    print(df)
    sound_conn.close()

if __name__ == "__main__":
    show_me_the_data()



