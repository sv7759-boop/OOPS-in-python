import html
import inspect
import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

import streamlit as st

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
DB_FILE = Path("school_data.json")  # same file as the CLI version
UNDO_LIMIT = 20
esc = html.escape

# newer Streamlit: width="stretch"; older: use_container_width=True
try:
    STRETCH = (
        {"width": "stretch"}
        if "width" in inspect.signature(st.button).parameters
        else {"use_container_width": True}
    )
except (TypeError, ValueError):
    STRETCH = {"use_container_width": True}


# ----------------------------------------------------------------------------
# Storage
# ----------------------------------------------------------------------------
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
    DB_FILE.write_text(snapshot(data), encoding="utf-8")


def snapshot(data):
    return json.dumps(data, indent=4)


# ----------------------------------------------------------------------------
# Models: same OOP structure, methods return (ok, message) instead of print()
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

    @abstractmethod
    def remove(self, data, key):
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
            return False, "That email doesn't look right."
        if self.find(data, roll_no):
            return False, "That roll number is already registered."
        data["students"].append(
            {"name": name, "age": age, "email": email, "roll_no": roll_no, "grades": {}}
        )
        save_data(data)
        return True, "Added {}".format(name)

    def find(self, data, roll_no):
        for s in data["students"]:
            if s["roll_no"] == roll_no:
                return s
        return None

    def remove(self, data, roll_no):
        s = self.find(data, roll_no)
        if not s:
            return False, "Student not found."
        data["students"].remove(s)
        save_data(data)
        return True, "Removed {}".format(s["name"])

    def add_grade(self, data, roll_no, subject, marks):
        s = self.find(data, roll_no)
        if not s:
            return False, "Student not found."
        if not subject:
            return False, "Enter a subject first."
        s.setdefault("grades", {})[subject] = marks
        save_data(data)
        return True, "Saved {}: {:g}".format(subject, marks)

    @staticmethod
    def average(student):
        grades = student.get("grades") or {}
        return sum(grades.values()) / len(grades) if grades else 0.0


class Teachers(Persons):
    def get_role(self):
        return "teacher"

    def register(self, data, name, age, email, emp_id, subject):
        if not name or not emp_id:
            return False, "Name and employee ID are required."
        if not self.validate_email(email):
            return False, "That email doesn't look right."
        if self.find(data, emp_id):
            return False, "That employee ID is already registered."
        data["teachers"].append(
            {"name": name, "age": age, "email": email, "emp_id": emp_id, "subject": subject}
        )
        save_data(data)
        return True, "Added {}".format(name)

    def find(self, data, emp_id):
        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                return t
        return None

    def remove(self, data, emp_id):
        t = self.find(data, emp_id)
        if not t:
            return False, "Teacher not found."
        data["teachers"].remove(t)
        save_data(data)
        return True, "Removed {}".format(t["name"])


student_svc = Students()
teacher_svc = Teachers()


