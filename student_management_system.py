HALF_LINE = "="*10
LINE = "=" *30
import sqlite3

class StudentManager:

    def __init__(self):

        self.connection = sqlite3.connect("data.db")

        self.cursor = self.connection.cursor()
        self.cursor.execute("""
               CREATE TABLE IF NOT EXISTS students (
               id INTEGER PRIMARY KEY,
               name TEXT,
               age INTEGER,
               course TEXT
               )""")
        self.connection.commit()


    def close(self):
        self.connection.close()    
        
    
    def display(self,id,name,age,course):
        print(LINE)
        print(f"ID     : {id}")
        print(f"Name   : {name}")
        print(f"Age    : {age}")
        print(f"Course :{course}")
        print(LINE)
        print()


    def add_student(self):
        while True:
            name = input("Enter name : ").strip().capitalize()
            if name:
                break
            else:
                print("Name can't be empty!")
        while True:
            try:
                age = int(input("Enter age:"))
                break
            except ValueError:
                print("Enter number only!")
                continue
        while True:
            course = input("Enter course : ").strip().capitalize()
            if course:
                break
            else:
                print("Course can't be empty!")
        self.cursor.execute("""INSERT INTO students(name, age, course)
                            VALUES(?, ?, ?)""",(name, age, course))
        self.connection.commit()
        print("Student added successfully!")
    

    def view_students(self):
        self.cursor.execute("SELECT * FROM students ")
        students = self.cursor.fetchall()
        if students:
            for student in students:
                self.display(*student)
        else:
            print("No student found!")
        

    def search_student(self):
        while True:
            print(f"{HALF_LINE} Search Student {HALF_LINE}")
            print("1.Search by name")
            print("2.Search by age")
            print("3.Search by course")
            print("4.Back")
            while True:
                try:
                    choice = int(input("Enter number you want to search by: "))
                    if choice< 1 or choice>4:
                        print("Enter number between 1 to 4")
                        continue
                    break
                except ValueError:
                    print("Enter number only!")

            if choice == 1:
                while True:
                    text = input("Enter name or starting letters : ").strip()
                    if text:
                        break
                    print("Name cannot be empty!")

                query = "SELECT *  FROM students WHERE name LIKE ?"
                params = (f"%{text}%",)
            elif choice == 2:
                while True:
                    try:
                        age = int(input("Enter age:"))
                        break
                    except ValueError:
                        print("Enter number only!")
                query= "SELECT *  FROM students WHERE age =?"
                params = (age,)
            elif choice == 3:
                while True:
                    course_text = input("Enter course: ").strip()
                    if course_text:
                        break
                    print("Course cannot be empty!")
                query= "SELECT *  FROM students WHERE course LIKE ?"
                params = (f"%{course_text}%",)
            elif choice == 4:
                break
            self.cursor.execute(query,params)
            students = self.cursor.fetchall()
            if students:
                for student in students:
                    self.display(*student)
            else:
                print("No matching student found!")


    def update_student(self):
        while True:
            try:
                student_id = int(input("Enter student id: "))
                break
            except ValueError:
                print("Enter number only!")
        self.cursor.execute("SELECT * FROM students WHERE id =?",(student_id,))
        student = self.cursor.fetchone()
        if student:
            self.display(*student)
            while True:
                y_n = input("Do you want to update this student's details?(Y/N): ").strip().lower()
                if y_n in ["y","n"]:
                    break
            if y_n == "y":
                while True:
                    print(f"{HALF_LINE} Update details {HALF_LINE}")
                    print("1.Update name")
                    print("2.Update age")
                    print("3.Update course")
                    print("4.Back")
                    while True:
                        try:
                            choice = int(input("Enter the option number what you want to change: "))
                            if choice<1 or choice>4:
                                print("Enter number between 1 to 4!")
                                continue
                            break
                        except ValueError:
                            print("Enter number only!")


                    if choice == 1:
                        while True:
                            new_name = input("Enter new name: ").strip().capitalize()
                            if new_name:
                                break
                            print("Name cannot be empty!")
                        query = "UPDATE students SET name =? WHERE id =?"
                        params = new_name
                        message = "Name updated successfully!"


                    elif choice ==2:
                        while True:
                            try:
                                new_age = int(input("Enter new age: "))
                                break
                            except ValueError:
                                print("Enter age in number only!")
                        query = "UPDATE students SET age =? WHERE id =?"
                        params = new_age
                        message = "Age updated successfully!"


                    elif choice ==3:
                        while True:
                            new_course = input("Enter new course : ").strip().capitalize()
                            if new_course:
                                break
                            print("Course cannot be empty!")
                        query = "UPDATE students SET course =? WHERE id =?"
                        params = new_course
                        message = "Course updated successfully!"

                    elif choice == 4:
                        break
                    self.cursor.execute(query,(params,student_id))
                    self.connection.commit()
                    print(message)
        else:
            print("No matching student found!")

        
    def delete_student(self):
        while True:
            try :
                student_id =  int(input("Enter student ID: "))
                break
            except ValueError:
                print("Enter number only!")
        self.cursor.execute("SELECT * FROM students WHERE id =?",(student_id,))
        student = self.cursor.fetchone()
        if student:
            self.display(*student)
            while True:
                y_n = input("Are you sure you want to delete this student?(Y/N)").lower().strip()
                if y_n in ["y","n"]:
                    break
            if y_n == "y":
                self.cursor.execute("DELETE FROM students WHERE id =?",(student_id,))
                self.connection.commit()
                print("Student deleted successfully!")
            else:
                print("Deletion cancelled!")
        else:
            print("Matching student not found!")

        
    def count_students(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        result = self.cursor.fetchone()[0]
        if result == 0:
            print("No student available!")
        else:
            print(LINE)
            print(f"Total students : {result}")
            print(LINE)


    def sort_students(self):
        while True:
            print(f"{HALF_LINE} Sort Student {HALF_LINE}")
            print("1.Name(A-z)")
            print("2.Name(Z-A)")
            print("3.Age (Low - High)")
            print("4.Age (High -Low)")
            print("5.Back")
            print()
            while True:
                try:
                    choice = int(input("Enter choice: "))
                    if choice <1 or choice>5:
                        print("Enter number betweent     1 to 5!")
                        continue
                    break
                except ValueError:
                    print("Enter number only!")


            if choice == 1:
                query = "SELECT * FROM students ORDER BY name"


            elif choice ==2:
                query = "SELECT * FROM students ORDER BY name DESC"
      

            elif choice == 3:
                query = "SELECT * FROM students ORDER BY age"
            


            elif choice == 4:
                query = "SELECT * FROM students ORDER BY age DESC"


            elif  choice == 5:
                break


            self.cursor.execute(query)
            students = self.cursor.fetchall()
            if students:
                for student in students:
                    self.display(*student)
            else:
                print("Student list is empty!")    



def main():
    manager = StudentManager()
    while True:
        print(f"{HALF_LINE} Student Management System {HALF_LINE}")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Count Students")
        print("7. Sort Students")
        print("8. Exit")
        print()
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice<1 or choice>8:
                    print("Enter number between 1 to 8!")
                    continue
                break
            except ValueError:
                print("Enter number only!")
        if choice == 1:
            manager.add_student()
        elif choice == 2:
            manager.view_students()
        elif choice == 3:
            manager.search_student()
        elif choice == 4:
            manager.update_student()
        elif choice == 5:
            manager.delete_student()
        elif choice == 6:
            manager.count_students()
        elif choice == 7:
            manager.sort_students()
        elif choice == 8:
            print("Thank you! For using student management system!")
            manager.close()
            break
    

if __name__ == "__main__":
    main()
