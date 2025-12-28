from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import CustomUser
from .models import Cart

