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
from django.core.paginator import Paginator
from django.db.models import Q

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
        products = Product.objects.filter(categories=category)  # Získání produktů v kategorii
        paginator = Paginator(products, 9)  # Paginace produktů po 3 na stránku
        page_number = self.request.GET.get('page')  # Získání čísla stránky z GET parametru
        page_obj = paginator.get_page(page_number)  # Získání aktuální stránky
        context["category"] = category
        context["products"] = products
        categories = Category.objects.all()
        for category in categories:
            category.product_count = Product.objects.filter(categories=category).count()
        context['categories'] = categories
        context['page_obj'] = page_obj
        try:
            context['user_city'] = self.request.user.profile.city
        except:
            context['user_city'] = 'Praha'
        return context


# Pohled pro zobrazení všech produktů
class ProductsListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 12  # Paginace produktů po 3 na stránku

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
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "produkty seřazené od nejlevnějšího"  # Nastavení aktuální šablony
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
    paginate_by = 12  # Paginace produktů po 3 na stránku

    def get_queryset(self):
        return Product.objects.order_by('-price')  # Seřazení produktů podle ceny sestupně

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "produkty seřazené od nejdražšího"  # Nastavení aktuální šablony
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
        context['categories'] = Category.objects.all()  # Získání všech kategorií
        context['current_template'] = "produkty seřazené od nejnovějšího"  # Nastavení aktuální šablony
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

# Pohled pro zobrazení produktů z orderlines (objednané produkty)
# class ProductsCartListView(ListView):
#     model = Product
#     template_name = 'cart.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()  # Získání všech kategorií
#         context['current_template'] = "Objednané produkty"  # Nastavení aktuální šablony
#         try:
#             context['user_city'] = self.request.user.profile.city
#         except:
#             context['user_city'] = 'Praha'
#         return context

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

    price = IntegerField(min_value=1, required=True)  # Pole pro cenu s minimální hodnotou 1
    stock = IntegerField(min_value=0, required=True)  # Pole pro sklady s minimální hodnotou 0

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
        except:
            context['user_city'] = 'Praha'
        return context

    def get(self, request, *args, **kwargs):
        product_form = ProductModelForm()
        return render(request, self.template_name, {'product_form': product_form})

    def post(self, request, *args, **kwargs):
        product_form = ProductModelForm(self.request.POST)
        if product_form.is_valid():
            product_form.save()
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

    # check if product is in order
    order_line, created = Order_Line.objects.get_or_create(Order=order, Product=cart_product, defaults={
        'product_price': cart_product.price,
        'quantity': quantity,
    })

    # if product in order update quantity
    if not created:
        order_line.quantity += quantity
        order_line.save()

    # update total cost of order
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

    # Existující logika košíku
    try:
        order = Order.objects.get(User=request.user.profile, status='Pending')
        order_lines = order.order_line_set.all().order_by('id')
        total_cost = order.total_cost

        # Calculate the total for each order line
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

        # Check if there are any order lines
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
        # Decrease the quantity by 1
        order_line.quantity -= 1
        order_line.save()
    else:
        # Remove the order line if quantity is 1
        order_line.delete()

    # Update the total cost of the order
    order = order_line.Order
    order.total_cost = sum(line.product_price * line.quantity for line in order.order_line_set.all())
    order.save()

    if not order.order_line_set.exists():
        order.delete()

    return redirect('cart_view')


@login_required
def delete_order_line(request, pk):
    order_line = get_object_or_404(Order_Line, id=pk, Order__User=request.user.profile, Order__status='Pending')

    # Get the associated order before deleting the line
    order = order_line.Order

    # Delete the order line
    order_line.delete()

    # Update the total cost of the order
    order.total_cost = sum(line.product_price * line.quantity for line in order.order_line_set.all())
    order.save()

    # Check if the order has no more order lines and delete the order if true
    if not order.order_line_set.exists():
        order.delete()

    return redirect('cart_view')


def checkout_view(request):
    context = {}
    context['current_template'] = "Pokladna"

    # Logika pro získání města uživatele
    try:
        if request.user.is_authenticated:
            context['user_city'] = request.user.profile.city
        else:
            context['user_city'] = 'Praha'
    except AttributeError:
        context['user_city'] = 'Praha'

    try:
        # Fetch the order based on the current user and status (assuming 'Pending')
        order = Order.objects.get(User=request.user.profile, status='Pending')

        # Fetch all order lines for the current order
        order_lines = order.order_line_set.all()

        # Calculate total cost of the order
        total_cost = order.total_cost  # Assuming total_cost is pre-calculated in the Order model

        # Prepare data for displaying in the template
        order_summary = []
        for line in order_lines:
            line_total = line.product_price * line.quantity
            order_summary.append({
                'product_title': line.Product.title,
                'quantity': line.quantity,
                'line_total': line_total,
            })

        # Add order data to context
        context.update({
            'order_summary': order_summary,
            'total_cost': total_cost,
            'order': order,
        })

    except Order.DoesNotExist:
        # Handle case where the order does not exist
        context.update({
            'order_summary': [],
            'total_cost': 0,
        })

    # Render the checkout template with the combined context
    return render(request, 'checkout.html', context)


@login_required
def place_order(request, pk):
    order = get_object_or_404(Order, id=pk, User=request.user.profile, status='Pending')
    order_lines = order.order_line_set.all()

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
        # order._processed = False  # Reset the flag to ensure the signal processes
        order.save()
        # messages.success(request, "Objednávka byla úspěšně vytvořena! Děkujeme! Nyní již potřebujeme jen vytvořit s.r.o., nakoupit stovky produktů, napojit skladový systém na databázi a zprovoznit tisíc dalších funkcí.")
        return redirect('order_confirmation')
    except Exception as e:
        messages.error(request, f"An error occurred while placing the order: {e}")
        return redirect('checkout')


def order_confirmation(request):
    return render(request, 'order_confirmation.html')


def search_view(request):

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

    return render(request, 'search_results.html',context)



# -----------------------------------------
# CART OPERATIONS END
# -----------------------------------------

# class ProductsCartListView(ListView): #TODO: vypsat produkty v pokladně z orderlines
#     model = Order_Line
#     template_name = 'cart.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product'] = Order_Line.objects.filter()
#         context['quantity'] = Order_Line.quantity
#         context['total'] = Order.total_cost
#         context['product_price'] = Product.price
#         return context


# class CheckoutView(ListView):
#     model = Order_Line
#     template_name = 'checkout.html'
#     context_object_name = 'order_lines'
#
#     def get_queryset(self):
#         order_id = self.kwargs['order_id']
#         order = get_object_or_404(Order, id=order_id)
#         return Order_Line.objects.filter(Order=order)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         order_id = self.kwargs['order_id']
#         order = get_object_or_404(Order, id=order_id)
#
#         total_price = sum(line.product_price * line.quantity for line in self.get_queryset())
#
#         context['order'] = order
#         context['total_price'] = total_price
#         return context

# class CheckoutView(TemplateView):
#     template_name = 'checkout.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         order_id = self.kwargs.get('order_id')
#
#         order = get_object_or_404(Order, pk=order_id)
#         order_lines = Order_Line.objects.filter(Order=order)
#
#         total_price = sum(line.product_price * line.quantity for line in order_lines)
#
#         context['order'] = order
#         context['order_lines'] = order_lines
#         context['total_price'] = total_price
#         return context