# ----------------------------------------------------------------------------
# Styling: Apple design principles translated to CSS
#   - system font, size-specific tracking/leading, rem units
#   - translucent materials (header, sidebar, cards) that adapt to light/dark
#   - instant press feedback (:active), "materialize" entrance (blur + scale)
#   - reduced motion / reduced transparency / increased contrast
# ----------------------------------------------------------------------------
CSS = """
:root{
  --blue:#0A84FF;
  --green:#30D158;
  --orange:#FF9F0A;
  --fill:rgba(127,127,127,.10);
  --fill-strong:rgba(127,127,127,.18);
  --hairline:rgba(127,127,127,.24);
  --ease:cubic-bezier(.2,.9,.25,1);
}

/* ---- Typography: platform system font, optical sizing ---- */
.stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp button, .stApp li,
[data-testid="stToast"] p{
  font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI Variable Text","Segoe UI",system-ui,sans-serif !important;
  font-optical-sizing:auto;
}
.page-title,.name,.stat-value,.brand{
  font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI Variable Display","Segoe UI",system-ui,sans-serif;
}

/* ---- Canvas: soft static depth so translucent layers have something to blur ---- */
.stApp{
  background-image:
    radial-gradient(52rem 34rem at 8% -8%, rgba(10,132,255,.10), transparent 62%),
    radial-gradient(44rem 28rem at 100% 0%, rgba(191,90,242,.08), transparent 62%);
  background-attachment:fixed;
}
footer{visibility:hidden}
div.block-container,[data-testid="stMainBlockContainer"]{max-width:68rem;padding-top:4.5rem;padding-bottom:4rem}

/* ---- Materials: content scrolls under translucent chrome ---- */
header[data-testid="stHeader"]{
  background:rgba(127,127,127,.04) !important;
  -webkit-backdrop-filter:blur(20px) saturate(180%);
  backdrop-filter:blur(20px) saturate(180%);
}
section[data-testid="stSidebar"]{
  background:rgba(127,127,127,.11) !important;
  -webkit-backdrop-filter:blur(30px) saturate(180%);
  backdrop-filter:blur(30px) saturate(180%);
  border-right:1px solid var(--hairline);
}
section[data-testid="stSidebar"] > div{background:transparent !important}

.card{
  background:var(--fill);
  border:1px solid var(--hairline);
  border-radius:1.25rem;
  padding:1.5rem 1.75rem;
  box-shadow:0 .75rem 2.25rem rgba(0,0,0,.10);
  -webkit-backdrop-filter:blur(24px) saturate(160%);
  backdrop-filter:blur(24px) saturate(160%);
}

/* ---- Hierarchy: weight + size + leading as a set ---- */
.page-title{font-size:clamp(2rem,4.2vw,2.8rem);font-weight:700;line-height:1.05;letter-spacing:-.025em;margin:0 0 .3rem}
.page-sub{font-size:1rem;line-height:1.4;opacity:.72;margin-bottom:1.5rem}
.brand{font-size:1.3rem;font-weight:700;line-height:1.1;letter-spacing:-.015em;margin:.25rem 0 1rem}
.side-note{font-size:.78rem;line-height:1.4;letter-spacing:.01em;opacity:.72;margin:.4rem .1rem}
.section-title{font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.72;margin:1.25rem 0 .6rem}
.section-title.loose{margin-top:1.75rem}

.person{display:flex;gap:1.1rem;align-items:center}
.name{font-size:1.75rem;font-weight:700;line-height:1.1;letter-spacing:-.02em}
.meta{font-size:.92rem;line-height:1.4;opacity:.75;margin-top:.3rem;word-break:break-word}
.avatar{width:4rem;height:4rem;flex:none;border-radius:50%;display:grid;place-items:center;
  color:#fff;font-weight:600;font-size:1.4rem;letter-spacing:.01em;box-shadow:0 .3rem .9rem rgba(0,0,0,.2)}

.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:1.4rem 0 .25rem;
  border-top:1px solid var(--hairline);border-bottom:1px solid var(--hairline)}
.stat{padding:1rem .25rem;min-width:0}
.stat + .stat{border-left:1px solid var(--hairline);padding-left:1.25rem}
.stat-label{font-size:.72rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.72}
.stat-value{font-size:1.75rem;font-weight:700;line-height:1.15;letter-spacing:-.02em;margin-top:.25rem;
  font-variant-numeric:tabular-nums;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stat-value.text{font-size:1.2rem;line-height:1.7;letter-spacing:-.01em}

.grade{display:grid;grid-template-columns:minmax(5rem,9rem) 1fr 3.25rem;gap:.9rem;align-items:center;padding:.5rem 0}
.g-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:500}
.g-val{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
.bar{height:.5rem;border-radius:999px;background:rgba(127,127,127,.22);overflow:hidden}
.bar > i{display:block;height:100%;border-radius:inherit;transform-origin:left center}

.empty{padding:2.25rem 1rem;text-align:center;line-height:1.45;opacity:.78}
.empty b{display:block;font-size:1.15rem;letter-spacing:-.01em;margin-bottom:.25rem}

.hint{font-size:.8rem;line-height:1.35;letter-spacing:.01em;opacity:.85;margin:-.15rem 0 .6rem}
.hint::before{content:"";display:inline-block;width:.45rem;height:.45rem;border-radius:50%;
  background:var(--orange);margin-right:.45rem;vertical-align:middle}

/* ---- Motion: materialize (blur + scale together), only when content changes ---- */
@keyframes materialize{from{opacity:0;transform:scale(.985);filter:blur(8px)}to{opacity:1;transform:none;filter:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.card.enter{animation:materialize .32s var(--ease) both}
.card.enter .bar > i{animation:grow .55s var(--ease) both}

/* ---- Controls: feedback on press, not on release ---- */
.stButton > button{
  border-radius:.8rem;border:1px solid var(--hairline);background:var(--fill);
  font-weight:500;letter-spacing:0;
  transition:transform .12s var(--ease),background-color .12s ease-out,filter .12s ease-out;
}
.stButton > button:hover{background:var(--fill-strong)}
.stButton > button:active{transform:scale(.97);transition-duration:60ms}
.stButton > button:disabled{opacity:.45}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"]{
  background:var(--blue) !important;border-color:var(--blue) !important;color:#fff !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover{filter:brightness(1.08)}

div[data-baseweb="input"],div[data-baseweb="base-input"]{border-radius:.8rem !important}
div[data-baseweb="input"]:focus-within{border-color:var(--blue) !important;box-shadow:0 0 0 .2rem rgba(10,132,255,.28) !important}
[data-testid="stExpander"] details{border-radius:1rem;border-color:var(--hairline)}

/* ---- Accessibility: reduced motion, reduced transparency, increased contrast ---- */
@media (prefers-reduced-motion: reduce){
  .card.enter{animation:fadein .2s ease both}
  .card.enter .bar > i{animation:none}
  .stButton > button{transition:none}
  .stButton > button:active{transform:none}
}
@media (prefers-reduced-transparency: reduce){
  header[data-testid="stHeader"],section[data-testid="stSidebar"],.card{
    -webkit-backdrop-filter:none !important;backdrop-filter:none !important}
  section[data-testid="stSidebar"]{background:rgba(127,127,127,.22) !important}
  .card{background:rgba(127,127,127,.18)}
}
@media (prefers-contrast: more){
  :root{--hairline:rgba(127,127,127,.85)}
  .card{background:rgba(127,127,127,.2)}
  .bar{background:rgba(127,127,127,.4)}
}
"""


