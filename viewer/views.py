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
        context['current_template'] = "Všechny produkty"
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


class ProductsCheckoutListView(ListView): #TODO: vypsat všechny produkty v košíku
    model = Product
    template_name = 'checkout.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "Všechny produkty v košíku"
        return context


class ProductsCartListView(ListView): #TODO: vypsat produkty z orderlines
    model = Product
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_template'] = "Objednané produkty"
        return context


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






