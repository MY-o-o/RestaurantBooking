import graphene
from graphene_django import DjangoObjectType

from .models import Hall, Reservation, RestaurantTable


class HallType(DjangoObjectType):
    class Meta:
        model = Hall
        fields = ('id', 'name', 'zone', 'description')


class RestaurantTableType(DjangoObjectType):
    class Meta:
        model = RestaurantTable
        fields = ('id', 'hall', 'number', 'seats', 'x', 'y', 'is_active')


class Query(graphene.ObjectType):
    available_tables = graphene.List(
        RestaurantTableType,
        date=graphene.Date(required=True),
        time=graphene.Time(required=True),
        guests=graphene.Int(required=True),
        zone=graphene.String(),
    )
    halls = graphene.List(HallType)

    def resolve_halls(self, info):
        return Hall.objects.all()

    def resolve_available_tables(self, info, date, time, guests, zone=None):
        reserved_ids = Reservation.objects.filter(date=date, time=time).values_list('table_id', flat=True)
        tables = RestaurantTable.objects.select_related('hall').filter(
            is_active=True,
            seats__gte=guests,
        ).exclude(id__in=reserved_ids)
        if zone:
            tables = tables.filter(hall__zone__icontains=zone)
        return tables


schema = graphene.Schema(query=Query)
