from django.urls import path
from django.contrib import admin
from menu.views import (
    HomeView,
    AboutView,
    ContactView,
    ServicesView,
    ProductsView,
    product_detail,
    CategoryView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Основные страницы
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/', ServicesView.as_view(), name='services'),
    path('products/', ProductsView.as_view(), name='products'),

    # Динамические URL
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),

    # Дополнительные страницы для теста вложенности
    path('company/history/', AboutView.as_view(), name='history'),
    path('company/team/', AboutView.as_view(), name='team'),
    path('services/development/', ServicesView.as_view(), name='development'),
    path('services/design/', ServicesView.as_view(), name='design'),
]
