import sqlite3 as lite
conn = lite.connect('stock.db')
cur = conn.cursor()
#cur.execute('''INSERT INTO stocks VALUES('2021-08-26','BUY','CRSR',90,26.7)''')

print(cur.execute('''SELECT * FROM stocks'''))
conn.commit()
conn.close()