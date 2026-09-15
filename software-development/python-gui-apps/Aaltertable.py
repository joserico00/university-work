import sqlite3

conn = sqlite3.connect('central.db')
cursor = conn.cursor()
cursor.execute('''ALTER TABLE ELDERS
ADD COLUMN HELP TEXT 
''')
conn.commit()

conn.close()
