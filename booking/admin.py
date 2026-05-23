from django.contrib import admin

from .models import Hall, MenuItem, Reservation, RestaurantTable, WorkingHours


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('day', 'open_time', 'close_time', 'is_closed')


class RestaurantTableInline(admin.TabularInline):
    model = RestaurantTable
    extra = 1


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone')
    search_fields = ('name', 'zone')
    inlines = [RestaurantTableInline]


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('number', 'hall', 'seats', 'x', 'y', 'is_active')
    list_filter = ('hall', 'is_active')
    search_fields = ('number', 'hall__name')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'date', 'time', 'guests', 'phone', 'user')
    list_filter = ('date', 'table__hall')
    search_fields = ('customer_name', 'phone', 'user__username')

# Register your models here.
