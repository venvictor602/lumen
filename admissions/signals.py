# admissions/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student

@receiver(post_save, sender=Student)
def create_user_on_acceptance(sender, instance, **kwargs):
    # Call create_user_account only if status is 'Accepted'
    if instance.status == 'Accepted':
        instance.create_user_account()
