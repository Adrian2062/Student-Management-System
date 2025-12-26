from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Students, Subjects, Attendance, AttendanceReport, StudentResult, LeaveReportStudent, FeedBackStudent, NotificationStudent
from django.db.models import Q, Count, Avg

# ============================================================================
# STUDENT VIEWS - ALL DYNAMIC DATA
# ============================================================================

@login_required
def student_home(request):
    """Student Dashboard with dynamic data"""
    try:
        student = Students.objects.get(admin=request.user)
        
        # Get student's course and subjects
        course = student.course_id
        total_subjects = Subjects.objects.filter(course_id=course).count() if course else 0
        
        # Get attendance statistics
        total_attendance = AttendanceReport.objects.filter(student_id=student).count()
        present_attendance = AttendanceReport.objects.filter(student_id=student, status=True).count()
        absent_attendance = total_attendance - present_attendance
        attendance_percentage = round((present_attendance / total_attendance * 100), 2) if total_attendance > 0 else 0
        
        # Get total results/exams
        total_results = StudentResult.objects.filter(student_id=student).count()
        
        # Get pending leave requests
        pending_leaves = LeaveReportStudent.objects.filter(student_id=student, leave_status=0).count()
        
        # Get unread notifications
        unread_notifications = NotificationStudent.objects.filter(student_id=student).count()
        
        context = {
            'student': student,
            'total_subjects': total_subjects,
            'total_attendance': total_attendance,
            'present_attendance': present_attendance,
            'absent_attendance': absent_attendance,
            'attendance_percentage': attendance_percentage,
            'total_results': total_results,
            'pending_leaves': pending_leaves,
            'unread_notifications': unread_notifications,
        }
        
        return render(request, "student_template/student_home_content_v4.txt", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_view_attendance(request):
    """View attendance with subject selection"""
    try:
        student = Students.objects.get(admin=request.user)
        course = student.course_id
        
        # Get all subjects for the student's course
        subjects = Subjects.objects.filter(course_id=course)
        
        context = {
            'subjects': subjects,
        }
        
        return render(request, "student_template/student_view_attendance_v4.txt", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_view_attendance_post(request):
    """Process attendance view request"""
    if request.method != "POST":
        return redirect("student_view_attendance")
    
    try:
        student = Students.objects.get(admin=request.user)
        subject_id = request.POST.get("subject")
        subject = Subjects.objects.get(id=subject_id)
        
        # Get all attendance for this subject
        attendance_records = Attendance.objects.filter(subject_id=subject)
        
        # Get student's attendance reports for these records
        attendance_reports = AttendanceReport.objects.filter(
            student_id=student,
            attendance_id__in=attendance_records
        )
        
        # Calculate statistics
        total_count = attendance_reports.count()
        present_count = attendance_reports.filter(status=True).count()
        absent_count = total_count - present_count
        
        # Get all subjects for the dropdown
        course = student.course_id
        subjects = Subjects.objects.filter(course_id=course)
        
        context = {
            'subjects': subjects,
            'subject': subject,
            'total_count': total_count,
            'present_count': present_count,
            'absent_count': absent_count,
            'attendance_reports': attendance_reports,
        }
        
        return render(request, "student_template/student_view_attendance_v4.txt", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")
    except Subjects.DoesNotExist:
        messages.error(request, "Subject not found")
        return redirect("student_view_attendance")


@login_required
def student_view_result(request):
    """View all exam results"""
    try:
        student = Students.objects.get(admin=request.user)
        
        # Get all results for this student
        student_result = StudentResult.objects.filter(student_id=student).select_related('subject_id')
        
        context = {
            'student_result': student_result,
        }
        
        return render(request, "student_template/student_view_result_v4.txt", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_apply_leave(request):
    """Apply for leave"""
    try:
        student = Students.objects.get(admin=request.user)
        
        # Get all leave applications for this student
        leave_data = LeaveReportStudent.objects.filter(student_id=student).order_by('-created_at')
        
        context = {
            'leave_data': leave_data,
        }
        
        return render(request, "student_template/student_apply_leave.html", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_apply_leave_save(request):
    """Save leave application"""
    if request.method != "POST":
        return redirect("student_apply_leave")
    
    try:
        student = Students.objects.get(admin=request.user)
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_msg")  # Changed from leave_message to leave_msg
        
        # Validate inputs
        if not leave_date or not leave_message or leave_message.strip() == "":
            messages.error(request, "Please fill in all required fields")
            return redirect("student_apply_leave")
        
        leave_report = LeaveReportStudent(
            student_id=student,
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status=0  # Pending
        )
        leave_report.save()
        
        messages.success(request, "Leave application submitted successfully")
        return redirect("student_apply_leave")
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")
    except Exception as e:
        messages.error(request, f"Failed to submit leave application: {str(e)}")
        return redirect("student_apply_leave")


@login_required
def student_feedback(request):
    """View and submit feedback"""
    try:
        student = Students.objects.get(admin=request.user)
        
        # Get all feedback for this student
        feedback_data = FeedBackStudent.objects.filter(student_id=student).order_by('-created_at')
        
        context = {
            'feedback_data': feedback_data,
        }
        
        return render(request, "student_template/student_feedback.html", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_feedback_save(request):
    """Save student feedback"""
    if request.method != "POST":
        return redirect("student_feedback")
    
    try:
        student = Students.objects.get(admin=request.user)
        feedback_message = request.POST.get("feedback_msg")  # Changed from feedback_message to feedback_msg
        
        # Validate feedback is not empty
        if not feedback_message or feedback_message.strip() == "":
            messages.error(request, "Feedback message cannot be empty")
            return redirect("student_feedback")
        
        feedback = FeedBackStudent(
            student_id=student,
            feedback=feedback_message,
            feedback_reply=""
        )
        feedback.save()
        
        messages.success(request, "Feedback submitted successfully")
        return redirect("student_feedback")
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")
    except Exception as e:
        messages.error(request, f"Failed to submit feedback: {str(e)}")
        return redirect("student_feedback")


@login_required
def student_profile(request):
    """View and edit student profile"""
    try:
        student = Students.objects.get(admin=request.user)
        
        context = {
            'student': student,
        }
        
        return render(request, "student_template/student_profile.html", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_profile_update(request):
    """Update student profile"""
    if request.method != "POST":
        return redirect("student_profile")
    
    try:
        student = Students.objects.get(admin=request.user)
        
        # Update profile fields
        student.address = request.POST.get("address")
        student.gender = request.POST.get("gender")
        
        # Handle profile picture upload
        if request.FILES.get("profile_pic"):
            student.profile_pic = request.FILES["profile_pic"]
        
        student.save()
        
        messages.success(request, "Profile updated successfully")
        return redirect("student_profile")
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")
    except Exception as e:
        messages.error(request, f"Failed to update profile: {str(e)}")
        return redirect("student_profile")


@login_required
def student_view_notification(request):
    """View all notifications"""
    try:
        student = Students.objects.get(admin=request.user)
        
        # Get all notifications for this student
        notifications = NotificationStudent.objects.filter(student_id=student).order_by('-created_at')
        
        context = {
            'notifications': notifications,
        }
        
        return render(request, "student_template/student_notifications.html", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")


@login_required
def student_view_subjects(request):
    """View all subjects for the student's course"""
    try:
        student = Students.objects.get(admin=request.user)
        course = student.course_id
        
        # Get all subjects for this student's course
        subjects = Subjects.objects.filter(course_id=course)
        
        context = {
            'subjects': subjects,
            'course': course,
        }
        
        return render(request, "student_template/student_view_subjects.html", context)
    
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect("login")
