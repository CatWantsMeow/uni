#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html
import sqlite3


def return_not_found(name):
    print("Content-Type: text/html")
    print()
    with open('html/not_found.html', 'r') as f:
        print(f.read().format(name=name))


def return_db_error(e):
    print("Content-Type: text/html")
    print()
    with open('html/db_error.html', 'r') as f:
        print(f.read().format(error=str(e)))


def return_student(name, group, faculty):
    print("Content-Type: text/html")
    print()
    with open('html/student.html', 'r') as f:
        print(f.read().format(name=name, group=group, faculty=faculty))


cgitb.enable()
form = cgi.FieldStorage()
name = form.getfirst('student_name', None)
name = html.escape(name)


conn = sqlite3.connect('students.db')
cur = conn.cursor()
try:
    cur.execute(
        'select name, group_number, faculty from students where name = ?',
        [name]
    )
    student = cur.fetchone()

    if not student:
        return_not_found(name)
    else:
        return_student(student[0], student[1], student[2])

except sqlite3.Error as e:
    raise
    return_db_error(e)
