import os
import django
import sys

# Setup Django environment
sys.path.append('c:\\Users\\AcerPredator\\Desktop\\django pw broadway')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management_system.settings")
django.setup()

from student_management_app.models import Students, Subjects, Courses, CustomUser, SessionYearModel

def check_data():
    print("--- Checking Courses ---")
    courses = Courses.objects.all()
    for c in courses:
        print(f"Course ID: {c.id}, Name: {c.course_name}")
    
    print("\n--- Checking Subjects ---")
    subjects = Subjects.objects.all()
    for s in subjects:
        print(f"Subject ID: {s.id}, Name: {s.subject_name}, Course ID: {s.course_id.id}")

    print("\n--- Checking Students ---")
    students = Students.objects.all()
    for s in students:
        course_name = s.course_id.course_name if s.course_id else "None"
        course_id = s.course_id.id if s.course_id else "None"
        print(f"Student: {s.admin.first_name} {s.admin.last_name}, Course: {course_name} (ID: {course_id})")

if __name__ == '__main__':
    check_data()
