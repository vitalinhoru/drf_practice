from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        # fields = '__all__'
        fields = ('title', 'description', 'course',)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_lesson_count(self, instance):
        if instance.lesson_set.all().first():
            return instance.lesson_set.all().count()
        return 0

    class Meta:
        model = Course
        fields = '__all__'
