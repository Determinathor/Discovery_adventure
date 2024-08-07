from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import DateField, CharField, Textarea, NumberInput, IntegerField, ModelForm, TextInput
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from pydantic import ValidationError

from accounts.models import Profile
from discovery_adventure import settings
from viewer.models import Category


def my_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username and password:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User exisujue a je ověřen
            login(request, user)
            messages.success(request, 'Přihlášení bylo úspěšné.')
            return redirect('home')
        else:
            # Chyba v ověření
            if User.objects.filter(username=username).exists():
                # Username exisutje ale heslo ne nesprávné
                messages.error(request,
                               'Nelze se přihlásit. Uživatelské jméno nebo heslo jsou nesprávné. ')
            else:
                # Username neexistuje
                messages.error(request,
                               'Nelze se přihlásit. Uživatelské jméno neexistuje. Chcete se registrovat?')
                               # 'Chcete se <a href="#" onclick="openSignupModal()">registrovat</a>?')
    else:
        # Uživatel není registrován (chybí username i heslo)
        messages.error(request,
                       'Pro přidání produktu do košíku je potřeba se nejprve '
                       '<a href="#" onclick="openSignupModal()">registrovat</a> '
                       'nebo <a href="#" onclick="openLoginModal()">přihlásit</a>. ')

    return redirect('home')


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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registrace byla úspěšná, nyní se můžete přihlásit.')
                                       # ' <a href="#" onclick="openLoginModal()">přihlásit</a>.')
        return response


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Staré heslo",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label="Nové heslo",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="<ul>"
                  "<li>Vaše heslo nesmí být příliš podobné vašim ostatním osobním údajům.</li>"
                  "<li>Vaše heslo musí obsahovat alespoň 8 znaků.</li>"
                  "<li>Vaše heslo nesmí být běžně používané heslo.</li>"
                  "</ul>",
    )
    new_password2 = forms.CharField(
        label="Potvrzení nového hesla",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Změna hesla'
        context['submit_text'] = 'Změnit heslo'
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Heslo bylo úspěšně změněno')
        return response


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'E-mailová adresa',
        }
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'John'}),
            'last_name': TextInput(attrs={'placeholder': 'Doe'}),
            'email': TextInput(attrs={'placeholder': 'johndoe@da.cz'}),
        }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'city']
        labels = {
            'phone_number': 'Telefonní číslo',
            'address': 'Adresa',
            'city': 'Město',
        }
        widgets = {
            'address': TextInput(attrs={'placeholder': 'Zbožná 123'}),
            'city': TextInput(attrs={'placeholder': 'Boží Dar'}),
            'phone_number': TextInput(attrs={'placeholder': 'Ve tvaru: 123456789'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

    def clean_phone_number(self):   # validace, jestliže necháváme telefonní číslo stejné (je unique)
        phone_number = self.cleaned_data.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exclude(user=self.user).exists():
            raise forms.ValidationError("Profile with this Phone number already exists.")
        return phone_number


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile_update')

    def get_common_context(self):
        context = {
            'categories': Category.objects.all(),
            'current_template': "Update profilu"
        }
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile, user=request.user)
        context = self.get_common_context()
        context.update({
            'user_form': user_form,
            'profile_form': profile_form
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile, user=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Změna osobních údajů proběhla úspěšně.')
            return redirect(self.success_url)

        context = self.get_common_context()
        context.update({
            'user_form': user_form,
            'profile_form': profile_form
        })
        return render(request, self.template_name, context)


