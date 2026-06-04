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
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from booking.auth_views import (
    SecureLoginView,
    SecurePasswordResetConfirmView,
    SecurePasswordResetDoneView,
    SecurePasswordResetView,
)
from booking import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('booking/', views.booking_page, name='booking'),
    path('register/', views.register_view, name='register'),
    path('accounts/login/', SecureLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', SecurePasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', SecurePasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', SecurePasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('api/', include('booking.api_urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('admin/', admin.site.urls),
]
