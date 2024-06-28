from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import DateField, CharField, Textarea, NumberInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)
        email = self.cleaned_data.get('email')
        profile = Profile(user=user, email=email)
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
