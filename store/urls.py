from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_Item/',views.updateItem,name='updateItem'),
    path('process_order/', views.processOrder,name="process_order"),
    path('loginPage/', views.loginPage,name="loginPage"),
    path('register/', views.register,name="register"),
    path('logoutUser/', views.logoutUser,name="logoutUser"),
]
