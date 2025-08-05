"""
URL configuration for elearning1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('signup/student/', core_views.student_signup, name='student_signup'),
    path('signup/teacher/', core_views.teacher_signup, name='teacher_signup'),
    path('login/', core_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', core_views.home, name='home'),
    path('student/dashboard/', core_views.student_dashboard, name='student_dashboard'),
    path('all_courses/', core_views.all_courses, name='all_courses'),
    path('teacher/dashboard/', core_views.teacher_dashboard, name='teacher_dashboard'),
    path('course/create/', core_views.create_course, name='create_course'),
    path('profile/', core_views.profile, name='profile'),
    path('course/<int:course_id>/', core_views.course_detail, name='course_detail'),
    path('course/<int:course_id>/manage/', core_views.manage_course, name='manage_course'),
    path('course/<int:course_id>/enroll/', core_views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/chat/', core_views.chat_room, name='chat_room'),
    path('docs/', core_views.documentation, name='documentation'),
]
