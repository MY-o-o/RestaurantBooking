from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', _('Starters')),
        ('main', _('Main dishes')),
        ('dessert', _('Desserts')),
        ('drink', _('Drinks')),
    ]

    name = models.CharField(_('name'), max_length=120)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=7, decimal_places=2)
    category = models.CharField(_('category'), max_length=30, choices=CATEGORY_CHOICES)
    image_url = models.URLField(_('image URL'), blank=True)
    is_available = models.BooleanField(_('is available'), default=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    day = models.CharField(_('day'), max_length=20)
    open_time = models.TimeField(_('open time'))
    close_time = models.TimeField(_('close time'))
    is_closed = models.BooleanField(_('is closed'), default=False)

    class Meta:
        verbose_name = _('working hours')
        verbose_name_plural = _('working hours')
        ordering = ['id']

    def __str__(self):
        if self.is_closed:
            return f'{self.day}: {_("closed")}'
        return f'{self.day}: {self.open_time:%H:%M}-{self.close_time:%H:%M}'


class Hall(models.Model):
    name = models.CharField(_('name'), max_length=100)
    zone = models.CharField(_('zone'), max_length=80)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('hall')
        verbose_name_plural = _('halls')

    def __str__(self):
        return f'{self.name} ({self.zone})'


class RestaurantTable(models.Model):
    hall = models.ForeignKey(Hall, verbose_name=_('hall'), on_delete=models.CASCADE, related_name='tables')
    number = models.PositiveIntegerField(_('number'))
    seats = models.PositiveIntegerField(_('seats'))
    x = models.PositiveIntegerField(default=1)
    y = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        ordering = ['hall__name', 'number']
        unique_together = ['hall', 'number']
        verbose_name = _('restaurant table')
        verbose_name_plural = _('restaurant tables')

    def __str__(self):
        return _('Table %(number)s - %(hall)s') % {'number': self.number, 'hall': self.hall.name}


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(RestaurantTable, verbose_name=_('table'), on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField(_('date'))
    time = models.TimeField(_('time'))
    guests = models.PositiveIntegerField(_('guests'))
    customer_name = models.CharField(_('customer name'), max_length=120)
    phone = models.CharField(_('phone'), max_length=30)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']
        unique_together = ['table', 'date', 'time']
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')

    def __str__(self):
        return _('%(name)s: table %(table)s on %(date)s %(time)s') % {
            'name': self.customer_name,
            'table': self.table.number,
            'date': self.date,
            'time': f'{self.time:%H:%M}',
        }
