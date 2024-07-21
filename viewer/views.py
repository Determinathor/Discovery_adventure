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


from viewer.models import *

from django.forms import *


def home(request):
    return render(request, "home.html")

class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "FAQ"
        return context

def hello(request):
    return render(request, "hello.html")


class Contactview(TemplateView):
    template_name = "contact.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "kONTAKT"
        return context

class CategoryListView(ListView): # chceme zobrazit všechny kategorie
    model = Category
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        for category in categories:
            category.product_count = Product.objects.filter(categories=category).count()
        context['categories'] = categories
        context['current_template'] = "Kategorie"
        return context


class CategoryTemplateView(TemplateView): # chceme vypsat produkty v dané kategorii
    template_name = "products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(categories=category)
        paginator = Paginator(products, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["category"] = category
        context["products"] = products
        categories = Category.objects.all()
        for category in categories:
            category.product_count = Product.objects.filter(categories=category).count()
        context['categories'] = categories
        context['page_obj'] = page_obj
        return context


class ProductsListView(ListView):  # chceme vypsat všechny produkty
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "Všechny produkty"
        return context


class ProductSortedHighListView(ListView): # chceme vypsat produkty serazene od nejlevnějšího
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "produkty seřazené od nejlevnějšího"
        return context


class ProductSortedLowListView(ListView): # chceme vypsat produkty serazene od nejdražšího
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.order_by('-price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "produkty seřazené od nejdražšího"
        return context


class ProductNewestListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "produkty seřazené od nejnovějšího"
        return context

class ProductTemplateView(TemplateView): # chceme zobrazit konkrétní produkt s popisem
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        product_ = Product.objects.get(id=pk)
        conversion_rate = 25.5
        context["product"] = product_
        context["title"] = product_.title
        context["description"] = product_.description
        context["price"] = product_.price
        context["manufacturer"] = product_.manufacturer
        context["conversion_rate"] = conversion_rate
        context["price_czk"] = product_.price * conversion_rate # TODO: aktuální cena czk -> eur?
        context['categories'] = Category.objects.all()
        context['current_template'] = "detail produktu"
        return context
        # context["reviews"] = Review.objects.filter(product=product_) TODO: chceme vypisovat a tvořit review pro produkt?
        # context["form_review"] = ReviewModelForm


class RandomProductTemplateView(TemplateView):
    template_name = 'random_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_count = Product.objects.count()
        if product_count > 0:
            while True:
                random_index = random.randint(0, product_count - 1)
                if Product.objects.filter(id=random_index).exists():
                    random_product = Product.objects.get(pk=random_index)
                    break
        else:
            random_product = None
        context["product"] = random_product
        context['categories'] = Category.objects.all()
        context['current_template'] = "Náhodný produkt"
        return context
# -----------------------------------------
# CRUD_product OPERATIONS START
# -----------------------------------------
class ProductModelForm(ModelForm): # formulář pro produkt
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'categories': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('shop')
            )
        }

    price = IntegerField(min_value=0, required=True)
    stock = IntegerField(min_value=0, required=True)

    def clean_title(self):
        initial = self.cleaned_data['title']
        return initial.strip()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "Formulář produktu"
        return context


class ProductCreateView(PermissionRequiredMixin, CreateView): # autorizace + vytvoření produktu skrze formulář
    template_name = 'product_create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.add_product'

    def form_invalid(self, form):
        LOGGER.warning('Invalid data in ProductCreateView.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "Vytváření produktu"
        return context


class ProductUpdateView(PermissionRequiredMixin, UpdateView): # update produktu (stock, cena apod)
    template_name = 'product_create.html'
    model = Product
    form_class = ProductModelForm
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.change_product'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a product.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "úprava produktu"
        return context


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProductDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('shop')
    permission_required = 'accounts.delete_product'

# -----------------------------------------
# CRUD_product OPERATIONS END
# -----------------------------------------


# -----------------------------------------
# CART OPERATIONS START
# -----------------------------------------


@login_required
def add_to_cart(request, pk):
    cart_product = get_object_or_404(Product, id=pk)

    # get or create order for user
    order, created = Order.objects.get_or_create(User=request.user.profile, status='Pending', defaults={
        'delivery_address': '',
        'date_of_sale': timezone.now(),
        'total_cost': 0,
    })

    # check if product is in order
    order_line, created = Order_Line.objects.get_or_create(Order=order, Product=cart_product, defaults={
        'product_price': cart_product.price,
        'quantity': 1,
    })

    # if product in order update quantity
    if not created:
        order_line.quantity += 1
        order_line.save()

    # update total cost of order
    order.total_cost = sum(line.Product.price * line.quantity for line in order.order_line_set.all())
    order.save()

    return redirect('cart_view')


def cart_view(request):
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

    return render(request, 'cart.html', {
        'order_lines': order_lines_with_total,
        'total_cost': total_cost,
        'has_items': has_items,
    })


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

        # Render the checkout template with the order summary data
        return render(request, 'checkout.html', {
            'order_summary': order_summary,
            'total_cost': total_cost,
            'order': order,
        })

    except Order.DoesNotExist:
        # Handle case where the order does not exist
        return render(request, 'checkout.html', {'order_summary': [], 'total_cost': 0})


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
        messages.success(request, "Order placed successfully!")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An error occurred while placing the order: {e}")
        return redirect('checkout')



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






