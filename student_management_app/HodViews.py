from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Staffs, Students, Courses, Subjects, SessionYearModel

def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method != "POST":
        return redirect("add_staff")
    
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    
    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
        user.staffs.address = address
        user.save()
        messages.success(request, "Staff Added Successfully!")
        return redirect("add_staff")
    except Exception as e:
        messages.error(request, "Failed to Add Staff: " + str(e))
        return redirect("add_staff")

def add_course(request):
    return render(request, "hod_template/add_course_template.html")

def add_course_save(request):
    if request.method != "POST":
        return redirect("add_course")
    
    course_name = request.POST.get("course")
    try:
        course = Courses(course_name=course_name)
        course.save()
        messages.success(request, "Course Added Successfully!")
        return redirect("add_course")
    except Exception as e:
        messages.error(request, "Failed to Add Course: " + str(e))
        return redirect("add_course")

def add_student(request):
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_template/add_student_template.html", {"courses": courses, "sessions": sessions})

def add_student_save(request):
    if request.method != "POST":
        return redirect("add_student")
    
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    gender = request.POST.get("gender")
    
    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
        user.students.address = address
        user.students.gender = gender
        
        course_obj = Courses.objects.get(id=course_id)
        user.students.course_id = course_obj
        
        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        user.students.session_year_id = session_year_obj
        
        user.save()
        messages.success(request, "Student Added Successfully!")
        return redirect("add_student")
    except Exception as e:
        messages.error(request, "Failed to Add Student: " + str(e))
        return redirect("add_student")

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html", {"courses": courses, "staffs": staffs})

def add_subject_save(request):
    if request.method != "POST":
         return redirect("add_subject")
         
    subject_name = request.POST.get("subject_name")
    course_id = request.POST.get("course")
    staff_id = request.POST.get("staff")
    
    try:
        course_obj = Courses.objects.get(id=course_id)
        staff_obj = CustomUser.objects.get(id=staff_id)
        subject = Subjects(subject_name=subject_name, course_id=course_obj, staff_id=staff_obj)
        subject.save()
        messages.success(request, "Subject Added Successfully!")
        return redirect("add_subject")
    except Exception as e:
        messages.error(request, "Failed to Add Subject: " + str(e))
        return redirect("add_subject")

def add_session(request):
    return render(request, "hod_template/add_session_template.html")

def add_session_save(request):
    if request.method != "POST":
        return redirect("add_session")

    session_start_year = request.POST.get("session_start")
    session_end_year = request.POST.get("session_end")

    try:
        session = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
        session.save()
        messages.success(request, "Session Year Added Successfully!")
        return redirect("add_session")
    except Exception as e:
        messages.error(request, "Failed to Add Session Year: " + str(e))
        return redirect("add_session")
