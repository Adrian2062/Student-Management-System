from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
from .models import *
admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(SessionYearModel)
