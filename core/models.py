from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver



class User(AbstractUser):
    
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    photo = models.ImageField(upload_to='users/', blank=True, null=True)

    enrolled_courses = models.ManyToManyField(
        'Course',
        related_name='enrolled_students',
        blank=True
    )

    def __str__(self):
        return self.username

class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},  
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
  
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # от 1 до 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
    
        unique_together = ('student', 'course')

    def __str__(self):
        return f'Review by {self.student.user.username} for {self.course.title}'

class StatusUpdate(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_updates')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Status update by {self.user.username}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'