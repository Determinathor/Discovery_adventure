from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Profile

from django.contrib.auth.models import User


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='testuser@test.cz', password='password')

        cls.profile = Profile.objects.create(
            user=cls.user,
            address='Test ulice 123',
            phone_number=123456789,
            city='Test city',
        )

        cls.profile.save()

    def setUp(self):
        print("-"*60)

    def test_profile_creation(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_creation: user='{profile.user.username}', address='{profile.address}', phone_number='{profile.phone_number}', city='{profile.city}'")
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.address, 'Test ulice 123')
        self.assertEqual(int(profile.phone_number), 123456789)
        self.assertEqual(profile.city, 'Test city')

    def test_profile_username(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_username: '{profile.user.username}'")
        self.assertEqual(profile.user.username, 'testuser')

    def test_profile_address(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_address: '{profile.address}'")
        self.assertEqual(profile.address, 'Test ulice 123')

    def test_profile_phone_number(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_phone_number: '{profile.phone_number}'")
        self.assertEqual(int(profile.phone_number), 123456789)

    def test_profile_city(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_city: '{profile.city}'")
        self.assertEqual(profile.city, 'Test city')

    def test_profile_str(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_str: '{str(profile)}'")
        self.assertEqual(str(profile), self.user.email)

    def test_profile_repr(self):
        profile = Profile.objects.get(id=self.profile.id)
        print(f"test_profile_repr: '{repr(profile)}'")
        self.assertEqual(repr(profile), f"Profile(user={self.user})")

    def test_phone_number_too_short(self):
        profile = Profile(
            user=self.user,
            address='Test ulice 123',
            phone_number=12345678,  # 8 číslic, krátké
            city='Test city',
        )
        print("test_phone_number_too_short: Trying to validate phone number '12345678'")
        with self.assertRaises(ValidationError):
            profile.full_clean()  # spustí validátor

    def test_phone_number_too_long(self):
        profile = Profile(
            user=self.user,
            address='Test ulice 123',
            phone_number=1234567890123,  # 13 číslic, dlouhé
            city='Test city',
        )
        print("test_phone_number_too_long: Trying to validate phone number:", 1234567890123)
        with self.assertRaises(ValidationError):
            profile.full_clean()  # spustí validátor

    def test_phone_number_contains_non_digits(self):
        profile = Profile(
            user=self.user,
            address='Test ulice 123',
            phone_number='1234abc789',  # obsah dalších znaků krom číslic
            city='Test city',
        )
        print("test_phone_number_contains_non_digits: Trying to validate phone number:", '1234abc789')
        with self.assertRaises(ValidationError):
            profile.full_clean()  # spustí custom clean metodu

