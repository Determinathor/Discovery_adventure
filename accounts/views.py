from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import DateField, CharField, Textarea, NumberInput, IntegerField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    address = CharField(max_length=80)
    phone_number = IntegerField()
    city = CharField(max_length=42)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)
        # email = self.cleaned_data.get('email')
        address = self.cleaned_data.get('address')
        phone_number = self.cleaned_data.get('phone_number')
        city = self.cleaned_data.get('city')
        profile = Profile(user=user, address=address, phone_number=phone_number, city=city)
        if commit:
            profile.save()
        return user


class SignUpView(CreateView):
    template_name = "form.html"
    form_class = SignUpForm
    success_url = reverse_lazy('home')


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')
