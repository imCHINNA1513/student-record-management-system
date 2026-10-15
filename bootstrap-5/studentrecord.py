
import sqlite3

# Connect to the database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the student table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL,
    marks REAL NOT NULL
)
""")
conn.commit()


def add_student():
    print("\n--- Add Student ---")

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return

    try:
        age = int(input("Enter age: "))
        if age <= 0:
            print("Age must be greater than zero!")
            return

        course = input("Enter course: ").strip()
        if not course:
            print("Course cannot be empty!")
            return

        marks = float(input("Enter marks (0-100): "))
        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100!")
            return

        cursor.execute(
            "INSERT INTO students (name, age, course, marks) VALUES (?, ?, ?, ?)",
            (name, age, course, marks)
        )
        conn.commit()
        print("Student added successfully!")

    except ValueError:
        print("Invalid input! Please enter numbers for age and marks.")


def view_students():
    print("\n--- All Students ---")

    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()

    if not students:
        print("No student records found.")
        return

    print("-" * 75)
    print(f"{'ID':<5}{'Name':<22}{'Age':<8}{'Course':<25}{'Marks':<10}")
    print("-" * 75)

    for student in students:
        student_id, name, age, course, marks = student
        print(f"{student_id:<5}{name:<22}{age:<8}{course:<25}{marks:<10.1f}")

    print("-" * 75)


def search_student():
    print("\n--- Search Student ---")

    try:
        student_id = int(input("Enter student ID: "))
        cursor.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        )
        student = cursor.fetchone()

        if student:
            print("\nStudent found!")
            print(f"ID:     {student[0]}")
            print(f"Name:   {student[1]}")
            print(f"Age:    {student[2]}")
            print(f"Course: {student[3]}")
            print(f"Marks:  {student[4]}")
        else:
            print("Student not found.")

    except ValueError:
        print("Please enter a valid numeric ID.")


def update_student():
    print("\n--- Update Student ---")

    try:
        student_id = int(input("Enter student ID to update: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        )
        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        print(f"Current name: {student[1]}")
        name = input("Enter new name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return

        age = int(input("Enter new age: "))
        if age <= 0:
            print("Age must be greater than zero!")
            return

        course = input("Enter new course: ").strip()
        if not course:
            print("Course cannot be empty!")
            return

        marks = float(input("Enter new marks (0-100): "))
        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100!")
            return

        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, course = ?, marks = ?
            WHERE id = ?
        """, (name, age, course, marks, student_id))

        conn.commit()
        print("Student updated successfully!")

    except ValueError:
        print("Invalid input! Please check the age and marks.")


def delete_student():
    print("\n--- Delete Student ---")

    try:
        student_id = int(input("Enter student ID to delete: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        )
        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        confirm = input(
            f"Delete record for {student[1]}? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            cursor.execute(
                "DELETE FROM students WHERE id = ?", (student_id,)
            )
            conn.commit()
            print("Student deleted successfully!")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid numeric ID.")


def main():
    while True:
        print("\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
