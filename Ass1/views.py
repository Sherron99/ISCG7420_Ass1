from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.urls import reverse

from Ass1.models import Semester, Course, Class, Student, StudentEnrolment, Lecturer


# Create your views here.
def index(request):
    return render(request, 'base.html')


# login 界面，检查用户输入账号和密码是否已创建和正确
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.groups.filter(name='Administrators').exists():
                return render(request, 'adminHome.html', {'user': user})
            elif user.groups.filter(name='Lecturers').exists():
                return render(request, 'lecturerHome.html', {'user': user})
            else:
                return render(request, 'studentHome.html', {'user': user})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)  # 当我们要退出界面的话，请注意，需要用Django内置的logout(request)执行登出操作。
    return redirect('login')


# def registerUser(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         role = request.POST.get('role')
#
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#
#         # 根据角色添加用户到相应的组
#         if role == 'Lecturer':
#             group_name = 'Lecturers'
#             Lecturer.objects.create(firstName=first_name, lastName=last_name, email=email)
#         elif role == 'Student':
#             group_name = 'Students'
#             Student.objects.create(firstName=first_name, lastName=last_name, email=email)
#         else:
#             group_name = 'Administrators'
#
#         # 获取或创建对应的组
#         group, created = Group.objects.get_or_create(name=group_name)
#         # group是第一个返回值。它是从数据库中获取的或新创建的 Group 对象的实例。无论是找到一个已存在的组还是新建了一个组，group 变量都会被赋值为该组的实例。
#         # created: 这是第二个返回值，一个布尔类型的变量。它指示 Group 对象是被创建还是已经存在：
#         # get_or_create 尝试获取一个已存在的数据库记录，或者在不存在时创建它
#         user.groups.add(group)
#
#         if role == 'Lecturer':
#             return redirect('showLecturers')
#         elif role == 'Student':
#             return redirect('showStudents')
#         else:
#             return redirect('login')  # 或者其他默认页面
#
#     return render(request, 'registerUser.html')

    # 1:
    #     if role == 'Lecturer':
    #         return HttpResponseRedirect(reverse('showLecturers')) #根据不同的角色，进入到相应的界面
    #     elif role == 'Student':
    #         return HttpResponseRedirect(reverse('showStudents'))
    #
    # return render(request, 'registerUser.html')


# 上面标注的1:是正确的，和没有被注释的代码都是可以使用的。只有用了redirect('')或者HttpResponseRedirect()才能更新界面
# 下面的标注2:是错误的，render并不能更新http界面，它只能将部分内容显示在界面上，但是并不能显示该界面。
# 2:
# if user.groups.filter(name='Lecturers').exists():
#     return render(request, 'showLecturers.html', {'user': user})
# elif user.groups.filter(name='Students').exists():
#     return render(request, 'showStudents.html', {'user': user})
# else:
#     return render(request, 'login.html', {'user': user})

