from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from accounts.views import UserUpdateForm, ProfileUpdateForm, SignUpForm


class UserUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='king',
            first_name='Thorin',
            last_name='Oakenshield',
            email='thorinoak@mistymountains.com',
            password='password'
        )

    def setUp(self):
        print("-"*60)

    def test_user_update_form_valid(self):
        form = UserUpdateForm(
            instance=self.user,
            data={
                'first_name': 'Bilbo',
                'last_name': 'Baggins',
                'email': 'bilbobaggins@shire.com',
            }
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        print(f"test_user_update_form_valid: ('updated_first_name': {updated_user.first_name}, 'updated_last_name': {updated_user.last_name}, 'updated_user_email': {updated_user.email}")
        self.assertEqual(updated_user.first_name, 'Bilbo')
        self.assertEqual(updated_user.last_name, 'Baggins')
        self.assertEqual(updated_user.email, 'bilbobaggins@shire.com')


class ProfileUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser_1',
            first_name='Daniel',
            last_name='Folta',
            email='test_1@example.com',
            password='password'
        )
        cls.profile = Profile.objects.create(
            user=cls.user,
            phone_number='123456789',
            address='Zbožná 123',
            city='Boží Dar'
        )
        cls.another_user = User.objects.create_user(
            username='testuser_2',
            first_name='Vít',
            last_name='Hlaváček',
            email='test_2@example.com',
            password='password'
        )
        cls.another_profile = Profile.objects.create(
            user=cls.another_user,
            phone_number='987654321',
            address='Krátká 456',
            city='Jáchymov'
        )

    def setUp(self):
        print("--"*60)

    def test_profile_update_form_valid(self):
        form = ProfileUpdateForm(
            instance=self.profile,
            user=self.user,
            data={
                'phone_number': 111111111,  # nové unikátní číslo
                'address': 'Nová adresa',
                'city': 'Nové město',
            }
        )
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        print(f"test_user_update_form_valid: ('updated_phone_number': {updated_profile.phone_number}, 'updated_address': {updated_profile.address}, 'updated_city': {updated_profile.city}")
        self.assertEqual(updated_profile.phone_number, 111111111)
        self.assertEqual(updated_profile.address, 'Nová adresa')
        self.assertEqual(updated_profile.city, 'Nové město')

    def test_profile_update_form_invalid_phone_number(self):
        form = ProfileUpdateForm(
            instance=self.profile,
            user=self.user,
            data={
                'phone_number': '987654321',  # číslo již existuje
                'address': 'Nová adresa_2',
                'city': 'Nové město_2',
            }
        )
        print(f"test_profile_update_form_invalid_phone_number: Profile with this Phone number already exists.'")
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ["Profile with this Phone number already exists."])


class SignUpFormTest(TestCase):

    def setUp(self):
        print("--"*35)

    def test_sign_up_form_valid(self):
        form = SignUpForm(
            data={
                'username': 'king',
                'first_name': 'Thorin',
                'last_name': 'Oakenshield',
                'email': 'thorinoak@mistymountains.com',
                'password1': 'Velmi_dulezite_heslo1',
                'password2': 'Velmi_dulezite_heslo1',  # hesla musí být stejná a projít django.user.auth pro heslo (znaky)
                'address': 'adresa',
                'phone_number': 123456789,
                'city': 'Město',
            }
        )
        print(f"\ntest_sign_up_form_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_sign_up_form_invalid_password(self):
        form = SignUpForm(
            data={
                'username': 'king',
                'first_name': 'Thorin',
                'last_name': 'Oakenshield',
                'email': 'thorinoak@mistymountains.com',
                'password1': 'password1',
                'password2': 'differentpassword',  # hesla se neshodují
                'address': 'adresa',
                'phone_number': 123456789,
                'city': 'Město',
            }
        )
        print(f"test_sign_up_form_invalid_password: Django.user.auth -> hesla se neshodují.")
        print(f"\nForm data: {form.data}")
        # print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())

    def test_sign_up_form_create_user(self):
        form = SignUpForm(
            data={
                'username': 'king',
                'first_name': 'Thorin',
                'last_name': 'Oakenshield',
                'email': 'thorinoak@mistymountains.com',
                'password1': 'Velmi_duleziteheslo1',
                'password2': 'Velmi_duleziteheslo1',
                'address': 'adresa',
                'phone_number': 123456789,
                'city': 'Město',
            }
        )
        if form.is_valid():
            user = form.save()
            self.assertEqual(User.objects.first().username, 'king')
            self.assertEqual(User.objects.first().email, 'thorinoak@mistymountains.com')
            self.assertEqual(Profile.objects.count(), 1)
            profile = Profile.objects.first()
            self.assertEqual(profile.address, 'adresa')
            self.assertEqual(int(profile.phone_number), 123456789)
            self.assertEqual(profile.city, 'Město')
            print(f"Registrace proběhla v pořádku: {form.data}")
        else:
            self.fail(f"Form is not valid: {form.errors}")