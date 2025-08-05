# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    StudentViewSet,
    TeacherViewSet,
    CourseViewSet,
    MaterialViewSet,
    ReviewViewSet,
    StatusUpdateViewSet,
    StudentSearchView,
    TeacherSearchView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'status-updates', StatusUpdateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('students/search/', StudentSearchView.as_view(), name='student-search'),
    path('teachers/search/', TeacherSearchView.as_view(), name='teacher-search'),
]