from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Organization

@receiver(post_migrate)
def create_default_organization(sender, **kwargs):
    if not Organization.objects.exists():
        Organization.objects.create(
            name="Default Organization",
            email="default@organization.com",
            address="Default Address",
            phone_number="123-456-7890"
        )
