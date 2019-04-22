#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3


students = [
    ('Alexey', '252504', 'KSIS'),
    ('Sergey', '455403', 'KSIS'),
    ('Maria', '455403', 'FITU'),
]


def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    try:
        cur.execute("""
            create table students(
                name varchar,
                group_number varchar,
                faculty varchar
            )
        """)
    except sqlite3.Error:
        pass

    for student in students:
        cur.execute("""
            insert into students(name, group_number, faculty) values (?, ?, ?)
        """, student)
        conn.commit()


if __name__ == '__main__':
    init_db()
