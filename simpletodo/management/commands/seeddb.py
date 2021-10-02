from django.core.management.base import BaseCommand

from user.factory import SuperUserFactory, UserFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        SuperUserFactory(
            email='admin@localhost',
            password='password',
        )

        for _ in range(5):
            UserFactory.create()
