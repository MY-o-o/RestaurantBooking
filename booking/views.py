from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .forms import RegistrationForm
from .models import Hall, MenuItem, RestaurantTable, WorkingHours


def home(request):
    return render(request, 'booking/home.html')


def menu_page(request):
    items = MenuItem.objects.filter(is_available=True)
    schedule = WorkingHours.objects.all()
    return render(request, 'booking/menu.html', {'items': items, 'schedule': schedule})


def booking_page(request):
    tables = RestaurantTable.objects.select_related('hall').filter(is_active=True)
    halls = Hall.objects.all()
    return render(request, 'booking/booking.html', {'tables': tables, 'halls': halls})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Account created successfully.'))
            return redirect('booking')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Create your views here.
