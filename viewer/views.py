import random
from concurrent.futures._base import LOGGER

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models.functions import datetime
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from accounts.views import ProfileUpdateForm
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
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
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
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
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
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'

        return context


# Pohled pro zobrazení produktů v konkrétní kategorii
class CategoryTemplateView(TemplateView):
    template_name = "products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']  # Získání ID kategorie z URL
        category = get_object_or_404(Category, pk=pk)  # Získání kategorie nebo 404 pokud neexistuje

        # Získání produktů v kategorii
        products = Product.objects.filter(categories=category)

        # Paginace produktů po 9 na stránku
        paginator = Paginator(products, 9)
        page_number = self.request.GET.get('page', 1)  # Získání čísla stránky z GET parametru

        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # Pokud je číslo stránky větší než počet stránek

        context["category"] = category
        context['page_obj'] = page_obj
        context['categories'] = Category.objects.all()

        # Nastavení počtu produktů v každé kategorii
        for cat in context['categories']:
            cat.product_count = Product.objects.filter(categories=cat).count()

        # Nastavení města uživatele
        user = self.request.user
        if hasattr(user, 'profile'):
            context['user_city'] = user.profile.city
        else:
            context['user_city'] = 'Praha'

        return context


# Pohled pro zobrazení všech produktů
class ProductsListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 12  # Paginace produktů po 12 na stránku

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Všechny produkty"  # Nastavení aktuální šablony
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


# Pohled pro zobrazení produktů seřazených od nejlevnějšího
class ProductSortedHighListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 12  # Paginace produktů po 3 na stránku

    def get_queryset(self):
        return Product.objects.order_by('price')  # Seřazení produktů podle ceny vzestupně

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "produkty seřazené od nejlevnějšího"
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


# Pohled pro zobrazení produktů seřazených od nejdražšího
class ProductSortedLowListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.order_by('-price')  # Seřazení produktů podle ceny sestupně

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "produkty seřazené od nejdražšího"
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
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
        context['categories'] = Category.objects.all()
        context['current_template'] = "produkty seřazené od nejnovějšího"
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
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
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context
        # context["reviews"] = Review.objects.filter(product=product_)
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

        if random_product:
            conversion_rate = 25.5  # Převodní kurz pro cenu (CZK na EUR)
            context["product"] = random_product
            context["title"] = random_product.title
            context["description"] = random_product.description
            context["price"] = random_product.price
            context["manufacturer"] = random_product.manufacturer
            context["conversion_rate"] = conversion_rate
            context["price_czk"] = random_product.price * conversion_rate  # Přepočet ceny na CZK

        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Náhodný produkt"  # Nastavení aktuální šablony
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


# Pohled pro zobrazení všech produktů v košíku
class ProductsCheckoutListView(ListView):
    model = Product
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Všechny produkty v košíku"  # Nastavení aktuální šablony
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


# -----------------------------------------
# CRUD_product OPERATIONS START
# -----------------------------------------

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

    price = IntegerField(min_value=1, required=True) # Pole pro cenu s minimální hodnotou 1
    # price = IntegerField(required=True)  # TEST VALIDACE BEZ INTEGER FIELD S VLASTNÍ ERROR MESSAGE
    # stock = IntegerField(min_value=0, required=True)  # S DEFAULT VALIDACÍ INTEGER FORM (ERROR_MSG)
    stock = IntegerField(required=True)  # Pole pro sklady s minimální hodnotou 0

    def clean_title(self):
        initial = self.cleaned_data['title']
        return initial.strip()  # Odstranění mezer na začátku a konci názvu

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError('Stock cannot be negative.')
        return stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "Formulář produktu"  # Nastavení aktuální šablony
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
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
        try:
            context['user_city'] = self.request.user.profile.city
        except AttributeError:
            context['user_city'] = 'Praha'
        return context

    def get(self, request, *args, **kwargs):
        product_form = ProductModelForm()
        return render(request, self.template_name, {'product_form': product_form})

    def post(self, request, *args, **kwargs):
        product_form = ProductModelForm(self.request.POST)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Produkt byl úspěšně vytvořen.')
            return redirect('shop')
        else:
            messages.error(request, "Nastala chyba při tvorbě produktu.")
            return redirect('shop')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):  # update produktu (stock, cena apod)
    template_name = 'product_update.html'
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
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context

    def get(self, request, *args, **kwargs):
        product_form = ProductModelForm(instance=self.get_object())
        return render(request, self.template_name, {'product_form': product_form})

    def post(self, request, *args, **kwargs):
        product_form = ProductModelForm(request.POST, instance=self.get_object())

        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Produkt byl úspěšně aktualizován.')
            return redirect('product_select')
        else:
            messages.error(request, "Nastala chyba při aktualizaci produktu.")
            return redirect('product_select')


