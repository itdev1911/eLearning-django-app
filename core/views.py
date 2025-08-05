from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import User, Student, Teacher, Course, Material, Review, StatusUpdate
from .serializers import (
    UserSerializer,
    StudentSerializer,
    TeacherSerializer,
    CourseSerializer,
    MaterialSerializer,
    ReviewSerializer,
    StatusUpdateSerializer
)

from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, TeacherSignUpForm, CourseForm
from .models import Course, Material

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentSignUpForm, TeacherSignUpForm # Эти формы нужно будет создать
from rest_framework import generics
from .serializers import StudentSerializer, TeacherSerializer
from .permissions import IsTeacherPermission
from .permissions import IsTeacherOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, TeacherSignUpForm, CourseForm

def home(request):
    return render(request, 'core/home.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated] # Доступ только для авторизованных пользователей

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsTeacherPermission]

from .permissions import IsStudentPermission 

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsStudentPermission] 

class StatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = StatusUpdate.objects.all()
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # 'home' - это URL-адрес для главной страницы
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/signup_student.html', {'form': form})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration/signup_teacher.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

class StudentSearchView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsTeacherPermission] # Эта пермиссия будет создана далее

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Student.objects.filter(user__username__icontains=query)

class TeacherSearchView(generics.ListAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacherPermission]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Teacher.objects.filter(user__username__icontains=query)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        try:
            student = request.user.student
            course.students.add(student)
            return Response({'status': 'student enrolled'}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'error': 'User is not a student'}, status=status.HTTP_400_BAD_REQUEST)
        
def home(request):
    return render(request, 'core/home.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('home')

    enrolled_courses = request.user.enrolled_courses.all()
    
    return render(request, 'core/student_dashboard.html', {'enrolled_courses': enrolled_courses})

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('home')

    # Получаем все курсы, где текущий пользователь является преподавателем
    teaching_courses = Course.objects.filter(teacher=request.user)
    
    return render(request, 'core/teacher_dashboard.html', {'teaching_courses': teaching_courses})

@login_required
def all_courses(request):
    # Получаем все курсы, кроме тех, на которые уже записан текущий пользователь
    all_courses = Course.objects.exclude(enrolled_students=request.user)

    return render(request, 'core/all_courses.html', {'available_courses': all_courses})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_student:
        request.user.enrolled_courses.add(course)
    return redirect('student_dashboard')

@login_required
def create_course(request):
    # Убедимся, что только преподаватель может создавать курсы
    if not request.user.is_teacher:
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('teacher_dashboard')
        # Если форма невалидна, мы просто продолжаем, и Python
        # передаст форму с ошибками в render()
    else:
        # Если это GET-запрос, создаем пустую форму
        form = CourseForm()
        
    return render(request, 'core/create_course.html', {'form': form})

def course_detail(request, course_id):
    # Пытаемся найти курс по его ID, если не находим - возвращаем 404
    course = get_object_or_404(Course, pk=course_id)
    
    # Получаем все материалы, связанные с этим курсом
    materials = Material.objects.filter(course=course)

    context = {
        'course': course,
        'materials': materials,
    }
    
    return render(request, 'core/course_detail.html', context)


@login_required
def manage_course(request, course_id):
    # Пытаемся найти курс по его ID
    course = get_object_or_404(Course, pk=course_id)

    # Проверяем, является ли текущий пользователь преподавателем этого курса
    if request.user != course.teacher:
        return redirect('home') # Или куда-либо еще, если доступ запрещен

    context = {
        'course': course,
        # Здесь будет логика для управления курсом, например, добавление материалов
    }
    
    return render(request, 'core/manage_course.html', context)

def chat_room(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'core/chat_room.html', {'course': course})

def documentation(request):
    """Представление для отображения страницы с документацией."""
    return render(request, 'core/documentation.html')