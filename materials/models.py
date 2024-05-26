from config import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    avatar = models.ImageField(verbose_name='превью', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    amount = models.IntegerField(default=1000, verbose_name='цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    avatar = models.ImageField(verbose_name='превью', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    status = models.BooleanField(default=False, verbose_name='статус подписки')

    def __str__(self):
        return f'{self.user} - {self.course} / {self.status}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
