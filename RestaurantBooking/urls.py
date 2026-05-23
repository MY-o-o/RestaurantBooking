"""
URL configuration for RestaurantBooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from booking import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('booking/', views.booking_page, name='booking'),
    path('register/', views.register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('booking.api_urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('admin/', admin.site.urls),
]
