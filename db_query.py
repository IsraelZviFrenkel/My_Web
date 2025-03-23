import sqlite3


db_locale = 'student.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
SELECT * FROM contact_details
 """)

student_info = c.fetchall()

for student in student_info:
    print(student)


connie.commit()
connie.close()