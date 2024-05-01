from rest_framework.serializers import ValidationError

allowed_video_link = 'youtube'


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data_url = dict(value).get(self.field)

        if allowed_video_link not in data_url:
            raise ValidationError('Нельзя использовать материалы сторонних ресурсов')
