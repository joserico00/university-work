import sqlite3
conn = sqlite3.connect('testda.db')
query=(''' CREATE TABLE DATAATBLE
        (FIRSTINDEX  TEXT NOT NULL,
        SECONDINDEX  INT);

                ''')
conn.execute(query)
conn.close()
