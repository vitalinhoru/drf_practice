from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        # fields = '__all__'
        fields = ('title', 'description', 'course',)


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # fields = '__all__'
        fields = ('title', 'description',)

    @staticmethod
    def get_count_lessons(course):
        return Lesson.objects.filter(course=course).count()
