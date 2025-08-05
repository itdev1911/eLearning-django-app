# core/permissions.py
from rest_framework import permissions

class IsTeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, авторизован ли пользователь и является ли он преподавателем
        return request.user and request.user.is_authenticated and request.user.is_teacher

class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS (только для чтения) для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем создание (POST), обновление (PUT, PATCH) и удаление (DELETE)
        # только для авторизованных преподавателей
        return request.user and request.user.is_authenticated and request.user.is_teacher

class IsStudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, авторизован ли пользователь и является ли он студентом
        return request.user and request.user.is_authenticated and request.user.is_student