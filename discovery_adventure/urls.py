
from django.contrib import admin
from django.urls import path, include
from discovery_adventure import settings
from discovery_adventure.context_processors import search_results

from viewer import views
from accounts.views import SignUpView, my_view, ProfileUpdateView, CustomPasswordChangeView

from viewer.views import home, ProductsListView, ProductTemplateView, ProductCreateView, CategoryListView, \
    CategoryTemplateView, RandomProductTemplateView, FAQView, \
    ProductUpdateView, ProductDeleteView, ProductSortedLowListView, ProductSortedHighListView, \
    add_to_cart, cart_view, delete_order_line, remove_from_cart, Contactview, checkout_view, place_order, \
    CategoryCreateView, order_confirmation, product_select_view

urlpatterns = [

    path('hello/', views.hello, name='hello'),

    path('', CategoryListView.as_view(), name='home'), # "domovská stránka", která zobrazuje kategorie

    path('shop/', ProductsListView.as_view(), name='shop'), # zobrazení všech produktů
    path('category/create/', CategoryCreateView.as_view(), name='category_create'), # vytvoření kategorie
    path('category/<pk>/', CategoryTemplateView.as_view(), name='category'), # zobrazení produktů dané kategorie
    path('shop/random/', RandomProductTemplateView.as_view(), name='random'),
    path('shop/<pk>/', ProductTemplateView.as_view(), name='detail'), # zobrazení detailu produktu
    path('shop-nejdrazsi/', ProductSortedLowListView.as_view(), name='shop-nejdrazsi'), #zobrazi vsechny produkty serazene od nejlevnejsiho
    path('shop-nejlevnejsi/', ProductSortedHighListView.as_view(), name='shop-nejlevnejsi'), #zobrazi vsechny produkty serazene od nejdrazsiho
    path('products/select/', product_select_view, name='product_select'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'), # vytvoření produktu
    path('product/update/<pk>/', ProductUpdateView.as_view(), name='product_update'), # update produktu
    path('product/delete/<pk>/', ProductDeleteView.as_view(), name='product_delete'), # odstranění produktu
    path('search/', views.search_view, name='search_results'),

    path('faq/', FAQView.as_view(), name='faq'), # faq stránka
    path('contact/', Contactview.as_view(), name='contact'), # kontakt stránka

    path('add-to-cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove_from_cart'),
    path('delete-order-line/<pk>/', delete_order_line, name='delete_order_line'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout_view, name='checkout'),
    path('place_order/<pk>/', place_order, name='place_order'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),


    path('accounts/login/', my_view, name='login'),  # vlastní view pro login
    path('accounts/signup/', SignUpView.as_view(), name='signup'),          # vlastní view pro signup
    path('accounts/password_change/', CustomPasswordChangeView.as_view(), name='password_change'), # view pro změnu hesla
    path('accounts/info_change/', ProfileUpdateView.as_view(), name='profile_update'), # view pro změnu údajů
    path('accounts/', include('django.contrib.auth.urls')), # default django view

    path('admin/', admin.site.urls),

]