class ProductSelectForm(forms.Form):
    product = ModelChoiceField(queryset=Product.objects.all(), label="Vyber")


def product_select_view(request):
    if request.method == 'POST':
        form = ProductSelectForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            return redirect('product_update', pk=product.pk)
    else:
        form = ProductSelectForm()

    return render(request, 'product_select.html', {'form': form})


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # Kontrola, zda je uživatel staff


# Pohled pro smazání produktu (pouze pro administrátory)
class ProductDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.delete_product'


# -----------------------------------------
# CRUD_product OPERATIONS END
# -----------------------------------------


class CategoryModelForm(ModelForm):  # formulář pro kategorii
    class Meta:
        model = Category
        fields = '__all__'

    def clean_title(self):
        initial = self.cleaned_data['name']
        return initial.strip()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_template'] = "Formulář kategorie"
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


class CategoryCreateView(PermissionRequiredMixin, CreateView):  # autorizace + vytvoření kategorie skrze formulář
    template_name = 'category_create.html'
    form_class = CategoryModelForm
    success_url = reverse_lazy('home')
    permission_required = 'accounts.add_category'

    def form_invalid(self, form):
        LOGGER.warning('Invalid data in CategoryCreateView.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_template'] = "Vytváření kategorie"
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


# -----------------------------------------
# CART OPERATIONS START
# -----------------------------------------


@login_required
def add_to_cart(request, pk):
    cart_product = get_object_or_404(Product, id=pk)

    # Get quantity from request, default to 1 if not provided
    quantity = int(request.GET.get('quantity', 1))

    # get or create order for user
    order, created = Order.objects.get_or_create(User=request.user.profile, status='Pending', defaults={
        'delivery_address': '',
        'date_of_sale': timezone.now(),
        'total_cost': 0,
    })

    order_line, created = Order_Line.objects.get_or_create(Order=order, Product=cart_product, defaults={
        'product_price': cart_product.price,
        'quantity': quantity,
    })

    # update počtu produktů
    if not created:
        order_line.quantity += quantity
        order_line.save()

    # update ceny order
    order.total_cost = sum(line.Product.price * line.quantity for line in order.order_line_set.all())
    order.save()

    return redirect('cart_view')


def cart_view(request):
    context = {}
    context['current_template'] = "Košík"

    # Logika pro získání města uživatele
    try:
        if request.user.is_authenticated:
            context['user_city'] = request.user.profile.city
        else:
            context['user_city'] = 'Praha'
    except AttributeError:
        context['user_city'] = 'Praha'

    try:
        order = Order.objects.get(User=request.user.profile, status='Pending')
        order_lines = order.order_line_set.all().order_by('id')
        total_cost = order.total_cost

        # výpočet ceny pro každou order_line
        order_lines_with_total = []
        for line in order_lines:
            line_total = line.product_price * line.quantity
            order_lines_with_total.append({
                'id': line.id,
                'Product': line.Product,
                'quantity': line.quantity,
                'product_price': line.product_price,
                'line_total': line_total,
            })

        has_items = order_lines.exists()

    except Order.DoesNotExist:
        order_lines_with_total = []
        total_cost = 0
        has_items = False

    # Přidání dat košíku do kontextu
    context.update({
        'order_lines': order_lines_with_total,
        'total_cost': total_cost,
        'has_items': has_items,
    })

    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, pk):
    order_line = get_object_or_404(Order_Line, id=pk, Order__User=request.user.profile, Order__status='Pending')

    if order_line.quantity > 1:
        order_line.quantity -= 1
        order_line.save()
    else:
        # smaže order_line, jestliže je menší než 1
        order_line.delete()

    # Update celkové ceny
    order = order_line.Order
    order.total_cost = sum(line.product_price * line.quantity for line in order.order_line_set.all())
    order.save()

    if not order.order_line_set.exists():
        order.delete()

    return redirect('cart_view')


