from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Students, Subjects, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult

def student_view_attendance(request):
    student_obj = Students.objects.get(admin=request.user.id)
    course = student_obj.course_id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance.html", {"subjects": subjects})

def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    student_obj = Students.objects.get(admin=request.user.id)
    subject = Subjects.objects.get(id=subject_id)
    
    attendance = Attendance.objects.filter(subject_id=subject)
    attendance_reports = AttendanceReport.objects.filter(student_id=student_obj, attendance_id__in=attendance)
    
    present_count = attendance_reports.filter(status=True).count()
    absent_count = attendance_reports.filter(status=False).count()
    
    return render(request, "student_template/student_view_attendance.html", {
        "subjects": Subjects.objects.filter(course_id=student_obj.course_id),
        "present_count": present_count,
        "absent_count": absent_count,
        "total_count": present_count + absent_count
    })

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_apply_leave.html", {"leave_data": leave_data})

def student_apply_leave_save(request):
    if request.method != "POST":
        return redirect("student_apply_leave")
    
    leave_date = request.POST.get("leave_date")
    leave_msg = request.POST.get("leave_msg")
    
    student_obj = Students.objects.get(admin=request.user.id)
    try:
        leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
        leave_report.save()
        messages.success(request, "Leave Application Sent Successfully")
        return redirect("student_apply_leave")
    except:
        messages.error(request, "Failed to Send Leave Application")
        return redirect("student_apply_leave")

def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_feedback.html", {"feedback_data": feedback_data})

def student_feedback_save(request):
    if request.method != "POST":
        return redirect("student_feedback")
    
    feedback_msg = request.POST.get("feedback_msg")
    
    student_obj = Students.objects.get(admin=request.user.id)
    try:
        feedback = FeedBackStudent(student_id=student_obj, feedback=feedback_msg, feedback_reply="")
        feedback.save()
        messages.success(request, "Feedback Sent Successfully")
        return redirect("student_feedback")
    except:
        messages.error(request, "Failed to Send Feedback")
        return redirect("student_feedback")

def student_view_result(request):
    student_obj = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_view_result.html", {"student_result": student_result})
