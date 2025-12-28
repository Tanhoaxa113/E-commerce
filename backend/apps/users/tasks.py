from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import CustomUser
from django.core.mail import send_mail
import shortuuid
from config import settings

@shared_task
def send_otp_to_email(user_id):
    otp = shortuuid.ShortUUID().random(length=8).upper()
    if not user_id:
        pass
    else:
        user = CustomUser.objects.get(pk=user_id)
        user.otp = otp
        user.otp_valid_until = timezone.now() + timedelta(minutes=10)
        user_email = user.email
        CustomUser.objects.filter(pk=user_id).update(
            otp=otp,
            otp_valid_until=timezone.now() + timedelta(minutes=10)
        )
        subject = "OTP"
        message_body = f"Mã OTP của bạn là: {otp}"
        print("Gửi Mail thành công")
        # send_mail(
        #     subject,
        #     message_body,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user_email],
        #     fail_silently=False,
        # )
        