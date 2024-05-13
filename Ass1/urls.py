from django.urls import path

from Ass1 import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registerStudent/', views.registerStudent, name='registerStudent'),
    path('registerLecturer/', views.registerLecturer, name='registerLecturer'),
    path('updateLecturer/<int:id>/', views.updateLecturer, name='updateLecturer'),
    path('updateStudent/<int:id>/', views.updateStudent, name='updateStudent'),
    path('deleteStudent/<int:id>/', views.deleteStudent, name='deleteStudent'),
    path('deleteLecturer/<int:id>/', views.deleteLecturer, name='deleteLecturer'),
    path('showLecturer/<int:id>/', views.showLecturer, name='showLecturer'),
    path('showStudent/<int:id>/', views.showStudent, name='showStudent'),
    path('showStudents/', views.showStudents, name='showStudents'),
    path('showLecturers/', views.showLecturers, name='showLecturers'),
    path('showSemester/<int:id>/', views.showSemester, name='showSemester'),
    path('showSemesters/', views.showSemesters, name='showSemesters'),
    path('updateSemester/<int:id>/', views.updateSemester, name='updateSemester'),
    path('deleteSemester/<int:id>/', views.deleteSemester, name='deleteSemester'),
    path('createSemester/', views.createSemester, name='createSemester'),
    path('createCourse/', views.createCourse, name='createCourse'),
    path('showCourses/', views.showCourses, name='showCourses'),
    path('showCourse/<int:id>/', views.showCourse, name='showCourse'),
    path('updateCourse/<int:id>/', views.updateCourse, name='updateCourse'),
    path('deleteCourse/<int:id>/', views.deleteCourse, name='deleteCourse'),
    path('showClasses/', views.showClasses, name='showClasses'),
    path('createClass/', views.createClass, name='createClass'),
    path('showClass/<int:id>/', views.showClass, name='showClass'),
    path('updateClass/<int:id>/', views.updateClass, name='updateClass'),
    path('deleteClass/<int:id>/', views.deleteClass, name='deleteClass'),
    path('assignLecturerToClass/', views.assignLecturerToClass, name='assignLecturerToClass'),
    path('AssignALecturerToThisClass/<int:id>/', views.AssignALecturerToThisClass, name='AssignALecturerToThisClass'),
    path('saveAndShowClassesWithLecturer/<int:id>/', views.saveAndShowClassesWithLecturer, name='saveAndShowClassesWithLecturer'),
    path('removeLecturerFromClass/', views.removeLecturerFromClass, name='removeLecturerFromClass'),
    path('removeLecturer/<int:id>/', views.removeLecturer, name='removeLecturer'),
    # path('RemoveALecturerFromThisClass/', views.RemoveALecturerFromThisClass, name='RemoveALecturerFromThisClass'),
    path('removeLecturerFromAClass/<int:id>/', views.removeLecturerFromAClass, name='removeLecturerFromAClass'),
    # path('removeLecturer/<int:id>/', views.removeLecturer, name='removeLecturer'),
    path('showLecturerToClass/', views.showLecturerToClass, name='showLecturerToClass'),
    path('showTheLecturerDetail', views.showTheLecturerDetail, name='showTheLecturerDetail'),
    path('showAllStudents', views.showAllStudents, name='showAllStudents'),
    path('showTheStudentDetail/', views.showTheStudentDetail, name='showTheStudentDetail'),
    path('submitEnrolment/<int:id>/', views.submitEnrolment, name='submitEnrolment'),
    path('send_email_out/', views.send_email_out, name='send_email_out'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('showAllStudentsClasses/', views.showAllStudentsClasses, name='showAllStudentsClasses'),
    path('showStudentClasses/', views.showStudentClasses, name='showStudentClasses'),
    path('showAllStudentstoRemoveClasses/', views.showAllStudentstoRemoveClasses, name='showAllStudentstoRemoveClasses'),
    path('removeClasses/', views.removeClasses, name='removeClasses'),
    path('updateTheStudentClasses/<int:id>/', views.updateTheStudentClasses, name='updateTheStudentClasses'),
]