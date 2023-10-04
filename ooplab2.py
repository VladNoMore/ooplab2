import os
from enum import Enum
from datetime import date


class StudyField(Enum):
    MECHANICAL_ENGINEERING = 1
    SOFTWARE_ENGINEERING = 2
    FOOD_TECHNOLOGY = 3
    URBANISM_ARCHITECTURE = 4
    VETERINARY_MEDICINE = 5

class Student:
    def __init__(self, first_name, last_name, email, enrollment_date, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.enrollmentDate = enrollment_date  # Using camelCase for attribute names
        self.dateOfBirth = date_of_birth  # Using camelCase for attribute names

class Faculty:
    def __init__(self, name, abbreviation, study_field):
        self.name = name
        self.abbreviation = abbreviation
        self.students = []
        self.studyField = study_field  # Using camelCase for attribute names

class University:
    def __init__(self):
        self.faculties = []
        self.unassigned_students = []

    def create_faculty(self, name, abbreviation, study_field):
        faculty = Faculty(name, abbreviation, study_field)
        self.faculties.append(faculty)
        return faculty

    def assign_student_to_faculty(self, student, faculty):
        if student not in faculty.students:
            faculty.students.append(student)

    def graduate_student(self, student, faculty):
        if student in faculty.students:
            faculty.students.remove(student)

    def display_enrolled_students(self, faculty):
        print(f"Enrolled students in {faculty.name}:")
        for student in faculty.students:
            print(f"{student.first_name} {student.last_name}")

    def display_graduates(self, faculty):
        print(f"Graduates from {faculty.name}:")
        for student in self.get_graduates(faculty):
            print(f"{student.first_name} {student.last_name}")

    def student_belongs_to_faculty(self, student, faculty):
        return student in faculty.students

    def get_graduates(self, faculty):
        return [student for student in faculty.students if student not in self.get_enrolled_students(faculty)]

    def enroll_student(self, student):
        if student not in self.unassigned_students:
            self.unassigned_students.append(student)

    def get_faculty_by_student_identifier(self, identifier):
        for faculty in self.faculties:
            for student in faculty.students:
                if student.email == identifier:
                    return faculty
        return None

    def get_faculties_by_study_field(self, study_field):
        return [faculty for faculty in self.faculties if faculty.studyField == study_field]

    def display_all_faculties(self):
        print("University faculties:")
        for faculty in self.faculties:
            print(f"{faculty.name} ({faculty.abbreviation}) - {faculty.studyField.name}")

def save_data(data):
    with open("university_data.txt", "w") as file:
        for faculty in data:
            file.write(f"Faculty: {faculty.name}\n")
            file.write(f"Abbreviation: {faculty.abbreviation}\n")
            file.write(f"Study Field: {faculty.studyField.name}\n")
            file.write("Students:\n")
            for student in faculty.students:
                file.write(f"  Name: {student.first_name} {student.last_name}\n")
                file.write(f"  Email: {student.email}\n")
                file.write(f"  Enrollment Date: {student.enrollmentDate}\n")
                file.write(f"  Date of Birth: {student.dateOfBirth}\n")
            file.write("\n")

def load_data():
    faculties = []
    current_faculty = None

    if os.path.exists("university_data.txt"):
        with open("university_data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(": ")
                if parts[0] == "Faculty":
                    current_faculty = Faculty(parts[1], "", StudyField[parts[2]])
                    faculties.append(current_faculty)
                elif parts[0] == "Abbreviation":
                    current_faculty.abbreviation = parts[1]
                elif parts[0] == "Students":
                    current_faculty.students = []
                elif parts[0] == "Name":
                    student_name = parts[1].split(" ")
                    first_name = student_name[1]
                    last_name = student_name[2]
                elif parts[0] == "Email":
                    email = parts[1]
                elif parts[0] == "Enrollment Date":
                    enrollment_date = parts[1]
                elif parts[0] == "Date of Birth":
                    date_of_birth = parts[1]
                    student = Student(first_name, last_name, email, enrollment_date, date_of_birth)
                    current_faculty.students.append(student)
    return faculties

def main():
    university = University()
    loaded_data = load_data()
    if loaded_data:
        university.faculties = loaded_data

    while True:
        print("\nTUM Board Menu:")
        print("1. Create Faculty")
        print("2. Assign Student to Faculty")
        print("3. Graduate Student from Faculty")
        print("4. Display Enrolled Students")
        print("5. Display Graduates")
        print("6. Check if Student Belongs to Faculty")
        print("7. Search Faculty by Student Identifier")
        print("8. Display All Faculties")
        print("9. Enroll New Student")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter faculty name: ")
            abbreviation = input("Enter faculty abbreviation: ")
            study_field = StudyField(int(input("Enter study field (1-5): ")))
            university.create_faculty(name, abbreviation, study_field)
            print("Faculty created successfully!")
            
            
        elif choice == "2":
            email =  input("Enter student's email: ")
            faculty = university.get_faculty_by_student_identifier(email)


            if student:
                faculty_index = int(input("Enter the index of the faculty to assign the student to: "))
                if 0 <= faculty_index < len(university.faculties):
                    faculty = university.faculties[faculty_index]
                    university.assign_student_to_faculty(student,faculty)
                    print("Student assigned to faculty succesful")
                else:
                    print("Invalid faculty index")
            else:
                print("Student not found")
        

 
        elif choice == "3":
            email = input("Enter student's email: ")
            faculty = university.get_faculty_by_student_identifier(email)
            if faculty:
                student = next((s for s in faculty.students if s.email == email), None)
                if student:
                    university.graduate_student(student, faculty)
                    print("Student graduated from faculty successfully!")
                else:
                    print("Student not found.")
            else:
                print("Student not found.")

        elif choice == "4":
            faculty = university.faculties[int(input("Enter faculty index: "))]
            university.display_enrolled_students(faculty)

        elif choice == "5":
            faculty = university.faculties[int(input("Enter faculty index: "))]
            university.display_graduates(faculty)

        elif choice == "6":
            email = input("Enter student's email: ")
            faculty = university.get_faculty_by_student_identifier(email)
            if faculty:
                student = next((s for s in faculty.students if s.email == email), None)
                if student:
                    print(f"Student belongs to {faculty.name}.")
                else:
                    print("Student not found in the specified faculty.")
            else:
                print("Student not found.")

        elif choice == "7":
            email = input("Enter student's email: ")
            faculty = university.get_faculty_by_student_identifier(email)
            if faculty:
                print(f"Student with email {email} belongs to {faculty.name}.")
            else:
                print("Student not found.")

        elif choice == "8":
            university.display_all_faculties()

        elif choice == "9":
            first_name = input("Enter student's first name: ")
            last_name = input("Enter student's last name: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
            email = input("Enter student's email: ")
            student = Student(first_name, last_name, email, enrollment_date, date_of_birth)
            university.enroll_student(student)
            print("Student enrolled successfully!")

        elif choice == "10":
            save_data(university.faculties)
            print("Data saved successfully.")
            break

if __name__ == "__main__":
    main()