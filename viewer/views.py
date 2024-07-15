import random
from concurrent.futures._base import LOGGER

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.paginator import Paginator

from viewer.models import *

from django.forms import *


# Funkce pro zobrazení úvodní stránky
def home(request):
    return render(request, "home.html")

# Pohled pro FAQ stránku
class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "FAQ"  # Nastavení aktuální šablony
        return context

# Funkce pro zobrazení uvítací stránky
def hello(request):
    return render(request, "hello.html")

# Pohled pro kontaktní stránku
class Contactview(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "kONTAKT"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení seznamu kategorií
class CategoryListView(ListView):
    model = Category
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()  # Získání všech kategorií
        for category in categories:
            # Spočítání počtu produktů v každé kategorii
            category.product_count = Product.objects.filter(categories=category).count()
        context['categories'] = categories
        context['current_template'] = "Kategorie"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení produktů v konkrétní kategorii
class CategoryTemplateView(TemplateView):
    template_name = "products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']  # Získání ID kategorie z URL
        category = get_object_or_404(Category, pk=pk)  # Získání kategorie nebo 404 pokud neexistuje
        products = Product.objects.filter(categories=category)  # Získání produktů v kategorii
        paginator = Paginator(products, 3)  # Paginace produktů po 3 na stránku
        page_number = self.request.GET.get('page')  # Získání čísla stránky z GET parametru
        page_obj = paginator.get_page(page_number)  # Získání aktuální stránky
        context["category"] = category
        context["products"] = products
        categories = Category.objects.all()
        for category in categories:
            category.product_count = Product.objects.filter(categories=category).count()
        context['categories'] = categories
        context['page_obj'] = page_obj
        return context

# Pohled pro zobrazení všech produktů
class ProductsListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3  # Paginace produktů po 3 na stránku

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Všechny produkty"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení produktů seřazených od nejlevnějšího
class ProductSortedHighListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3  # Paginace produktů po 3 na stránku

    def get_queryset(self):
        return Product.objects.order_by('price')  # Seřazení produktů podle ceny vzestupně

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "produkty seřazené od nejlevnějšího"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení produktů seřazených od nejdražšího
class ProductSortedLowListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3  # Paginace produktů po 3 na stránku

    def get_queryset(self):
        return Product.objects.order_by('-price')  # Seřazení produktů podle ceny sestupně

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "produkty seřazené od nejdražšího"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení nejnovějších produktů
class ProductNewestListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3  # Paginace produktů po 3 na stránku

    def get_queryset(self):
        return Product.objects.order_by('-created_at')  # Seřazení produktů podle data vytvoření (novější první)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "produkty seřazené od nejnovějšího"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení detailu konkrétního produktu
class ProductTemplateView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']  # Získání ID produktu z URL
        product_ = Product.objects.get(id=pk)  # Získání produktu podle ID
        conversion_rate = 25.5  # Převodní kurz pro cenu (CZK na EUR)
        context["product"] = product_
        context["title"] = product_.title
        context["description"] = product_.description
        context["price"] = product_.price
        context["manufacturer"] = product_.manufacturer
        context["conversion_rate"] = conversion_rate
        context["price_czk"] = product_.price * conversion_rate  # Přepočet ceny na CZK
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "detail produktu"  # Nastavení aktuální šablony
        return context
        # context["reviews"] = Review.objects.filter(product=product_)  # TODO: Chceme vypisovat a tvořit recenze pro produkt?
        # context["form_review"] = ReviewModelForm

# Pohled pro zobrazení náhodného produktu
class RandomProductTemplateView(TemplateView):
    template_name = 'random_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_count = Product.objects.count()  # Získání počtu produktů
        if product_count > 0:
            while True:
                random_index = random.randint(0, product_count - 1)  # Generování náhodného indexu produktu
                if Product.objects.filter(id=random_index).exists():  # Kontrola existence produktu s tímto ID
                    random_product = Product.objects.get(pk=random_index)
                    break
        else:
            random_product = None
        context["product"] = random_product
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Náhodný produkt"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení všech produktů v košíku
class ProductsCheckoutListView(ListView):
    model = Product
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Všechny produkty v košíku"  # Nastavení aktuální šablony
        return context

# Pohled pro zobrazení produktů z orderlines (objednané produkty)
class ProductsCartListView(ListView):
    model = Product
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Objednané produkty"  # Nastavení aktuální šablony
        return context

# Formulář pro vytvoření/úpravu produktu
class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'categories': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('shop')  # URL pro přidání nové kategorie
            )
        }

    price = IntegerField(min_value=0, required=True)  # Pole pro cenu s minimální hodnotou 0
    stock = IntegerField(min_value=0, required=True)  # Pole pro sklady s minimální hodnotou 0

    def clean_title(self):
        initial = self.cleaned_data['title']
        return initial.strip()  # Odstranění mezer na začátku a konci názvu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Formulář produktu"  # Nastavení aktuální šablony
        return context

# Pohled pro vytvoření nového produktu
class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'product_create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.add_product'

    def form_invalid(self, form):
        LOGGER.warning('Invalid data in ProductCreateView.')  # Logování chyby při neplatném formuláři
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Vytváření produktu"  # Nastavení aktuální šablony
        return context

# Pohled pro úpravu existujícího produktu
class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductModelForm
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.change_product'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a product.')  # Logování chyby při neplatném formuláři
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "úprava produktu"  # Nastavení aktuální šablony
        return context

# Mixin pro kontrolu, zda je uživatel staff (administrátor)
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # Kontrola, zda je uživatel staff

# Pohled pro smazání produktu (pouze pro administrátory)
class ProductDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.delete_product'
