from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Student, Teacher, StatusUpdate, Material

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Что нового?'})
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'file']