import os
import django
import sys
import random

# Setup Django environment
sys.path.append('c:\\Users\\AcerPredator\\Desktop\\django pw broadway')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management_system.settings")
django.setup()

from student_management_app.models import Students, Subjects, Courses, CustomUser

def seed_subjects():
    print("Seeding subjects...")
    
    # Get the first student to find their course
    try:
        student_user = CustomUser.objects.filter(user_type=3).first()
        if not student_user:
            print("No student user found.")
            return

        student = Students.objects.get(admin=student_user)
        course = student.course_id
        
        if not course:
            print(f"Student {student_user.username} has no course assigned.")
            return

        print(f"Checking subjects for Course: {course.course_name} (ID: {course.id})")
        
        existing_subjects = Subjects.objects.filter(course_id=course)
        if existing_subjects.exists():
            print(f"Course already has {existing_subjects.count()} subjects.")
            for s in existing_subjects:
                print(f" - {s.subject_name}")
            return

        # Create dummy subjects if none exist
        staff = CustomUser.objects.filter(user_type=2).first()
        if not staff:
            print("No staff user found to assign to subject. Please create a staff member first.")
            return

        subjects_to_create = ["Mathematics", "Physics", "Chemistry", "Computer Science"]
        
        for sub_name in subjects_to_create:
            subject = Subjects(
                subject_name=sub_name,
                course_id=course,
                staff_id=staff
            )
            subject.save()
            print(f"Created subject: {sub_name}")

        print("Successfully seeded subjects.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    seed_subjects()
