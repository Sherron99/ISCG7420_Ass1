from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

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
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name, email=email)
        user.groups.add(Group.objects.get(name='Students'))

        # Create Student instance
        student = Student.objects.create(firstName=first_name, lastName=last_name, email=email, DOB=dob)
        student.save()  # 遇到的问题是：我一开始只使用了user = User.objects.create_user()...但是没有对管理后台里的Student class进行创建。导致登陆了管理系统，Student列表一直没有显示数据

        # Add any other logic or redirects as needed
        return redirect('showStudents')

    # Render the registration form
    return render(request, 'registerStudent.html')


def registerLecturer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name, email=email)
        user.groups.add(Group.objects.get(name='Lecturers'))

        lecturer = Lecturer.objects.create(firstName=first_name, lastName=last_name, email=email, DOB=dob)

        return redirect('showLecturers')
    return render(request, 'registerLecturer.html')


# 下面这串代码我是想显示出该用户的信息

def showLecturer(request, id):
    user = User.objects.get(id=id)
    return render(request, 'showLecturer.html', {'user': user})


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
    return redirect('showLecturers')


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
    return render(request, 'showStudent.html', {'user': user})  # 因为showStudent用的是user，所以我们不用更改


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
    return render(request, 'showSemester.html',
                  {'semester': semester})  # context里的内容一定要和showSemester.html里的名字对应(semester.id)


def deleteSemester(request, id):
    semester = Semester.objects.get(id=id)
    semester.delete()
    return redirect('showSemesters')


def createCourse(request):
    if request.method == 'POST':
        code = request.POST.get('Code')  # 这里的我改为大写Code就可以创建了！！！！
        name = request.POST.get('Name')  # 注意：括号里的名字写什么取决于你的html input的name是什么！！！
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
    return render(request, 'showClass.html', {'class': class_obj, })


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
        course_id = request.POST.get('course')  # Retrieve course ID
        lecturer_id = request.POST.get('lecturer')  # Retrieve lecturer ID
        # 出现的问题：刚开始用的是直接将页面上的semester/course/lecturer都保存了，可是他们是name字符串，而不是id！没有办法保存的呀！

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


# def removeLecturerFromClass(request):
#     classes = Class.objects.all()
#     return render(request, 'removeLecturerToClass.html', {'classes': classes})

#
# def RemoveALecturerFromThisClass(request):
#     if request.method == 'POST':
#         class_id = request.POST.get('classChose')
#         class_obj = Class.objects.get(id=class_id)
#         lecturers = Lecturer.objects.all()
#         return render(request, 'removeLecturerToThisClass.html', {'lecturers': lecturers, 'class_obj': class_obj})
#     else:
#         classes = Class.objects.all()
#         return render(request, 'removeLecturerToThisClass.html', {'classes': classes})


# def removeLecturerFromAClass(request, id):
#     classC = get_object_or_404(Class, id=id)
#     lecturer_id = request.POST.get('lecturer')
#
#     if lecturer_id == 0:  # 如果用户没有选择讲师
#         messages.error(request, 'One class must have only one lecturer')
#         return redirect('RemoveALecturerFromThisClass')
#     else:  # 如果用户选择了一个讲师
#         lecturer = get_object_or_404(Lecturer, id=lecturer_id)
#         classC.lecturer = lecturer
#         classC.save()
#         return redirect('RemoveALecturerFromThisClass')


def removeLecturerFromClass(request):
    classes = Class.objects.all()
    # for class_obj in classes:
    #     class_obj.remove_lecturer_url = reverse('removeLecturer', args=[class_obj.id]) 另一种方式给每一个class创建一个url。我觉得难理解
    return render(request, 'showAllClasses.html', {'classes': classes})


def removeLecturerFromAClass(request, id):
    classC = get_object_or_404(Class, id=id)
    lecturer_id = request.POST.get('lecturer')

    if lecturer_id == '':  # 如果用户没有选择讲师
        messages.error(request, 'One class must have one lecturer')
        return redirect('removeLecturer', id=id)
    else:  # 如果用户选择了一个讲师
        lecturer = get_object_or_404(Lecturer, id=lecturer_id)
        classC.lecturer = lecturer
        classC.save()
        return redirect('removeLecturerFromClass')


def removeLecturer(request, id):
    classDe = Class.objects.get(id=id)
    lecturers = Lecturer.objects.all()
    error_messages = messages.get_messages(request)
    return render(request, 'showClassDe.html',
                  {'classDe': classDe, 'lecturers': lecturers, 'error_messages': error_messages})


def showLecturerToClass(request):
    lecturers = Lecturer.objects.all();
    return render(request, 'chooseALecturer.html', {'lecturers': lecturers})


def showTheLecturerDetail(request):
    if request.method == 'GET':
        id = request.GET.get('theLecturer')
        allClasses = Class.objects.filter(lecturer=id)
        return render(request, 'showTheLecturerDetail.html', {'theLecturer': id, 'allClasses': allClasses})


def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        import pandas as pd
        excel_data = pd.read_excel(myfile)
        data = pd.DataFrame(excel_data)
        firstnames = data['firstname'].tolist()
        lastnames = data['lastname'].tolist()
        emails = data['email'].tolist()
        DOBs = data['DOB'].tolist()

        i = 0
        while i < len(emails):
            student = Student.objects.create(firstName=firstnames[i], lastName=lastnames[i]
                                             , email=emails[i], DOB=DOBs[i])

            student.save()
            user = User.objects.create_user(username=student.email, password=student.DOB.strftime('%Y%m%d'))
            user.save()

            i = i + 1

        return render(request, 'file_upload_form.html', {
            'uploaded_file_url': uploaded_file_url

        })

    return render(request, 'file_upload_form.html')