# ----------------------------------------------------------------------------
# Small UI helpers
# ----------------------------------------------------------------------------
def _h(*parts):
    # one line, no blank lines: Streamlit's markdown would otherwise break the HTML block
    return "".join(parts)


def page_header(title, subtitle):
    st.markdown(
        _h('<div class="page-title">', esc(title), '</div><div class="page-sub">', esc(subtitle), "</div>"),
        unsafe_allow_html=True,
    )


def hint(text):
    st.markdown(_h('<div class="hint">', esc(text), "</div>"), unsafe_allow_html=True)


def empty_state(title, text):
    st.markdown(
        _h('<div class="card"><div class="empty"><b>', esc(title), "</b>", esc(text), "</div></div>"),
        unsafe_allow_html=True,
    )


def avatar(name):
    parts = name.split()
    if not parts:
        initials = "?"
    elif len(parts) == 1:
        initials = parts[0][0]
    else:
        initials = parts[0][0] + parts[-1][0]
    hue = sum(ord(c) for c in name) % 360
    return _h(
        '<div class="avatar" style="background:linear-gradient(135deg,hsl(',
        str(hue), " 75% 62%),hsl(", str((hue + 40) % 360), ' 75% 48%))">', esc(initials.upper()), "</div>",
    )


def stat(label, value, text=False):
    return _h(
        '<div class="stat"><div class="stat-label">', esc(label),
        '</div><div class="stat-value', " text" if text else "", '">', esc(str(value)), "</div></div>",
    )


def tone(marks):
    if marks >= 75:
        return "#30D158"
    if marks >= 50:
        return "#0A84FF"
    return "#FF9F0A"


