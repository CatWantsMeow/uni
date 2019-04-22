#!/usr/bin/env python3
import sqlite3
import tkinter as tk
from tkinter import messagebox


class App(tk.Frame):

    def __init__(self, master):
        super(App, self).__init__(master)
        self.pack()
        self.create_widgets()

        self.conn = sqlite3.connect("students.db")
        self.init_db()
        self.select_all_students()

    def create_widgets(self):
        self.name_input_frame = tk.Frame(self, padx=2, pady=2)
        self.name_label = tk.Label(self.name_input_frame, text="Name", width=11, anchor=tk.W)
        self.name_label.pack(side='left')
        self.name_input = tk.Entry(self.name_input_frame)
        self.name_input.pack(side='left')
        self.name_input_frame.pack()

        self.group_number_input_frame = tk.Frame(self, padx=2, pady=2)
        self.group_number_label = tk.Label(self.group_number_input_frame, text="Group Number", width=11, anchor=tk.W)
        self.group_number_label.pack(side='left')
        self.group_number_input = tk.Entry(self.group_number_input_frame)
        self.group_number_input.pack(side='left')
        self.group_number_input_frame.pack()

        self.faculty_input_frame = tk.Frame(self, padx=2, pady=2)
        self.faculty_label = tk.Label(self.faculty_input_frame, text="Faculty", width=11, anchor=tk.W)
        self.faculty_label.pack(side='left')
        self.faculty_input = tk.Entry(self.faculty_input_frame)
        self.faculty_input.pack(side='left')
        self.faculty_input_frame.pack()

        self.buttons_frame = tk.Frame(self, padx=2, pady=2)
        self.create_button = tk.Button(self.buttons_frame, text='Create Student', width=13, command=self.create_student)
        self.create_button.pack(side='left')
        self.find_button = tk.Button(self.buttons_frame, text='Find Students', width=13, command=self.select_students)
        self.find_button.pack(side='left')
        self.buttons_frame.pack()

        self.students_list_box = tk.Listbox(self, width=32, height=20)
        self.students_list_box.pack()

        self.delete_button_frame = tk.Frame(self, padx=2, pady=2)
        self.delete_button = tk.Button(self.delete_button_frame, text='Delete Student', width=31, command=self.delete_student)
        self.delete_button.pack()
        self.delete_button_frame.pack()

    def init_db(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE students(
                    name varchar,
                    group_number varchar,
                    faculty varchar
                )
            """)
        except sqlite3.Error as e:
            pass

    def select_all_students(self):
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT name, group_number, faculty FROM students')
            rows = cur.fetchall()
        except sqlite3.Error as e:
            tk.messagebox.showwarning("Error", "Database error: {}".format(e))
            rows = []

        self.students_list_box.delete(0, tk.END)
        for row in rows:
            self.students_list_box.insert(tk.END, "{}, {}, {}".format(*row))

    def select_students(self):
        name = self.name_input.get()
        group_number = self.group_number_input.get()
        faculty = self.faculty_input.get()

        sql = 'SELECT name, group_number, faculty FROM students'
        if name or group_number or faculty:
            statements = []
            if name:
                statements.append("(name = '{}')".format(name))
            if group_number:
                statements.append("(group_number = '{}')".format(group_number))
            if faculty:
                statements.append("(faculty = '{}')".format(faculty))
            sql += " WHERE " + " AND ".join(statements)

        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        except sqlite3.Error as e:
            tk.messagebox.showwarning("Error", "Database error: {}".format(e))
            rows = []

        self.students_list_box.delete(0, tk.END)
        for row in rows:
            self.students_list_box.insert(tk.END, "{}, {}, {}".format(*row))

    def create_student(self):
        name = self.name_input.get()
        group_number = self.group_number_input.get()
        faculty = self.faculty_input.get()

        if not name or not group_number or not faculty:
            tk.messagebox.showwarning("Error", "All fields must be filled!")
        else:
            try:
                cur = self.conn.cursor()
                cur.execute('INSERT INTO students VALUES (?, ?, ?)', [name, group_number, faculty])
                self.conn.commit()
            except sqlite3.Error as e:
                tk.messagebox.showwarning("Error", "Database error: {}".format(e))

            self.select_all_students()

            self.name_input.delete(0, tk.END)
            self.name_input.insert(0, "")

            self.group_number_input.delete(0, tk.END)
            self.group_number_input.insert(0, "")

            self.faculty_input.delete(0, tk.END)
            self.faculty_input.insert(0, "")

    def delete_student(self):
        index = self.students_list_box.curselection()
        if not index:
            tk.messagebox.showwarning('Warning', 'No student selected!')

        name, group_number, faculty = self.students_list_box.get(index[0]).split(',')

        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                    DELETE FROM students
                    WHERE (name = ?) AND (group_number = ?) AND (faculty = ?)
                """,
                [name.strip(), group_number.strip(), faculty.strip()]
            )
            self.conn.commit()
        except sqlite3.Error as e:
            tk.messagebox.showwarning("Error", "Database error: {}".format(e))

        self.select_all_students()


def main():
    root = tk.Tk()
    # root.geometry("600x600")
    app = App(root)
    app.mainloop()


if __name__ == '__main__':
    main()
