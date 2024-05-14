from django.db import models

# Create your models here.
class Semester(models.Model): #Semester Model
    year = models.IntegerField()
    semester = models.IntegerField()
    courses = models.ManyToManyField('Course', blank=True, null=True)
    #course 和 semester是多对多关系，那么ManyToManyField放在哪一个class里面，取决于哪一个逻辑会更自然或查询更频繁

    def __str__(self):
        return f"{self.year} - Semester {self.semester}"
    #In Django, the __str__ method should return a string representation of the object.
    #这里的def显示的是管理后台显示的内容

class Course(models.Model): #Course Model
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lecturer(models.Model): #Lecturer Model
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    DOB = models.DateField()

    def __str__(self):
        return self.firstName + self.lastName

class Class(models.Model): #Class Model
    number = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='classes_taught') #这里我们有related_name后，我们是可以通过lecturer来获取所有的与他有关的class。related_name指定反向关系的名称
    students = models.ManyToManyField('Student', through='StudentEnrolment')#through指定关系的表名

    def __str__(self):
        return self.number + self.course.name

class Student(models.Model): #Student Model
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    DOB = models.DateField()

    def __str__(self):
        return self.firstName + self.email


class StudentEnrolment(models.Model): #Student Enrolment Model
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE,related_name="getAllStudentEnrolments")
    grade = models.IntegerField(blank=True, null=True)
    enrolTime = models.DateTimeField(auto_now_add=True) #auto_now_add=True 在创建的时候自动添加
    gradeTime = models.DateTimeField(auto_now=True) #auto_now=True 在修改的时候自动修改
