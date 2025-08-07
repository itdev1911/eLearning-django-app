from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Course, Notification, Material


@receiver(m2m_changed, sender=Course.enrolled_students.through)
def student_enrollment_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        course = instance
        teacher = course.teacher
        for student_pk in pk_set:
            student = course.enrolled_students.get(pk=student_pk)
            message = f"Студент {student.username} записался на ваш курс '{course.title}'."
            Notification.objects.create(user=teacher, message=message)


@receiver(post_save, sender=Material)
def new_material_notification(sender, instance, created, **kwargs):
    if created:
        material = instance
        course = material.course
        students = course.enrolled_students.all()
        for student in students:
            message = f"В курсе '{course.title}' добавлен новый материал: '{material.title}'."
            Notification.objects.create(user=student, message=message)