from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.users.models import UserProfile
from .models import Coupon

User = get_user_model()

class CouponModelTest(TestCase):

    def setUp(self):
        now = timezone.now()
        next_year = now + timedelta(days=365)

        self.GOLD_user = User.objects.create_user(
            username='GOLDuser', password='password123'
        )

        self.GOLD_profile, created = UserProfile.objects.get_or_create(user=self.GOLD_user)
        self.GOLD_profile.customer_type = UserProfile.CustomerType.GOLD
        self.GOLD_profile.save()
        self.GOLD_user.refresh_from_db()
        self.normal_user = User.objects.create_user(
            username='normaluser', password='password123'
        )

        self.normal_profile, _ = UserProfile.objects.get_or_create(user=self.normal_user)
        self.normal_profile.customer_type = 'BRONZE'
        self.normal_profile.save()

        self.GOLD_coupon = Coupon.objects.create(
            code='GOLD50',
            discount_value=50000,
            discount_type='AMOUNT',
            applies_to_customer_type='GOLD',
            valid_from=now,
            valid_until=next_year
        )

        self.public_coupon = Coupon.objects.create(
            code='WELCOME',
            discount_value=10,
            discount_type='PERCENT',
            applies_to_customer_type='',
            valid_from=now,
            valid_until=next_year
        )

    def test_coupon_creation(self):
        coupon = Coupon.objects.get(code='GOLD50')
        self.assertEqual(coupon.discount_value, 50000)

    def test_GOLD_coupon_valid_for_GOLD_user(self):
        self.GOLD_user.refresh_from_db()
        print(UserProfile.CustomerType.GOLD)
        print(f"User Type: {self.GOLD_user.profile.customer_type}") 
        print(f"Coupon Target: {self.GOLD_coupon.applies_to_customer_type}")
        
        is_valid = self.GOLD_coupon.is_applicable_to_user(self.GOLD_user)
        self.assertTrue(is_valid, "Coupon GOLD phải dùng được cho user GOLD")

    def test_GOLD_coupon_invalid_for_normal_user(self):
        is_valid = self.GOLD_coupon.is_applicable_to_user(self.normal_user)
        self.assertFalse(is_valid, "Coupon GOLD không được dùng cho user thường")

    def test_public_coupon_valid_for_everyone(self):
        self.assertTrue(self.public_coupon.is_applicable_to_user(self.GOLD_user))
        self.assertTrue(self.public_coupon.is_applicable_to_user(self.normal_user))