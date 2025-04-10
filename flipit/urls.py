"""
URL configuration for flipit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from home import class_views
from home import views_estadisticas
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),  
    path('login/', views.user_login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('process_registration/', views.process_registration, name='process_registration'),
    path('agregar_al_carrito/<int:prenda_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('limpiar-carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    path('prendas/', class_views.PrendaListView.as_view(), name='prenda-list'),
    path('prendas/<int:pk>/', class_views.PrendaDetailView.as_view(), name='prenda-detail'),
    path('prendas/nueva/', class_views.PrendaCreateView.as_view(), name='prenda-create'),
    path('prendas/<int:pk>/editar/', class_views.PrendaUpdateView.as_view(), name='prenda-update'),
    path('prendas/<int:pk>/eliminar/', class_views.PrendaDeleteView.as_view(), name='prenda-delete'),
    path('prendas/populares/', class_views.PrendasPopularesView.as_view(), name='prendas-populares'),
    path('prendas/estadisticas/', views_estadisticas.estadisticas_prendas, name='prendas-estadisticas'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)