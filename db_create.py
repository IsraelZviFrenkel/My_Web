import sqlite3

db_locale = 'student.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
CREATE TABLE contact_details
(id INTEGER PRIMARY KEY AUTOINCREMENT,
firstname TEXT,
lastname TEXT,
street_address TEXT,
city TEXT
)
""")

connie.commit()
connie.close()
