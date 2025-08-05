from rest_framework import serializers
from .models import User, Student, Teacher, Course, Material, Review, StatusUpdate

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_student', 'is_teacher', 'photo')

# Сериализатор для студента
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

# Сериализатор для преподавателя
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    # Добавляем скрытое поле 'teacher', которое автоматически заполняется текущим пользователем
    teacher = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'created_at']
        read_only_fields = ['id', 'created_at']

# Сериализатор для материала
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

# Сериализатор для отзыва
class ReviewSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

# Сериализатор для обновления статуса
class StatusUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StatusUpdate
        fields = '__all__'

class StatusUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Это поле будет только для чтения

    class Meta:
        model = StatusUpdate
        fields = '__all__'

    def create(self, validated_data):
        # Получаем текущего пользователя из контекста запроса
        user = self.context['request'].user
        # Создаем StatusUpdate, привязывая его к текущему пользователю
        status_update = StatusUpdate.objects.create(user=user, **validated_data)
        return status_update

class ReviewSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        # Получаем текущего пользователя-студента
        user = self.context['request'].user
        course = data['course']

        if not user.is_student:
            raise serializers.ValidationError("Only students can leave reviews.")

        student = user.student
        # Проверяем, записан ли студент на этот курс
        if not course.students.filter(user=student.user).exists():
            raise serializers.ValidationError("You must be enrolled in this course to leave a review.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        student = user.student
        review = Review.objects.create(student=student, **validated_data)
        return review