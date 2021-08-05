import sqlite3
conn = sqlite3.connect("test.db") 
cursor = conn.cursor()
cursor.execute("""CREATE TABLE images
                  (name text)
               """)
