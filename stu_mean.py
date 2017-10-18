import sqlite3
import csv

f = 'discobandit.db'

db = sqlite3.connect(f)
c = db.cursor()

def get_student(student_id):
    command = 'SELECT name, mark FROM peeps, courses WHERE courses.id = peeps.id AND peeps.id = %d' % student_id
    return c.execute(command)

def get_name(student_id):
    student = get_student(student_id)
    for record in student:
        return record[0]

def get_grade(student_id):
    student = get_student(student_id)
    grades = []
    for course in student:
        grades.append(course[1])
    return grades

def get_average(student_id):
    student = get_student(student_id)
    total = 0
    courses = 0
    for record in student:
        total += record[1]
        courses += 1
    return total * 1.0 / courses

def student_info(student_id):
    print "Name: " + get_name(student_id) + "\nID: " + str(student_id) + "\nAverage: " + \
        str(get_average(student_id))

def populate_peeps_avg():
    cursor = c.execute("SELECT id FROM peeps")
    for record in cursor.fetchall():
        command = "INSERT INTO peeps_avg VALUES (%d, %d)" % (record[0], get_average(record[0]))
        c.execute(command)
    db.commit()

def update_average(student_id, new_average):
    command = "UPDATE peeps_avg SET average = %d WHERE id = %d" % (new_average, student_id)
    c.execute(command)
    db.commit()

def add_course(row):
    command = 'INSERT INTO courses VALUES ("%s", %d, %d)' % (row['code'], int(row['mark']), int(row['id']))
    c.execute(command)
    db.commit()
    
def add_courses():
    with open('courses.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            command = 'SELECT * FROM courses WHERE code = "%s" AND mark = %d AND id = %d' % (row['code'], int(row['mark']), int(row['id']))
            results = c.execute(command).fetchall()
            if len(results) == 0:
                add_course(row)
                update_average(int(row['id']), get_average(int(row['id'])))
            
def run():
    print get_grade(1)
    print get_average(1)
    student_info(1)
    student_info(5)

    try:
        command = "CREATE TABLE peeps_avg (id INTEGER, average INTEGER)"
        c.execute(command)
        populate_peeps_avg()
    except sqlite3.OperationalError:
        print "peeps_avg already exists"

    add_courses()
    student_info(1)
    student_info(5)
    
    
run()
db.close()
