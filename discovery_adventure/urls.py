
from django.contrib import admin
from django.urls import path, include
from discovery_adventure import settings

from viewer import views
from accounts.views import SubmittableLoginView, SignUpView, SubmittablePasswordChangeView

from viewer.views import home, ProductsListView, ProductTemplateView, ProductCreateView, CategoryListView, \
    CategoryTemplateView, faq, ProductsCheckoutListView, ProductsCartListView, RandomProductTemplateView, \
    ProductUpdateView, ProductDeleteView

urlpatterns = [

    path('hello/', views.hello, name='hello'),

    path('', CategoryListView.as_view(), name='home'), # "domovská stránka", která zobrazuje kategorie

    # path('index/', CategoryListView.as_view(), name='index'), # "domovská stránka", která zobrazuje kategorie
    path('shop/', ProductsListView.as_view(), name='shop'), # zobrazení všech produktů
    path('category/<pk>/', CategoryTemplateView.as_view(), name='category'), # zobrazení produktů dané kategorie TODO: chceme místo pk vypsat category_name
    path('shop/random/', RandomProductTemplateView.as_view(), name='random'),
    path('shop/<pk>/', ProductTemplateView.as_view(), name='detail'), # zobrazení detailu produktu TODO: aby byla adresář shop/product/<pk>
    path('product/create/', ProductCreateView.as_view(), name='product_create'), # vytvoření produktu
    path('product/update/<pk>/', ProductUpdateView.as_view(), name='product_create'), # update produktu
    path('product/delete/<pk>/', ProductDeleteView.as_view(), name='product_delete'), # odstranění produktu
    path('faq/', views.faq, name='faq'), # faq stránka
    path('checkout/', ProductsCheckoutListView.as_view(), name='checkout'),
    path('cart/', ProductsCartListView.as_view(), name='cart'),





    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),  # vlastní view pro login
    path('accounts/signup/', SignUpView.as_view(), name='signup'),          # vlastní view pro signup
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'), # view pro změnu hesla
    path('accounts/', include('django.contrib.auth.urls')), # default django view

    path('admin/', admin.site.urls),
]
