
from rest_framework import permissions

class IsTeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user and request.user.is_authenticated and request.user.is_teacher

class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        
        return request.user and request.user.is_authenticated and request.user.is_teacher

class IsStudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user and request.user.is_authenticated and request.user.is_student