def mark_fresh(sig_key, sig):
    """True only when the content changed, so the entrance animation plays once, not on every rerun."""
    fresh = st.session_state.get(sig_key) != sig
    st.session_state[sig_key] = sig
    return fresh


def ensure_selection(items, id_field, sel_key):
    ids = [p[id_field] for p in items]
    if st.session_state.get(sel_key) not in ids:
        st.session_state[sel_key] = ids[0] if ids else None


# ----------------------------------------------------------------------------
# Callbacks (run before the script reruns, so the UI always shows fresh data)
# ----------------------------------------------------------------------------
def go(page):
    st.session_state["page"] = page
    st.session_state.pop("_sig_student", None)
    st.session_state.pop("_sig_teacher", None)


def select(key, value):
    st.session_state[key] = value


def push_undo(label, snap):
    stack = st.session_state.setdefault("undo", [])
    stack.append((label, snap))
    del stack[:-UNDO_LIMIT]


def undo():
    stack = st.session_state.get("undo") or []
    if not stack:
        return
    label, snap = stack.pop()
    DB_FILE.write_text(snap, encoding="utf-8")
    st.toast("Undid: {}".format(label), icon="↩️")


def add_student():
    ss = st.session_state
    data = load_data()
    snap = snapshot(data)
    name, roll = ss["ns_name"].strip(), ss["ns_roll"].strip()
    ok, msg = student_svc.register(data, name, int(ss["ns_age"]), ss["ns_email"].strip(), roll)
    if ok:
        push_undo("added {}".format(name), snap)
        ss["sel_student"] = roll
        ss["ns_name"], ss["ns_roll"], ss["ns_email"], ss["ns_age"] = "", "", "", 18
    st.toast(msg, icon="✅" if ok else "⚠️")


def add_teacher():
    ss = st.session_state
    data = load_data()
    snap = snapshot(data)
    name, emp = ss["nt_name"].strip(), ss["nt_emp"].strip()
    ok, msg = teacher_svc.register(
        data, name, int(ss["nt_age"]), ss["nt_email"].strip(), emp, ss["nt_subject"].strip()
    )
    if ok:
        push_undo("added {}".format(name), snap)
        ss["sel_teacher"] = emp
        ss["nt_name"], ss["nt_emp"], ss["nt_email"], ss["nt_subject"], ss["nt_age"] = "", "", "", "", 30
    st.toast(msg, icon="✅" if ok else "⚠️")


def save_grade(roll_no):
    ss = st.session_state
    data = load_data()
    snap = snapshot(data)
    subject = ss["gs_" + roll_no].strip()
    marks = float(ss["gm_" + roll_no])
    ok, msg = student_svc.add_grade(data, roll_no, subject, marks)
    if ok:
        push_undo("grade in {}".format(subject), snap)
        ss["gs_" + roll_no], ss["gm_" + roll_no] = "", 0.0
    st.toast(msg, icon="✅" if ok else "⚠️")


def remove_person(kind, key):
    svc = student_svc if kind == "student" else teacher_svc
    data = load_data()
    snap = snapshot(data)
    person = svc.find(data, key)
    ok, msg = svc.remove(data, key)
    if ok:
        push_undo("removed {}".format(person["name"]), snap)
    st.toast(msg, icon="🗑️" if ok else "⚠️")


# ----------------------------------------------------------------------------
# Shared directory list (search + selectable rows)
# ----------------------------------------------------------------------------
def directory(items, id_field, sel_key, query_key, placeholder):
    ss = st.session_state
    st.text_input("Search", key=query_key, placeholder=placeholder, label_visibility="collapsed")
    q = ss[query_key].strip().lower()
    shown = [p for p in items if q in p["name"].lower() or q in str(p[id_field]).lower()]
    for p in shown:
        pid = p[id_field]
        st.button(
            "{}  ·  {}".format(p["name"], pid),
            key="{}_{}".format(sel_key, pid),
            type="primary" if ss.get(sel_key) == pid else "secondary",
            on_click=select,
            args=(sel_key, pid),
            **STRETCH,
        )
    if items and not shown:
        hint("No match for “{}”.".format(ss[query_key].strip()))


