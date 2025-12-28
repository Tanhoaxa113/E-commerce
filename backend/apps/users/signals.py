from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, CustomUser
from apps.carts.models import Cart

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Cart.objects.create(user=instance)
