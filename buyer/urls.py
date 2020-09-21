from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('addItem/<int:item_id>', views.addItemView, name='addItemView'),
    path('removeItem/<int:item_id>', views.removeItemView, name='removeItemView'),
    path('logout/', auth_views.LogoutView.as_view(template_name="login.html"), name='login'),
    path('checkout/', views.checkoutView, name='checkoutView'),
]