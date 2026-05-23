from rest_framework import serializers

from .models import Hall, MenuItem, Reservation, RestaurantTable, WorkingHours


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = '__all__'


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class RestaurantTableSerializer(serializers.ModelSerializer):
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    zone = serializers.CharField(source='hall.zone', read_only=True)

    class Meta:
        model = RestaurantTable
        fields = ['id', 'hall', 'hall_name', 'zone', 'number', 'seats', 'x', 'y', 'is_active']


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    table_number = serializers.IntegerField(source='table.number', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'table_number', 'date', 'time', 'guests', 'customer_name', 'phone', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        table = attrs.get('table')
        date = attrs.get('date')
        time = attrs.get('time')
        guests = attrs.get('guests')

        if table and guests and guests > table.seats:
            raise serializers.ValidationError('This table does not have enough seats.')
        if table and date and time and Reservation.objects.filter(table=table, date=date, time=time).exists():
            raise serializers.ValidationError('This table is already reserved for the selected date and time.')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
