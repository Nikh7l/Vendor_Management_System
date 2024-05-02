from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class Command(BaseCommand):
    help = 'Generate tokens for testing purposes'

    def handle(self, *args, **options):
        # Check if the test user already exists
        if not User.objects.filter(username='test_user').exists():
            # Create a new user with username 'test_user' and password 'test_password'
            User.objects.create_user(username='test_user', password='test_password')
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Retrieve the test user
        test_user = User.objects.get(username='test_user')

        # Generate tokens for the test user
        refresh = RefreshToken.for_user(test_user)

        # Display the generated tokens
        self.stdout.write(self.style.SUCCESS(f'Access Token: {str(refresh.access_token)}'))
        self.stdout.write(self.style.SUCCESS(f'Refresh Token: {str(refresh)}'))
        
