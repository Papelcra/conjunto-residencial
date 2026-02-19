from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea datos iniciales'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@admin.com",
                password="Admin123!"
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado'))
        else:
            self.stdout.write('El superusuario ya existe')
