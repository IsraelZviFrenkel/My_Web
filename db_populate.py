import sqlite3

db_locale = 'student.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
INSERT INTO contact_details (firstname, lastname, street_address, city) VALUES
('David', 'Bowie', '11 Stardust Way', 'Wynnum'),
('Israel', 'Frenkel', '3 Shlomo Zlotnik', 'Petah Tikva'),
('Eden', 'Scott', '15 Hero', 'Sidni')
 """)

connie.commit()
connie.close()
