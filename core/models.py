from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Расширение стандартной модели пользователя Django
# (для соответствия требованиям о двух типах пользователей - R1)
class User(AbstractUser):
    # Дополнительные поля для хранения информации о пользователе (R1)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    # Здесь можно добавить другие поля, например, date_of_birth, bio и т.д.

    enrolled_courses = models.ManyToManyField(
        'Course',
        related_name='enrolled_students',
        blank=True
    )

    def __str__(self):
        return self.username

class Student(models.Model):
    # Связь "один к одному" со стандартным пользователем
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Другие поля, если необходимо
    # Например:
    # specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    # Связь "один к одному" со стандартным пользователем
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Другие поля, если необходимо
    # Например:
    # bio = models.TextField()

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # ИСПРАВЛЕНО: используем 'is_teacher=True' вместо 'user_type'
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},  # <--- ИСПРАВЛЕНО ЗДЕСЬ
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    # Студенты могут оставлять отзывы о курсах (R1f)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # от 1 до 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Убедимся, что один студент может оставить только один отзыв на курс
        unique_together = ('student', 'course')

    def __str__(self):
        return f'Review by {self.student.user.username} for {self.course.title}'

class StatusUpdate(models.Model):
    # Обновления статуса могут добавлять как студенты, так и преподаватели (R1i)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_updates')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Status update by {self.user.username}'
