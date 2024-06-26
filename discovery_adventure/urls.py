
from django.contrib import admin
from django.urls import path, include
from discovery_adventure import settings

from viewer import views
from accounts.views import SubmittableLoginView, SignUpView, SubmittablePasswordChangeView

from viewer.views import home, ProductsListView, ProductTemplateView, ProductCreateView, CategoryListView, \
    CategoryTemplateView

urlpatterns = [

    path('hello/', views.hello, name='hello'),

    path('', CategoryListView.as_view(), name='home'), # "domovská stránka", která zobrazuje kategorie

    # path('index/', CategoryListView.as_view(), name='index'), # "domovská stránka", která zobrazuje kategorie
    path('shop/', ProductsListView.as_view(), name='shop'), # zobrazení všech produktů
    path('category/<pk>/', CategoryTemplateView.as_view(), name='category'), # zobrazení produktů dané kategorie
    path('product/<pk>', ProductTemplateView.as_view(), name='product'), # zobrazení detailu produktu
    path('product/create/', ProductCreateView.as_view(), name='product_create'), # vytvoření produktu

    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),  # vlastní view pro login
    path('accounts/signup/', SignUpView.as_view(), name='signup'),          # vlastní view pro signup
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'), # view pro změnu hesla
    path('accounts/', include('django.contrib.auth.urls')), # default django view

    path('admin/', admin.site.urls),
]
