from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """Create a superuser when the application is first deployed."""
    User = get_user_model()
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