# ----------------------------------------------------------------------------
# Students
# ----------------------------------------------------------------------------
def new_student_form(data):
    ss = st.session_state
    for k, v in (("ns_name", ""), ("ns_roll", ""), ("ns_email", ""), ("ns_age", 18)):
        ss.setdefault(k, v)

    st.text_input("Name", key="ns_name", placeholder="Full name")
    st.text_input("Roll number", key="ns_roll")
    st.number_input("Age", min_value=1, max_value=100, step=1, key="ns_age")
    st.text_input("Email", key="ns_email", placeholder="name@college.edu")

    roll, email = ss["ns_roll"].strip(), ss["ns_email"].strip()
    if roll and student_svc.find(data, roll):
        hint("That roll number is already registered.")
    if email and not Persons.validate_email(email):
        hint("Enter an email like name@college.edu.")

    st.button("Add student", type="primary", on_click=add_student, **STRETCH)


def student_detail(s):
    ss = st.session_state
    roll = s["roll_no"]
    grades = s.get("grades") or {}
    avg = Students.average(s)
    best = max(grades, key=grades.get) if grades else "—"

    fresh = mark_fresh("_sig_student", "{}|{}".format(roll, sorted(grades.items())))

    rows = ""
    for subject, marks in grades.items():
        pct = max(0.0, min(100.0, marks))
        rows += _h(
            '<div class="grade"><span class="g-name" title="', esc(subject), '">', esc(subject),
            '</span><div class="bar"><i style="width:', "{:g}".format(pct), "%;background:", tone(marks),
            '"></i></div><span class="g-val">', "{:g}".format(marks), "</span></div>",
        )
    if not rows:
        rows = '<div class="empty"><b>No grades yet</b>Add the first one below.</div>'

    st.markdown(
        _h(
            '<div class="card', " enter" if fresh else "", '">',
            '<div class="person">', avatar(s["name"]),
            '<div><div class="name">', esc(s["name"]), '</div><div class="meta">Roll ', esc(str(roll)),
            " · Age ", esc(str(s.get("age", "—"))), " · ", esc(s.get("email", "")), "</div></div></div>",
            '<div class="stats">',
            stat("Average", "{:.1f}".format(avg) if grades else "—"),
            stat("Subjects", len(grades)),
            stat("Top subject", best, text=True),
            "</div>",
            '<div class="section-title">Grades</div>', rows,
            "</div>",
        ),
        unsafe_allow_html=True,
    )

    # the control sits right under the thing it changes
    st.markdown('<div class="section-title loose">Add or update a grade</div>', unsafe_allow_html=True)
    ss.setdefault("gs_" + roll, "")
    ss.setdefault("gm_" + roll, 0.0)
    c1, c2, c3 = st.columns([5, 3, 3])
    c1.text_input("Subject", key="gs_" + roll, placeholder="Subject", label_visibility="collapsed")
    c2.number_input(
        "Marks", min_value=0.0, max_value=100.0, step=0.5, format="%.1f",
        key="gm_" + roll, label_visibility="collapsed",
    )
    subject = ss["gs_" + roll].strip()
    exists = subject in grades
    c3.button(
        "Update grade" if exists else "Save grade",
        type="primary", on_click=save_grade, args=(roll,), key="save_grade_" + roll, **STRETCH,
    )
    if exists:
        hint("Replaces the current {:g} in {}.".format(grades[subject], subject))

    with st.expander("More"):
        st.button("Remove student", on_click=remove_person, args=("student", roll), key="rm_s_" + roll, **STRETCH)
        st.caption("Changed your mind? Undo is in the sidebar.")


