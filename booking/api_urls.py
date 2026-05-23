from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import HallViewSet, MenuItemViewSet, ReservationViewSet, RestaurantTableViewSet, WorkingHoursViewSet

router = DefaultRouter()
router.register('menu', MenuItemViewSet)
router.register('schedule', WorkingHoursViewSet)
router.register('halls', HallViewSet)
router.register('tables', RestaurantTableViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
