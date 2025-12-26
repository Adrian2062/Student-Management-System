from django.shortcuts import render, redirect
from django.http import HttpResponse
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
        user.staffs.save()
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
    return render(request, "hod_template/add_student_template_v4.txt", {"courses": courses, "sessions": sessions})

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
        
        course_obj = Courses.objects.get(id=course_id)
        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        
        # Create Student Profile
        Students.objects.create(admin=user, address=address, gender=gender, course_id=course_obj, session_year_id=session_year_obj)
        
        # user.save() is not needed as create_user already saves the user
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

def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)

def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, "hod_template/manage_student_template_v4.txt", context)

def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "hod_template/manage_course_template.html", context)

def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, "hod_template/manage_subject_template.html", context)


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    context = {
        "student": student,
        "courses": courses,
        "sessions": sessions,
        "id": student_id
    }
    return render(request, "hod_template/edit_student_template_v4.txt", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
             return redirect("manage_student")
            
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        session_year_id = request.POST.get("session_year")
        course_id = request.POST.get("course")
        gender = request.POST.get("gender")

        try:
            # Updating Custom User Model
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            # Updating Student Model
            student = Students.objects.get(admin=student_id)
            student.address = address
            student.gender = gender
            
            course_obj = Courses.objects.get(id=course_id)
            student.course_id = course_obj
            
            session_year_obj = SessionYearModel.objects.get(id=session_year_id)
            student.session_year_id = session_year_obj
            
            student.save()
            messages.success(request, "Student Updated Successfully!")
            return redirect("edit_student", student_id=student_id)
        except Exception as e:
            messages.error(request, "Failed to Update Student: " + str(e))
            return redirect("edit_student", student_id=student_id)

def edit_staff(request, staff_id):
    request.session['staff_id'] = staff_id
    staff = Staffs.objects.get(admin=staff_id)
    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)

def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    
    staff_id = request.session.get("staff_id")
    if staff_id == None:
        return redirect("manage_staff")
    
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    address = request.POST.get("address")
    
    try:
        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        
        staff = Staffs.objects.get(admin=staff_id)
        staff.address = address
        staff.save()
        
        messages.success(request, "Staff Updated Successfully!")
        return redirect("edit_staff", staff_id=staff_id)
    except Exception as e:
        messages.error(request, "Failed to Update Staff: " + str(e))
        return redirect("edit_staff", staff_id=staff_id)

def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, "hod_template/edit_course_template.html", context)

def edit_course_save(request):
    if request.method != "POST":
         return HttpResponse("<h2>Method Not Allowed</h2>")
    
    course_id = request.POST.get("course_id")
    course_name = request.POST.get("course")
    
    try:
        course = Courses.objects.get(id=course_id)
        course.course_name = course_name
        course.save()
        
        messages.success(request, "Course Updated Successfully!")
        return redirect("edit_course", course_id=course_id)
    except Exception as e:
        messages.error(request, "Failed to Update Course: " + str(e))
        return redirect("edit_course", course_id=course_id)

def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, "hod_template/edit_subject_template.html", context)

def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    
    subject_id = request.POST.get("subject_id")
    subject_name = request.POST.get("subject_name")
    course_id = request.POST.get("course")
    staff_id = request.POST.get("staff")
    
    try:
        subject = Subjects.objects.get(id=subject_id)
        subject.subject_name = subject_name
        
        course_obj = Courses.objects.get(id=course_id)
        subject.course_id = course_obj
        
        staff_obj = CustomUser.objects.get(id=staff_id)
        subject.staff_id = staff_obj
        
        subject.save()
        
        messages.success(request, "Subject Updated Successfully!")
        return redirect("edit_subject", subject_id=subject_id)
    except Exception as e:
        messages.error(request, "Failed to Update Subject: " + str(e))
        return redirect("edit_subject", subject_id=subject_id)
