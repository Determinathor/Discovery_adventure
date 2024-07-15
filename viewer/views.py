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

from viewer.models import *

from django.forms import *


def home(request):
    return render(request, "home.html")



class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



def hello(request):
    return render(request, "hello.html")




class CategoryListView(ListView): # chceme zobrazit všechny kategorie
    model = Category
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryTemplateView(TemplateView): # chceme vypsat produkty v dané kategorii
    template_name = "products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        category = Category.objects.get(pk=pk) # TODO: category_name
        products = Product.objects.filter(categories=category)
        context["category"] = category
        context["products"] = products
        context['categories'] = Category.objects.all()
        return context


class ProductsListView(ListView):  # chceme vypsat všechny produkty
    model = Product
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductSortedHighListView(ListView): # chceme vypsat produkty serazene od nejdrazsiho
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('price')


class ProductSortedLowListView(ListView): # chceme vypsat produkty serazene od nejlevnejsiho
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-price')


class ProductNewestListView:
    pass

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
    except Order.DoesNotExist:
        order_lines_with_total = []
        total_cost = 0

    return render(request, 'cart.html', {
        'order_lines': order_lines_with_total,
        'total_cost': total_cost,
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

    return redirect('cart_view')


# -----------------------------------------
# CART OPERATIONS END
# -----------------------------------------

# class ProductsCartListView(ListView): #TODO: vypsat produkty v košíku z orderlines
#     model = Order_Line
#     template_name = 'cart.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product'] = Order_Line.objects.filter()
#         context['quantity'] = Order_Line.quantity
#         context['total'] = Order.total_cost
#         context['product_price'] = Product.price
#         return context


class ProductsCheckoutListView(ListView): #TODO: vypsat všechny produkty v checkoutu
    model = Product
    template_name = 'checkout.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context






