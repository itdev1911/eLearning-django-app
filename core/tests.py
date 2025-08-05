# core/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Material, Review, Student, Teacher
from .serializers import CourseSerializer, UserSerializer

User = get_user_model()

# ====================================================================
# Модульное тестирование моделей
# ====================================================================

class ModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='test_teacher', password='password123', is_teacher=True
        )
        self.student = User.objects.create_user(
            username='test_student', password='password123', is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course', description='Test Description', teacher=self.teacher
        )
        self.material = Material.objects.create(
            course=self.course, title='Test Material', file='test_file.pdf'
        )

    def test_course_creation(self):
        """Проверяет, что курс создается корректно."""
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.teacher, self.teacher)

    def test_material_creation(self):
        """Проверяет, что материал создается корректно."""
        self.assertEqual(self.material.title, 'Test Material')
        self.assertEqual(self.material.course, self.course)

    def test_review_creation(self):
        """Проверяет, что отзыв создается корректно."""
        student_profile = Student.objects.create(user=self.student)
        review = Review.objects.create(
            student=student_profile, course=self.course, rating=5, comment='Great course!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.student, student_profile)
        self.assertEqual(review.course, self.course)

# ====================================================================
# Модульное тестирование представлений
# ====================================================================

class ViewTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='test_teacher', password='password123', is_teacher=True
        )
        self.student = User.objects.create_user(
            username='test_student', password='password123', is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course', description='Test Description', teacher=self.teacher
        )

    def test_student_dashboard(self):
        """Проверяет, что панель студента отображается и показывает записанные курсы."""
        self.client.login(username='test_student', password='password123')
        self.student.enrolled_courses.add(self.course)
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_teacher_dashboard(self):
        """Проверяет, что панель преподавателя отображается и показывает созданные курсы."""
        self.client.login(username='test_teacher', password='password123')
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

# ====================================================================
# Тестирование API с Django REST Framework
# ====================================================================

class ApiTest(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='test_teacher', password='password123', is_teacher=True
        )
        self.student = User.objects.create_user(
            username='test_student', password='password123', is_student=True
        )
        self.course = Course.objects.create(
            title='API Course', description='API Test Description', teacher=self.teacher
        )
        self.course_url = reverse('course-list')

    def test_course_list_api(self):
        """Проверяет, что список курсов доступен."""
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'API Course')

    def test_create_course_api_by_teacher(self):
        """Проверяет, что преподаватель может создать курс через API."""
        self.client.force_authenticate(user=self.teacher)
        data = {'title': 'New API Course', 'description': 'New API Description', 'teacher': self.teacher.id}
        response = self.client.post(self.course_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_create_course_api_by_student_fail(self):
        """Проверяет, что студент не может создать курс через API."""
        self.client.force_authenticate(user=self.student)
        data = {'title': 'New API Course', 'description': 'New API Description', 'teacher': self.teacher.id}
        response = self.client.post(self.course_url, data)
        # Ожидаем ошибку 403 Forbidden, так как студент не может создавать курсы
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)