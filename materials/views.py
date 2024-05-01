from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.paginations import LessonPagination, CoursePagination
from materials.permissions import IsStaff, IsOwner
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsStaff]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsOwner | IsStaff]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwner | IsStaff]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsOwner | IsStaff]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsStaff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsStaff]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionView(APIView):
    # serializer_class = SubscriptionSerializer
    # queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data['course']
        course_item = get_object_or_404(Course, id=course_id)

        subs_item, created = Subscription.objects.update_or_create(course=course_item, user=user)

        if created:
            subs_item.status = True
            subs_item.save()
            message = 'подписка добавлена'
        # Если подписка у пользователя на этот курс есть - удаляем ее
        elif subs_item.status:
            subs_item.status = False
            subs_item.save()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            subs_item.status = True
            subs_item.save()
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
