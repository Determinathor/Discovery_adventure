from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import DateField, CharField, Textarea, NumberInput, IntegerField
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.models import Profile
from discovery_adventure import settings


def my_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')

# class SubmittableLoginView(View):
    # def post(self, request, *args, **kwargs):
    #     if request.method == "POST":
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')
    #         user = User.objects.get(username=username)
    #         login(request, user)
    #     return redirect('home')
    # reverse_lazy = 'home'

    # def get(self, request, *args, **kwargs):
    #     form = AuthenticationForm()
    #     return render(request, 'login.html', {'form': form})

    # def post(self, request, *args, **kwargs):
    #     if request.method == "POST":
    #         form = AuthenticationForm(request, data=request.POST)
    #         if form.is_valid():
    #             username = form.cleaned_data.get('username')
    #             password = form.cleaned_data.get('password')
    #             user = authenticate(request, username=username, password=password)
    #             if user is not None:
    #                 login(request, user)
    #                 return redirect('home')
    #             else:
    #                 form.add_error(None, "Invalid username or password")
    #     return redirect('home')
    #
    # reverse_lazy = 'home'

    # def get(self, request, *args, **kwargs):
    #     # If user is already authenticated, redirect to LOGIN_REDIRECT_URL
    #     if request.user.is_authenticated:
    #         return redirect('home')
    #
    #     form = AuthenticationForm()
    #     return redirect('home')

    # def post(self, request, *args, **kwargs):
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    #         else:
    #             form.add_error(None, "Invalid username or password")
    #     print("nevalidni formulař")
    #     # If form is invalid or authentication fails, render the login form with errors
    #     return redirect('home')

    
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
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     # Create the Profile for the user
    #     user = form.instance
    #     Profile.objects.create(
    #         user=user,
    #         address=form.cleaned_data.get('address'),
    #         phone_number=form.cleaned_data.get('phone_number'),
    #         city=form.cleaned_data.get('city')
    #     )
    #     # Add the success message
    #     messages.success(self.request, 'Účet byl úspěšně vytvořen! Můžete se nyní přihlásit.')
    #     return response



class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')
