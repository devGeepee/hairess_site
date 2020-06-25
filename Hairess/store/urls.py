from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('product_details/<int:id>',views.product_details,name="product"),
    path('hair_bundles_products/<int:id>',views.hair_bundles_products,name="hair_bundles_products"),
    path('category/',views.category,name="category"),
    path('hair_bundles/',views.hair_bundles,name="hair_bundles"),
    ####################################################
    path('identity/register', views.Register, name="register"),
    path('identity/login', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('forgot-password', views.ForgotP, name="forgotpassword"),
    path('change-password/<str:email>', views.NewPassword, name="newpassword"),
    path('api/', views.Apicart, name="api"),
    path('search/', views.search, name="search")
]