def students_page(data):
    items = data["students"]
    page_header("Students", "{} enrolled".format(len(items)))
    ensure_selection(items, "roll_no", "sel_student")

    left, right = st.columns([5, 7], gap="large")
    with left:
        directory(items, "roll_no", "sel_student", "q_student", "Search name or roll number")
        with st.expander("+ New student", expanded=not items):
            new_student_form(data)
    with right:
        s = student_svc.find(data, st.session_state.get("sel_student"))
        if s:
            student_detail(s)
        else:
            empty_state("No students yet", "Open “+ New student” to add the first one.")


# ----------------------------------------------------------------------------
# Teachers
# ----------------------------------------------------------------------------
def new_teacher_form(data):
    ss = st.session_state
    for k, v in (("nt_name", ""), ("nt_emp", ""), ("nt_subject", ""), ("nt_email", ""), ("nt_age", 30)):
        ss.setdefault(k, v)

    st.text_input("Name", key="nt_name", placeholder="Full name")
    st.text_input("Employee ID", key="nt_emp")
    st.text_input("Subject taught", key="nt_subject")
    st.number_input("Age", min_value=18, max_value=100, step=1, key="nt_age")
    st.text_input("Email", key="nt_email", placeholder="name@college.edu")

    emp, email = ss["nt_emp"].strip(), ss["nt_email"].strip()
    if emp and teacher_svc.find(data, emp):
        hint("That employee ID is already registered.")
    if email and not Persons.validate_email(email):
        hint("Enter an email like name@college.edu.")

    st.button("Add teacher", type="primary", on_click=add_teacher, **STRETCH)


def teacher_detail(t):
    emp = t["emp_id"]
    fresh = mark_fresh("_sig_teacher", "{}|{}".format(emp, sorted(t.items())))

    st.markdown(
        _h(
            '<div class="card', " enter" if fresh else "", '">',
            '<div class="person">', avatar(t["name"]),
            '<div><div class="name">', esc(t["name"]), '</div><div class="meta">',
            esc(t.get("email", "")), "</div></div></div>",
            '<div class="stats">',
            stat("Subject", t.get("subject") or "—", text=True),
            stat("Employee ID", emp, text=True),
            stat("Age", t.get("age", "—")),
            "</div></div>",
        ),
        unsafe_allow_html=True,
    )

    with st.expander("More"):
        st.button("Remove teacher", on_click=remove_person, args=("teacher", emp), key="rm_t_" + emp, **STRETCH)
        st.caption("Changed your mind? Undo is in the sidebar.")


def teachers_page(data):
    items = data["teachers"]
    page_header("Teachers", "{} on staff".format(len(items)))
    ensure_selection(items, "emp_id", "sel_teacher")

    left, right = st.columns([5, 7], gap="large")
    with left:
        directory(items, "emp_id", "sel_teacher", "q_teacher", "Search name or employee ID")
        with st.expander("+ New teacher", expanded=not items):
            new_teacher_form(data)
    with right:
        t = teacher_svc.find(data, st.session_state.get("sel_teacher"))
        if t:
            teacher_detail(t)
        else:
            empty_state("No teachers yet", "Open “+ New teacher” to add the first one.")


# ----------------------------------------------------------------------------
# App shell
# ----------------------------------------------------------------------------
def sidebar():
    page = st.session_state["page"]
    with st.sidebar:
        st.markdown('<div class="brand">School</div>', unsafe_allow_html=True)
        for name in ("Students", "Teachers"):
            st.button(
                name,
                key="nav_" + name,
                type="primary" if page == name else "secondary",
                on_click=go,
                args=(name,),
                **STRETCH,
            )

        stack = st.session_state.get("undo") or []
        st.markdown('<div class="section-title loose">History</div>', unsafe_allow_html=True)
        st.button("Undo last change", key="undo_btn", disabled=not stack, on_click=undo, **STRETCH)
        if stack:
            st.markdown(
                _h('<div class="side-note">Last: ', esc(stack[-1][0]), "</div>"), unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="side-note">Nothing to undo yet.</div>', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="School", page_icon="🎓", layout="wide")
    st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)
    st.session_state.setdefault("page", "Students")

    data = load_data()
    sidebar()

    if st.session_state["page"] == "Students":
        students_page(data)
    else:
        teachers_page(data)


main()
