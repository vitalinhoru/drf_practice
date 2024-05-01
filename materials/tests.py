from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='sky@pro.ru',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            title='Test',
            description='Test',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Test',
            description='Test_lesson',
            owner=self.user
        )

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            "title": "Test DRF 1",
            "description": "test",
            "video_link": "https://www.youtube.com/some_video",
            "course": "1"
        }

        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])

    def test_create_lesson_with_invalid_data(self):
        """Тестирование ошибки по видео"""

        data = {
            "title": "Test DRF 2",
            "description": "test",
            "video_link": "https://www.sky.pro/video",
            "course": "2"
        }

        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Нельзя использовать материалы сторонних ресурсов']})

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""

        response = self.client.get(
            reverse('materials:lesson-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], self.lesson.title)

    def test_retrieve_lesson(self):
        """Тестирование вывода одного урока"""

        response = self.client.get(
            reverse('materials:lesson-get', args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        """Тестирование обновления урока"""

        updated_data = {
            "description": "updated lesson",
            "video_link": "https://www.youtube.com/watch?v=jAWHLwICGc4"
        }

        response = self.client.patch(
            reverse('materials:lesson-update', args=[self.lesson.id]), updated_data
        )

        self.lesson.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], updated_data['description'])

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        response = self.client.delete(
            reverse('materials:lesson-delete', args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='sky2@pro.ru',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            title='test_course',
            description='test_course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='test_lesson',
            description='test_lesson',
            owner=self.user
        )

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_subscribe_to_course(self):
        """Тестирование функционала подписки на курс"""

        data = {
            "user": self.user,
            "course": self.course.id
        }

        response = self.client.post(
            reverse('materials:subscription'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

    def test_unsubscribe_to_course(self):
        """Тестирование функционала удаления подписки на курс"""
        data = {
            "user": self.user,
            "course": self.course.id
        }

        response = self.client.post(
            reverse('materials:subscription'),
            data=data
        )
        response = self.client.post(
            reverse('materials:subscription'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
