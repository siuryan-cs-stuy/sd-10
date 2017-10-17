import sqlite3
import csv

f = 'discobandit.db'

db = sqlite3.connect(f)
c = db.cursor()

def get_grade(student_id):
    command = 'SELECT code, mark FROM courses WHERE id = %d' % student_id
    c.execute(command)
    grades = []
    for record in c:
        grades.append(record)
    return grades

def get_average(student_id):
    command = 'SELECT mark FROM courses WHERE id = %d' % student_id
    c.execute(command)
    total = 0
    courses = 0
    for record in c:
        total += record[0]
        courses += 1
    return total * 1.0 / courses

def print_students():
    command = 'SELECT name, id FROM peeps'
    c.execute(command)
    string = ''
    for student in c:
        print student
        string += str(get_average(student[1]))
    print string
        
def run():
    print get_grade(1)
    print get_average(1)
    print_students()

run()
db.close()
