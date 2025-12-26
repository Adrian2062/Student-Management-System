
import os

BASE_DIR = r"c:\Users\AcerPredator\Desktop\django pw broadway\student_management_app\templates\hod_template"

# Strings are carefully constructed to ensure single lines where needed for Django templates

edit_student_content = """{% extends 'base_template.html' %}
{% block page_title %}Edit Student{% endblock page_title %}
{% block main_content %}
<section class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-12">
                <div class="card card-primary">
                    <div class="card-header">
                        <h3 class="card-title">Edit Student</h3>
                    </div>
                    <form role="form" action="{% url 'edit_student_save' %}" method="post">
                        {% csrf_token %}
                        <div class="card-body">
                            <div class="form-group">
                                <label>Email address</label>
                                <input type="email" class="form-control" name="email" value="{{ student.admin.email }}">
                            </div>
                            <div class="form-group">
                                <label>First Name</label>
                                <input type="text" class="form-control" name="first_name" value="{{ student.admin.first_name }}">
                            </div>
                            <div class="form-group">
                                <label>Last Name</label>
                                <input type="text" class="form-control" name="last_name" value="{{ student.admin.last_name }}">
                            </div>
                            <div class="form-group">
                                <label>Username</label>
                                <input type="text" class="form-control" name="username" value="{{ student.admin.username }}">
                            </div>
                            <div class="form-group">
                                <label>Address</label>
                                <input type="text" class="form-control" name="address" value="{{ student.address }}">
                            </div>
                            <div class="form-group">
                                <label>Gender</label>
                                <select class="form-control" name="gender">
                                    <option value="Male" {% if student.gender == "Male" %}selected{% endif %}>Male</option>
                                    <option value="Female" {% if student.gender == "Female" %}selected{% endif %}>Female</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Course</label>
                                <select class="form-control" name="course">
                                    {% for course in courses %}
                                    <option value="{{ course.id }}" {% if student.course_id.id == course.id %}selected{% endif %}>{{ course.course_name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Session Year</label>
                                <select class="form-control" name="session_year">
                                    {% for session in sessions %}
                                    <option value="{{ session.id }}" {% if student.session_year_id.id == session.id %}selected{% endif %}>{{ session.session_start_year|date:"Y" }} to {{ session.session_end_year|date:"Y" }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="form-group">
                                {% if messages %}
                                {% for message in messages %}
                                {% if message.tags == 'error' %}
                                <div class="alert alert-danger" style="margin-top:10px">{{ message }}</div>
                                {% endif %}
                                {% if message.tags == 'success' %}
                                <div class="alert alert-success" style="margin-top:10px">{{ message }}</div>
                                {% endif %}
                                {% endfor %}
                                {% endif %}
                            </div>
                        </div>
                        <div class="card-footer">
                            <button type="submit" class="btn btn-primary">Save Student</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock main_content %}
{% block sidebar_menu %}{% include 'hod_template/sidebar_template.html' %}{% endblock sidebar_menu %}
"""

manage_student_content = """{% extends 'base_template.html' %}
{% block page_title %}Manage Student{% endblock page_title %}
{% block main_content %}
<section class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Student Details</h3>
                        <div class="card-tools">
                            <div class="input-group input-group-sm" style="width: 150px;">
                                <input type="text" name="table_search" class="form-control float-right" placeholder="Search">
                                <div class="input-group-append">
                                    <button type="submit" class="btn btn-default"><i class="fas fa-search"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- /.card-header -->
                    <div class="card-body table-responsive p-0">
                        <table class="table table-hover text-nowrap">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>First Name</th>
                                    <th>Last Name</th>
                                    <th>Username</th>
                                    <th>Email</th>
                                    <th>Address</th>
                                    <th>Gender</th>
                                    <th>Course</th>
                                    <th>Session Year</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for student in students %}
                                <tr>
                                    <td>{{ student.admin.id }}</td>
                                    <td>{{ student.admin.first_name }}</td>
                                    <td>{{ student.admin.last_name }}</td>
                                    <td>{{ student.admin.username }}</td>
                                    <td>{{ student.admin.email }}</td>
                                    <td>{{ student.address|default:"None" }}</td>
                                    <td>{{ student.gender|default:"None" }}</td>
                                    <td>{{ student.course_id.course_name|default:"None" }}</td>
                                    <td>
                                        {% if student.session_year_id %}
                                        {{ student.session_year_id.session_start_year|date:"Y" }} to {{ student.session_year_id.session_end_year|date:"Y" }}
                                        {% else %}
                                        None
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'edit_student' student.admin.id %}" class="btn btn-success">Edit</a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>
        </div>
    </div>
</section>
{% endblock main_content %}
{% block sidebar_menu %}{% include 'hod_template/sidebar_template.html' %}{% endblock sidebar_menu %}
"""

add_student_content = """{% extends 'base_template.html' %}
{% block page_title %}Add Student{% endblock page_title %}
{% block main_content %}
<section class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-12">
                <!-- general form elements -->
                <div class="card card-primary">
                    <div class="card-header">
                        <h3 class="card-title">Add Student</h3>
                    </div>
                    <!-- /.card-header -->
                    <!-- form start -->
                    <form role="form" action="{% url 'add_student_save' %}" method="post">
                        {% csrf_token %}
                        <div class="card-body">
                            <div class="form-group">
                                <label>Email address</label>
                                <input type="email" class="form-control" name="email" placeholder="Enter email" required>
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" class="form-control" name="password" placeholder="Password" required>
                            </div>
                            <div class="form-group">
                                <label>First Name</label>
                                <input type="text" class="form-control" name="first_name" placeholder="First Name" required>
                            </div>
                            <div class="form-group">
                                <label>Last Name</label>
                                <input type="text" class="form-control" name="last_name" placeholder="Last Name" required>
                            </div>
                            <div class="form-group">
                                <label>Username</label>
                                <input type="text" class="form-control" name="username" placeholder="Username" required>
                            </div>
                            <div class="form-group">
                                <label>Address</label>
                                <input type="text" class="form-control" name="address" placeholder="Address" required>
                            </div>
                            <div class="form-group">
                                <label>Gender</label>
                                <select class="form-control" name="gender">
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Course</label>
                                <select class="form-control" name="course">
                                    {% for course in courses %}
                                    <option value="{{ course.id }}">{{ course.course_name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Session Year</label>
                                <select class="form-control" name="session_year">
                                    {% for session in sessions %}
                                    <option value="{{ session.id }}">{{ session.session_start_year|date:"Y" }} to {{ session.session_end_year|date:"Y" }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="form-group">
                                {% if messages %}
                                {% for message in messages %}
                                {% if message.tags == 'error' %}
                                <div class="alert alert-danger" style="margin-top:10px">{{ message }}</div>
                                {% endif %}
                                {% if message.tags == 'success' %}
                                <div class="alert alert-success" style="margin-top:10px">{{ message }}</div>
                                {% endif %}
                                {% endfor %}
                                {% endif %}
                            </div>
                        </div>
                        <!-- /.card-body -->
                        <div class="card-footer">
                            <button type="submit" class="btn btn-primary">Add Student</button>
                        </div>
                    </form>
                </div>
                <!-- /.card -->
            </div>
        </div>
    </div>
</section>
{% endblock main_content %}
{% block sidebar_menu %}
{% include 'hod_template/sidebar_template.html' %}
{% endblock sidebar_menu %}
"""

files_to_fix = {
    "edit_student_template_v3.html": edit_student_content,
    "manage_student_template_v3.html": manage_student_content,
    "add_student_template_v3.html": add_student_content
}

for filename, content in files_to_fix.items():
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Overwrote {filename}")