def send_email_out(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        from_email = request.POST['from_email']
        to_email = request.POST['to_email']
        send_mail(subject, body, from_email, [to_email])

    return render(request, 'send_email_out.html')


def showAllStudents(request):
    students = Student.objects.all()
    return render(request, 'showAllStudents.html', {'students': students})


def showTheStudentDetail(request):
    # theStudentID = Student.objects.get(id=id)
    if request.method == 'GET':
        studentId = request.GET.get('theStudent')
        student = Student.objects.get(id=studentId)

        # 获取该学生已经注册的课程 ID 列表
        enrolled_classes = StudentEnrolment.objects.filter(student=student).values_list('Class__id',
                                                                                        flat=True)  # chatgpt写的
        # 上面这串代码，是从studentenrolment表中获取student的实例（当然我们也可以通过主键来filter都可以）。values_list括号里第一个是写想要查询的字段，例如Class__id（是可以这样写的），然后将其转换为一个列表
        # 上面这串代码，是多对多的表（bridge table），如果我们想要通过一个class id 获取另一个class id的方法。
        # 所以最终enroleed_classes的效果是[1,3,5]....这就是flat=true的效果

        # 获取所有课程,但排除已经注册的课程
        allClasses = Class.objects.exclude(id__in=enrolled_classes)
        # __in是一种查询方式，我们查询所有class的id，搜索出不在enrolled_classes里的所有class

        return render(request, 'enrolStudent.html', {'theStudent': student, 'allClasses': allClasses})


def submitEnrolment(request, id):
    if request.method == 'POST':
        selected_student = Student.objects.get(id=id)
        class_id = request.POST.get('theClass')
        selected_class = Class.objects.get(id=class_id)
        # 上两步获取相应的studentID和classID

    enrollment = StudentEnrolment.objects.create(student=selected_student, Class=selected_class, grade=None,
                                                 enrolTime=timezone.now(), gradeTime=None)
    # 遇到的问题是：我直接保存了class的id，这是不对的。当我们要创建一个新的实例的时候，我们必须指定关联的对象（实例，就是一个对象包含了所有属性）。
    enrollment.save()

    # Redirect to success page or display a success message
    return redirect('showAllStudents')


def showAllStudentsClasses(request):
    allStudents = Student.objects.all()
    return render(request, 'showAllStudentsClasses.html', {'allStudents': allStudents})


def showStudentClasses(request):
    if request.method == 'GET':
        getStudentID = request.GET.get('theStudent')
        studentObj = Student.objects.get(id=getStudentID)
        enrolled_classes = StudentEnrolment.objects.filter(student=studentObj).values_list('Class',
                                                                                           flat=True)  # 我们这里用的是class实例
        # 上面这行代码：由于student和class之间有一个StudentEnrolment（bridge table），我们通过filter，来获取同一个student的所有class
        classes = Class.objects.filter(id__in=enrolled_classes)
    return render(request, 'showStudentClasses.html', {'student': studentObj, 'classes': classes})


def showAllStudentstoRemoveClasses(request):
    allStudents = Student.objects.all()
    return render(request, 'showAllStudentsClassesToRemove.html', {'allStudents': allStudents})


def removeClasses(request):
    if request.method == 'GET':
        getStudentID = request.GET.get('theStudent')
        studentObj = Student.objects.get(id=getStudentID)
        enrolled_classes = StudentEnrolment.objects.filter(student=studentObj).values_list('Class', flat=True)
        classes = Class.objects.filter(id__in=enrolled_classes)
        return render(request, 'removeStudentClass.html', {'student': studentObj, 'classes': classes})


def updateTheStudentClasses(request, id):
    if request.method == 'POST':
        selected_student = Student.objects.get(id=id)
        selected_classes = request.POST.get('theClass')

        for class_id in selected_classes:
            selected_class = Class.objects.get(id=class_id)

        enrollments = StudentEnrolment.objects.filter(student=selected_student, Class=selected_class)
        enrollments.delete()

        return redirect('showAllStudentsClasses')


def chooseAClass(request, user_email):
    user = User.objects.get(email=user_email)
    lecturer = Lecturer.objects.get(user=user)  # Assuming a one-to-one relationship between User and Lecturer
    lecturer_classes = Class.objects.filter(lecturer=lecturer)

    return render(request, 'displayAllClasses.html', {'classes': lecturer_classes})


def markStudentsGrade(request):
    if request.metho == 'GET':
        classID = request.GET.get('classChose')
        classObj = Class.objects.get(id=classID)
        getAllStudent = StudentEnrolment.objects.filter(Class=classID).values_list('student', flat=True)
        allStudentsObjs = Student.objects.filter(id__in=getAllStudent)
    return render(request, 'showAllStudentsWithMarks.html', {'class': classObj, 'Students': allStudentsObjs})


def submitMarks(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        selected_class = get_object_or_404(Class, id=class_id)
        for student in selected_class.students.all():
            student_id = student.id
            grade = request.POST.get(f'mark_{student_id}')
            if grade:
                enrollment, created = StudentEnrolment.objects.get_or_create(
                    student=student,
                    Class=selected_class,
                    defaults={'grade': grade, 'gradeTime': timezone.now()}
                )
                if not created:
                    enrollment.grade = grade
                    enrollment.gradeTime = timezone.now()
                    enrollment.save()
    return redirect('markStudentsGrade')
