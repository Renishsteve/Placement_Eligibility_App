#python data_generator.py

import sqlite3
from faker import Faker
import random

conn = sqlite3.connect('students.db')
cur = conn.cursor()

fake = Faker()
courses = ['Math', 'English', 'Science', 'History']

for sid in range(1, 501):
    fn, ln = fake.first_name(), fake.last_name()
    email = fake.email()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=30).isoformat()
    cur.execute("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?)",
                (sid, fn, ln, email, dob))

    for course in courses:
        enroll_date = fake.date_between(start_date='-2y', end_date='today').isoformat()
        score = random.randint(50, 100)
        cur.execute("INSERT OR REPLACE INTO enrollments VALUES (?, ?, ?)",
                    (sid, course, enroll_date))
        cur.execute("INSERT OR REPLACE INTO scores VALUES (?, ?, ?)",
                    (sid, course, score))

    # Random attendance: last 30 days
    for d in fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d').split(','):
        # Actually generate each day in code; simplified below
        pass
    # Better:
    import datetime
    today = datetime.date.today()
    for i in range(30):
        date = today - datetime.timedelta(days=i)
        present = random.choice([True, False])
        cur.execute("INSERT OR REPLACE INTO attendance VALUES (?, ?, ?)",
                    (sid, date.isoformat(), present))

conn.commit()
conn.close()
print("500 student records generated.")
