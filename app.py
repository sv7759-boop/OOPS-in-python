import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# Storage (same school_data.json as the CLI version)
# ----------------------------------------------------------------------------
DB_FILE = Path("school_data.json")


def load_data():
    data = {"students": [], "teachers": []}
    if DB_FILE.exists():
        content = DB_FILE.read_text(encoding="utf-8").strip()
        if content:
            data = json.loads(content)
    data.setdefault("students", [])
    data.setdefault("teachers", [])
    return data


def save_data(data):
    DB_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


# ----------------------------------------------------------------------------
# Models (same OOP structure, but no input()/print() -> returns (ok, message))
# ----------------------------------------------------------------------------
class Persons(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def register(self, data, **fields):
        pass

    @abstractmethod
    def find(self, data, key):
        pass

    @staticmethod
    def validate_email(email):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


class Students(Persons):
    def get_role(self):
        return "student"

    def register(self, data, name, age, email, roll_no):
        if not name or not roll_no:
            return False, "Name and roll number are required."
        if not self.validate_email(email):
            return False, "Invalid email."
        if self.find(data, roll_no):
            return False, "Student already exists."

        data["students"].append({
            "name": name,
            "age": age,
            "email": email,
            "roll_no": roll_no,
            "grades": {},
        })
        save_data(data)
        return True, f"Student {name} with roll no. {roll_no} registered successfully!"

    def find(self, data, roll_no):
        for s in data["students"]:
            if s["roll_no"] == roll_no:
                return s
        return None

    def add_grade(self, data, roll_no, subject, marks):
        student = self.find(data, roll_no)
        if not student:
            return False, "Student not found."
        if not subject:
            return False, "Subject is required."
        student["grades"][subject] = marks
        save_data(data)
        return True, f"Grade added: {subject} = {marks}"

    @staticmethod
    def average(student):
        grades = student["grades"]
        return sum(grades.values()) / len(grades) if grades else 0.0


class Teachers(Persons):
    def get_role(self):
        return "teacher"

    def register(self, data, name, age, email, emp_id, subject):
        if not name or not emp_id:
            return False, "Name and employee ID are required."
        if not self.validate_email(email):
            return False, "Invalid email."
        if self.find(data, emp_id):
            return False, "Teacher already exists."

        data["teachers"].append({
            "name": name,
            "age": age,
            "email": email,
            "emp_id": emp_id,
            "subject": subject,
        })
        save_data(data)
        return True, f"Teacher {name} with employee ID {emp_id} registered successfully!"

    def find(self, data, emp_id):
        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                return t
        return None


student_svc = Students()
teacher_svc = Teachers()


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_dashboard(data):
    st.header("📊 Dashboard")

    c1, c2 = st.columns(2)
    c1.metric("Total students", len(data["students"]))
    c2.metric("Total teachers", len(data["teachers"]))

    tab_s, tab_t = st.tabs(["Students", "Teachers"])

    with tab_s:
        if data["students"]:
            df = pd.DataFrame([
                {
                    "Roll No": s["roll_no"],
                    "Name": s["name"],
                    "Age": s["age"],
                    "Email": s["email"],
                    "Subjects": len(s["grades"]),
                    "Average": round(Students.average(s), 1),
                }
                for s in data["students"]
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No students registered yet.")

    with tab_t:
        if data["teachers"]:
            df = pd.DataFrame([
                {
                    "Emp ID": t["emp_id"],
                    "Name": t["name"],
                    "Age": t["age"],
                    "Email": t["email"],
                    "Subject": t["subject"],
                }
                for t in data["teachers"]
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No teachers registered yet.")


def page_register_student(data):
    st.header("🎓 Register Student")

    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=18, step=1)
        email = st.text_input("Email")
        roll_no = st.text_input("Roll number")
        submitted = st.form_submit_button("Register student", type="primary")

    if submitted:
        ok, msg = student_svc.register(
            data, name.strip(), int(age), email.strip(), roll_no.strip()
        )
        (st.success if ok else st.error)(msg)


def page_register_teacher(data):
    st.header("👩‍🏫 Register Teacher")

    with st.form("teacher_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
        email = st.text_input("Email")
        emp_id = st.text_input("Employee ID")
        subject = st.text_input("Subject taught")
        submitted = st.form_submit_button("Register teacher", type="primary")

    if submitted:
        ok, msg = teacher_svc.register(
            data, name.strip(), int(age), email.strip(), emp_id.strip(), subject.strip()
        )
        (st.success if ok else st.error)(msg)


def page_add_grade(data):
    st.header("📝 Add Grade")

    if not data["students"]:
        st.info("No students registered yet. Register a student first.")
        return

    names = {s["roll_no"]: s["name"] for s in data["students"]}

    with st.form("grade_form", clear_on_submit=True):
        roll_no = st.selectbox(
            "Student",
            options=list(names.keys()),
            format_func=lambda r: f"{r} — {names[r]}",
        )
        subject = st.text_input("Subject")
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        submitted = st.form_submit_button("Add grade", type="primary")

    if submitted:
        ok, msg = student_svc.add_grade(data, roll_no, subject.strip(), float(marks))
        (st.success if ok else st.error)(msg)
        if ok:
            st.caption("If the subject already existed, its marks were updated.")


def page_student_details(data):
    st.header("🔍 Student Details")

    if not data["students"]:
        st.info("No students registered yet.")
        return

    names = {s["roll_no"]: s["name"] for s in data["students"]}
    roll_no = st.selectbox(
        "Select student",
        options=list(names.keys()),
        format_func=lambda r: f"{r} — {names[r]}",
    )

    student = student_svc.find(data, roll_no)
    if not student:
        st.error("Student not found.")
        return

    st.subheader(student["name"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Roll no", student["roll_no"])
    c2.metric("Age", student["age"])
    c3.metric("Average", f"{Students.average(student):.1f}")
    st.write(f"**Email:** {student['email']}")

    st.markdown("#### Grades")
    if student["grades"]:
        gdf = pd.DataFrame(
            {"Subject": list(student["grades"].keys()),
             "Marks": list(student["grades"].values())}
        )
        col_a, col_b = st.columns([1, 2])
        col_a.dataframe(gdf, use_container_width=True, hide_index=True)
        col_b.bar_chart(gdf.set_index("Subject"))
    else:
        st.info("No grades added yet.")


def page_teacher_details(data):
    st.header("🔍 Teacher Details")

    if not data["teachers"]:
        st.info("No teachers registered yet.")
        return

    names = {t["emp_id"]: t["name"] for t in data["teachers"]}
    emp_id = st.selectbox(
        "Select teacher",
        options=list(names.keys()),
        format_func=lambda e: f"{e} — {names[e]}",
    )

    teacher = teacher_svc.find(data, emp_id)
    if not teacher:
        st.error("Teacher not found.")
        return

    st.subheader(teacher["name"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Employee ID", teacher["emp_id"])
    c2.metric("Age", teacher["age"])
    c3.metric("Subject", teacher["subject"] or "—")
    st.write(f"**Email:** {teacher['email']}")


# ----------------------------------------------------------------------------
# App
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Student Management System", page_icon="🏫", layout="wide")
st.title("🏫 Student Management System")

PAGES = {
    "📊 Dashboard": page_dashboard,
    "🎓 Register Student": page_register_student,
    "👩‍🏫 Register Teacher": page_register_teacher,
    "📝 Add Grade": page_add_grade,
    "🔍 Student Details": page_student_details,
    "🔍 Teacher Details": page_teacher_details,
}

choice = st.sidebar.radio("Navigation", list(PAGES.keys()))

# reload from disk on every rerun so the UI always matches the JSON file
PAGES[choice](load_data())