def registerStudent(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        # Create User instance
        # Create User instance
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.groups.add(Group.objects.get(name='Students'))

        # Create Student instance
        student = Student.objects.create(firstName=first_name, lastName=last_name, email=email, DOB=dob)
        student.save() #遇到的问题是：我一开始只使用了user = User.objects.create_user()...但是没有对管理后台里的Student class进行创建。导致登陆了管理系统，Student列表一直没有显示数据

        # Add any other logic or redirects as needed
        return redirect('showStudents')

    # Render the registration form
    return render(request, 'registerStudent.html')

def registerLecturer(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        # Create User instance
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.groups.add(Group.objects.get(name='Lecturers'))

        # Create Student instance
        lecturer = Lecturer.objects.create(firstName=first_name, lastName=last_name, email=email, DOB=dob)
        lecturer.save()

        # Add any other logic or redirects as needed
        return redirect('showLecturers')

    # Render the registration form
    return render(request, 'registerStudent.html')


# 下面这串代码我是想显示出该用户的信息

def showLecturer(request, id):
    user = User.objects.get(id=id)
    return render(request, 'showStudent.html', {'user': user})


def updateLecturer(request, id):
    if request.method == 'POST':  # 这串代码非常重要，没有的话，直接显示User matching query does not exist.和method是get
        id = request.POST.get('id')
        print(id)
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        user = User.objects.get(id=id)
        user.username = username
        user.set_password(password)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.role = role

        user.save()
    return redirect('showLecturer', id=id)


def showStudent(request, id):
    user = User.objects.get(id=id)
    return render(request, 'showStudent.html', {'user': user})


def updateStudent(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        user.username = username
        user.set_password(password)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.role = role
        user.save()
        return redirect('showStudents')
    return render(request, 'showStudent.html', {'user': user})#因为showStudent用的是user，所以我们不用更改


def deleteStudent(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('showStudents')


def deleteLecturer(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('showLecturers')


def showStudents(request):
    users = User.objects.filter(groups__name='Students')
    return render(request, 'showStudents.html', {'users': users})


def showLecturers(request):
    users = User.objects.filter(groups__name='Lecturers')
    return render(request, 'showLecturers.html', {'users': users})


def showSemesters(request):
    semesters = Semester.objects.all()
    return render(request, 'showSemesters.html', {'semesters': semesters})


def showSemester(request, id):
    semester = Semester.objects.get(id=id)
    return render(request, 'showSemester.html', {'semester': semester})


def createSemester(request):
    if request.method == 'POST':
        year = request.POST.get('Year')
        semester = request.POST.get('Semester')
        semester = Semester(year=year, semester=semester)
        semester.save()
        return redirect('showSemesters')
    return render(request, 'createSemester.html')


def updateSemester(request, id):
    semester = Semester.objects.get(id=id)
    if request.method == 'POST':
        # id = request.POST.get('id')
        year = request.POST.get('Year')
        semesterr = request.POST.get('Semester')
        # semester = Semester.objects.get(id=id) 注释的id那行和这行我们用def下面的一行顶替了
        semester.year = year
        semester.semester = semesterr
        semester.save()
        return redirect('showSemesters')
    return render(request, 'showSemester.html', {'semester': semester})#context里的内容一定要和showSemester.html里的名字对应(semester.id)


def deleteSemester(request, id):
    semester = Semester.objects.get(id=id)
    semester.delete()
    return redirect('showSemesters')


def createCourse(request):
    if request.method == 'POST':
        code = request.POST.get('Code') #这里的我改为大写Code就可以创建了！！！！
        name = request.POST.get('Name') #注意：括号里的名字写什么取决于你的html input的name是什么！！！
        course = Course(code=code, name=name)
        course.save()
        return redirect('showCourses')
    return render(request, 'createCourse.html')


def showCourses(request):
    courses = Course.objects.all()
    return render(request, 'showCourses.html', {'courses': courses})


def showCourse(request, id):
    course = Course.objects.get(id=id)
    return render(request, 'showCourse.html', {'course': course})


def updateCourse(request, id):
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        course.name = name
        course.code = code
        course.save()
        return redirect('showCourses')
    return render(request, 'showCourse.html', {'course': course})


def deleteCourse(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('showCourses')


def showClasses(request):
    classes = Class.objects.all()
    return render(request, 'showClasses.html', {'classes': classes})


def showClass(request, id):
    class_obj = Class.objects.get(id=id)
    return render(request, 'showClass.html', {'class': class_obj,})


def createClass(request):
    semester_choices = Semester.objects.all()
    course_choices = Course.objects.all()
    lecturer_choices = Lecturer.objects.all()

    context = {
        'semester_choices': semester_choices,
        'course_choices': course_choices,
        'lecturer_choices': lecturer_choices,
    }

    if request.method == 'POST':
        number = request.POST.get('number')
        semester_id = request.POST.get('semester')  # Retrieve semester ID
        course_id = request.POST.get('course')      # Retrieve course ID
        lecturer_id = request.POST.get('lecturer')  # Retrieve lecturer ID
        #出现的问题：刚开始用的是直接将页面上的semester/course/lecturer都保存了，可是他们是name字符串，而不是id！没有办法保存的呀！

        # Get semester, course, and lecturer instances
        semester = Semester.objects.get(pk=semester_id)
        course = Course.objects.get(pk=course_id)
        lecturer = Lecturer.objects.get(pk=lecturer_id)

        class_instance = Class(number=number, semester=semester, course=course, lecturer=lecturer)
        class_instance.save()

        return redirect('showClasses')
    return render(request, 'createClass.html', context)


def updateClass(request, id):
    classs = Class.objects.get(id=id)

    if request.method == 'POST':
        number = request.POST.get('number')
        semester_id = request.POST.get('semester')
        course_id = request.POST.get('course')
        lecturer_id = request.POST.get('lecturer')

        semester = Semester.objects.get(pk=semester_id)
        course = Course.objects.get(pk=course_id)
        lecturer = Lecturer.objects.get(pk=lecturer_id)

        classs.number = number
        classs.semester = semester
        classs.course = course
        classs.lecturer = lecturer
        classs.save()
        return redirect('showClasses')

    semester_choices = Semester.objects.all()
    course_choices = Course.objects.all()
    lecturer_choices = Lecturer.objects.all()

    context = {
        'class': classs,
        'semester_choices': semester_choices,
        'course_choices': course_choices,
        'lecturer_choices': lecturer_choices,
    }

    return render(request, 'showClass.html', context)


def deleteClass(request, id):
    classs = Class.objects.get(id=id)
    classs.delete()
    return redirect('showClasses')


def assignLecturerToClass(request):
    classes = Class.objects.all()
    return render(request, 'assignLecturerToClass.html', {'classes': classes})


# def AssignALecturerToThisClass(request, id):
#     if request.method == 'POST':
#         classs = Class.objects.get(id=id)
#         lecturers = Lecturer.objects.all()
#         return render(request, 'assignLecturerToThisClass.html', {'class': classs, 'lecturers': lecturers})
#
def AssignALecturerToThisClass(request, id):
    classs = Class.objects.get(id=id)
    lecturers = Lecturer.objects.all()
    return render(request, 'assignLecturerToThisClass.html', {'class': classs, 'lecturers': lecturers})


def saveAndShowClassesWithLecturer(request, id):
    classs = Class.objects.get(id=id)
    lecturer = request.POST.get('lecturer')
    classs.lecturer = lecturer
    classs.save()
    return redirect('assignLecturerToClass')


def removeLecturerFromClass(request):
    return redirect('removeLecturerToClass.html')

def removeLecturerToClass(request):
    return redirect('RemoveALecturerFromThisClass')

def RemoveALecturerFromThisClass(request, id):
    classC = request.POST.get(id=id)
    lecturers = Lecturer.objects.all()
    return render(request, 'removeLecturerToThisClass.html', {'class': classC, 'lecturers': lecturers})

def removeLecturerFromAClass(request, id):
    classC = request.POST.get(id=id)
    lecturer = request.POST.get('lecturer')
    if lecturer:
        classC.lecturer = lecturer
        classC.save()
        return redirect('removeLecturerFromClass')
    else:
        # 使用Django的消息框架显示提示
        messages.error(request, 'One class must have only one lecturer')
        return redirect('RemoveALecturerFromThisClass')

def changeLecturerToClass(request):
    return None


def showLecturerToClass(request):
    return None
