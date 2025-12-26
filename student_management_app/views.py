from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .models import CustomUser, AdminHOD, Staffs, Students, Courses, Subjects

def ShowLogin(request):
    return render(request, "login_page.html")

def DoLogin(request):
    if request.method != "POST":
        return render(request, "login_page.html")
    
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        # Find user by email
        user_obj = CustomUser.objects.get(email=email)
        
        # Check if password is correct
        if not user_obj.check_password(password):
            messages.error(request, "Invalid password")
            return redirect("login")
        
        # Authenticate and login
        from django.contrib.auth import authenticate, login as auth_login
        user = authenticate(request, username=user_obj.username, password=password)
        
        if user is not None and user.is_active:
            auth_login(request, user)
            
            # Redirect based on user type
            user_type = str(user.user_type)  # Convert to string for comparison
            if user_type == "1":
                return redirect("admin_home")
            elif user_type == "2":
                return redirect("staff_home")
            elif user_type == "3":
                return redirect("student_home")
            else:
                return redirect("admin_home")
        else:
            messages.error(request, "Account is not active")
            return redirect("login")
            
    except CustomUser.DoesNotExist:
        messages.error(request, "No account found with this email")
        return redirect("login")
    except Exception as e:
        messages.error(request, f"Login error: {str(e)}")
        return redirect("login")

def GetUserTypeFromEmail(email):
    if "university.org" in email:
        return "1"
    elif "college.com" in email:
        return "2"
    elif "school.com" in email:
        return "3"
    else:
        return "3" # Default to student

def Registration(request):
    return render(request, "registration.html")

def DoRegistration(request):
    if request.method != "POST":
        return redirect("registration")
    
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email or login.")
            return redirect("registration")
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect("registration")
        
        user_type = GetUserTypeFromEmail(email)
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=user_type)
        user.save()
        
        # Profile creation is handled by signals in models.py
        # But for Student, we might need to be careful if signal passed 'pass'.
        if user_type == "3":
            # Manually create student if signal didn't (I commented it out in models)
            if not hasattr(user, 'students'):
                Students.objects.create(admin=user)
        
        messages.success(request, "Registration Successful")
        return redirect("login")
    except Exception as e:
        messages.error(request, f"Failed to Register: {e}")
        return redirect("registration")

def logout_user(request):
    logout(request)
    return redirect("login")

def admin_home(request):
    student_count = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    course_count = Courses.objects.all().count()
    subject_count = Subjects.objects.all().count()
    
    context = {
        "student_count": student_count,
        "staff_count": staff_count,
        "course_count": course_count,
        "subject_count": subject_count
    }
    return render(request, "hod_template/home_content.html", context)

def staff_home(request):
    return render(request, "staff_template/home_content.html")

# Student home is now handled by StudentViews.student_home
# Import it in urls.py as: from . import StudentViews
# And use: StudentViews.student_home
