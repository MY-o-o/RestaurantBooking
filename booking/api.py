from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import permissions, viewsets

from .models import Hall, MenuItem, Reservation, RestaurantTable, WorkingHours
from .serializers import (
    HallSerializer,
    MenuItemSerializer,
    ReservationSerializer,
    RestaurantTableSerializer,
    WorkingHoursSerializer,
)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class WorkingHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class RestaurantTableViewSet(viewsets.ModelViewSet):
    queryset = RestaurantTable.objects.select_related('hall')
    serializer_class = RestaurantTableSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('table', 'table__hall', 'user')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reservation = serializer.save(user=self.request.user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'tables',
            {
                'type': 'table_status',
                'table_id': reservation.table_id,
                'status': 'busy',
                'date': reservation.date.isoformat(),
                'time': reservation.time.strftime('%H:%M'),
            },
        )
