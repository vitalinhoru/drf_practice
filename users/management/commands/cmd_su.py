from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='kirillovitaly@mail.ru',
            first_name='admin',
            last_name='adminov',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('1234')
        user.save()
