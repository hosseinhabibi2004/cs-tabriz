# Main
START_NEW_USER = """START_NEW_USER

bot_name: {bot_name}
full_name: {full_name}"""
START_EXISTED_USER = """START_EXISTED_USER

bot_name: {bot_name}
full_name: {full_name}"""
BACK_MAIN_MENU = "BACK_MAIN_MENU"

# Freshman
FRESHMAN_MENU = "FRESHMAN_MENU"
FRESHMAN_REGISTER = "FRESHMAN_REGISTER"

# Course
COURSE_MENU = "COURSE_MENU"
COURSES_BY_SEMESTER_MENU = "COURSES_BY_SEMESTER_MENU"
SEMESTER_COURSES_MENU = """SEMESTER_COURSES_MENU

offering_semester: {offering_semester}"""
COURSES_BY_TYPE_MENU = "COURSES_BY_TYPE_MENU"
TYPE_COURSES_MENU = """TYPE_COURSES_MENU

course_type: {course_type}"""
COURSE_DETAILS = """COURSE_DETAILS

fa_title: {fa_title}
en_title: {en_title}
offering_semester: {offering_semester}
credit: {credit}
quiz_credit: {quiz_credit}
prerequisite_course: {prerequisite_course}
unit_type: {unit_type}
course_type: {course_type}
has_exam: {has_exam}
has_project: {has_project}"""

# Place
GROUPS = "GROUPS"
GROUP_PLACES = """GROUP_PLACES

group: {group}"""

# Phone
PHONES = """PHONES

{phones}"""
PHONE_TEMPLATE = """PHONE_TEMPLATE
name: {name}
phone_number: {phone_number}"""

# Link
LINKS = """LINKS

{links}"""
LINK_TEMPLATE = """LINK_TEMPLATE
<a href="{address}">{name}</a>"""
