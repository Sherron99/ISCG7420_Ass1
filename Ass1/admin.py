from django.contrib import admin

from Ass1.models import Class, Semester, Lecturer, Student, StudentEnrolment, Course

# Register your models here.

#我们在admin界面创建这些模型
admin.site.register(Class)
admin.site.register(Semester)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(StudentEnrolment)
admin.site.register(Course)

