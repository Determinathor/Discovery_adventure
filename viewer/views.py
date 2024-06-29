from concurrent.futures._base import LOGGER

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper

from viewer.models import *

from django.forms import *


def home(request):
    return render(request, "home.html")


def faq(request):
    return render(request, "faq.html")


def hello(request):
    return render(request, "hello.html")


class CategoryListView(ListView): # chceme zobrazit všechny kategorie
    model = Category
    template_name = "home.html"


class CategoryTemplateView(TemplateView): # chceme vypsat produkty v dané kategorii TODO: category_name
    template_name = "products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        category = Category.objects.get(id=pk)
        products = Product.objects.filter(categories=category)
        context["category"] = category
        context["products"] = products
        return context


class ProductsListView(ListView):  # chceme vypsat všechny produkty
    model = Product
    template_name = 'shop.html'


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
        return context
        # context["reviews"] = Review.objects.filter(product=product_) TODO: chceme vypisovat a tvořit review pro produkt?
        # context["form_review"] = ReviewModelForm



class ProductModelForm(ModelForm): # formulář pro produkt
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock', 'thumbnail']
        widgets = {
            'category': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('shop')
            )
        }

    price = IntegerField(min_value=0, required=True)
    stock = IntegerField(min_value=0, required=True)

    def clean_title(self):
        initial = self.cleaned_data['title']
        return initial.strip()


class ProductCreateView(PermissionRequiredMixin, CreateView): # autorizace + vytvoření produktu skrze formulář
    template_name = 'form_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('shop')
    #TODO: správnost viewer.add_product?
    permission_required = 'viewer.add_product'

    def form_invalid(self, form):
        LOGGER.warning('Invalid data in ProductCreateView.')
        return super().form_invalid(form)


class ProductUpdateView(PermissionRequiredMixin, UpdateView): # update produktu (stock, cena apod)
    template_name = 'form_product.html'
    model = Product
    form_class = ProductModelForm
    success_url = reverse_lazy('shop')
    permission_required = 'viewer.change_product'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a product.')
        return super().form_invalid(form)






