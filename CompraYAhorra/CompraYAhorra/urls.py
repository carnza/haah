from django.contrib import admin
from django.urls import path
from ecommerceET import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('aliexpress/', views.aliexpress_view, name='aliexpress'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('direccion_envio/', views.direccion_envio, name='direccion_envio'),
    path("iniciar-pago/", views.iniciar_pago, name="iniciar_pago"),
    path("pago-exitoso/", views.pago_exitoso, name="pago_exitoso"),
    path("pago-fallido/", views.pago_fallido, name="pago_fallido"),
]
