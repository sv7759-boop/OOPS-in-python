import json
from abc import ABC , abstractmethod
from pathlib import Path

database = "school_data.json"
data = {"students" : [] , "teachers" : []}

if Path(database).exists():
    with open(database , 'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database , "w") as f:
        json.dump(data , f , indent = 4)

class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
          return True
        else:
          return False

class students(Persons):

    def get_roles(self):
        return "student"

    def register(self):
        name = input("tell your name :- ")
        age = int(input("tell your age :-"))
        email = input("tell your mail:- ")
        roll_no = input("tell your roll number:- ")

        if not Persons.validate_email(email):
            print("invalid email")
            return

        for i in data['students']:
            if i['roll_no'] == roll_no:
                print("student already exist")
                return

        data['students'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "roll_no" : roll_no,
            "grades" : {}
        })

        save()

        print(f"student: {name} with roll no.: {roll_no} sucessfully registered!")

    def show_details(self):
        roll_no = input("roll no :- ")
        for i in data["students"]:
            if i["roll_no"] == roll_no:
                grades = i["grades"]
                avg = sum(i["grades"].values()) / len(i["grades"]) if grades else 0

                print(f"\nName : {i["name"]}")
                print(f"Roll no : {i["roll_no"]}")
                print(f"Grades : {i["grades"]}")
                print(f"Average : {avg:.1f}")
                return
        print("Student not found")



    def add_grade(self):
        roll_no = input("tell the roll number:- ")
        subject = input("Subject : ")
        marks = float(input("Marks : "))

        for i in data["students"]:
            if i["roll_no"] == roll_no:
                i["grades"][subject] = marks
                save()
                print("grade added successfully")
                return
        print("student not found")
    
class Teachers(Persons):

    def get_roles(self):
        return "Teacher"

    def register(self):
        name = input("tell your name :- ")
        age = int(input("tell your age :-"))
        email = input("tell your mail:- ")
        emp_id = input("tell your emp_id number:- ")
        subject = input("tell the subject you teach:- ")
        
        if not Persons.validate_email(email):
            print("invalid email")
            return

        for i in data['teachers']:
            if i['emp_id'] == emp_id:
                print("teacher already exist")
                return

        data['teachers'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "emp_id" : emp_id,
            "subject" : subject
        })

        save()

        print(f"teacher: {name} with employe no.: {emp_id} sucessfully registered!")

    def show_details(self):
        emp_id = input("tell the employe number:- ")
        for i in data["teachers"]:
            if i["emp_id"] == emp_id:
                print(f"\nName : {i["name"]}")
                print(f"Age : {i["age"]}")
                print(f"Employe ID : {i["emp_id"]}")
                print(f"Subject : {i["subject"]}")
                return
        print("Teacher not found")



    

print("press 1 to register a student")
print("press 2 to register a teacher")
print("press 3 to add grades")
print("press 4 to show student details")
print("press 5 to show teacher details")

choice = int(input("please tell your choice:- "))

student = students()
teacher = Teachers()

if choice == 1:
    student.register()

elif choice == 2:
    teacher.register()

elif choice == 3:
    student.add_grade()

elif choice == 4:
    student.show_details()

elif choice == 5:
    teacher.show_details()