@login_required
def delete_order_line(request, pk):
    order_line = get_object_or_404(Order_Line, id=pk, Order__User=request.user.profile, Order__status='Pending')

    order = order_line.Order

    order_line.delete()

    # Update celkové ceny
    order.total_cost = sum(line.product_price * line.quantity for line in order.order_line_set.all())
    order.save()

    # smaže order jestliže nejsou další order_lines
    if not order.order_line_set.exists():
        order.delete()

    return redirect('cart_view')


def checkout_view(request):
    context = {}
    context['current_template'] = "Pokladna"

    try:
        if request.user.is_authenticated:
            context['user_city'] = request.user.profile.city
        else:
            context['user_city'] = 'Praha'
    except AttributeError:
        context['user_city'] = 'Praha'

    try:
        order = Order.objects.get(User=request.user.profile, status='Pending')
        order_lines = order.order_line_set.all()

        # výpočet celkové ceny order
        total_cost = order.total_cost

        order_summary = []
        for line in order_lines:
            line_total = line.product_price * line.quantity
            order_summary.append({
                'product_title': line.Product.title,
                'quantity': line.quantity,
                'line_total': line_total,
            })

        context.update({
            'order_summary': order_summary,
            'total_cost': total_cost,
            'order': order,
        })

    except Order.DoesNotExist:
        context.update({
            'order_summary': [],
            'total_cost': 0,
        })


    return render(request, 'checkout.html', context)

@login_required
def place_order(request, pk):
    order = get_object_or_404(Order, id=pk, User=request.user.profile, status='Pending')
    order_lines = order.order_line_set.all()

    if request.method == 'POST':
        user = request.user
        profile = user.profile

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')

        # kontrola atributů usera (příp update)
        if user.first_name != first_name:
            user.first_name = first_name
        if user.last_name != last_name:
            user.last_name = last_name
        if user.email != email:
            user.email = email
        user.save()

        # kontrola atributů profilu (příp update)
        if profile.phone_number != phone_number:
            profile.phone_number = phone_number
        if profile.address != address:
            profile.address = address
        if profile.city != city:
            profile.city = city
        profile.save()

        try:
            for line in order_lines:
                product = line.Product
                if product.stock >= line.quantity:
                    product.stock -= line.quantity
                    product.save()
                else:
                    messages.error(request, f"Insufficient stock for {product.title}")
                    return redirect('checkout')

            order.status = 'Confirmed'
            order.save()
            return redirect('order_confirmation')
        except Exception as e:
            messages.error(request, f"An error occurred while placing the order: {e}")
            return redirect('checkout')

    return redirect('checkout')


def order_confirmation(request):
    return render(request, 'order_confirmation.html')


def search_view(request):

    context = {}
    context['current_template'] = "Hledání"

    try:
        if request.user.is_authenticated:
                context['user_city'] = request.user.profile.city
        else:
                context['user_city'] = 'Praha'
    except AttributeError:
        context['user_city'] = 'Praha'

    return render(request, 'search_results.html',context)


# def custom_404(request, exception):
#     return render(request, '404.html', status=404)
#
# def custom_500(request):
#     return render(request, '500.html', status=500)


# -----------------------------------------
# CART OPERATIONS END
# -----------------------------------------


