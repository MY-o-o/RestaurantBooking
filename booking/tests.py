from datetime import date, time

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Hall, MenuItem, Reservation, RestaurantTable
from .schema import schema


class BookingProjectTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='demo', password='pass12345')
        self.hall = Hall.objects.create(name='VIP Room', zone='VIP')
        self.table = RestaurantTable.objects.create(hall=self.hall, number=1, seats=4, x=1, y=1)
        self.busy_table = RestaurantTable.objects.create(hall=self.hall, number=2, seats=4, x=2, y=1)
        MenuItem.objects.create(
            name='Margherita Pizza',
            description='Tomato, mozzarella and basil.',
            price=310,
            category='main',
        )
        Reservation.objects.create(
            user=self.user,
            table=self.busy_table,
            date=date(2026, 5, 25),
            time=time(18, 0),
            guests=2,
            customer_name='Demo',
            phone='+380000000000',
        )

    def test_public_pages_render(self):
        for url in ['/', '/menu/', '/booking/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_rest_menu_is_public(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'Margherita Pizza')

    def test_reservation_requires_authentication(self):
        response = self.client.post('/api/reservations/', {})
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_create_reservation(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/api/reservations/', {
            'table': self.table.id,
            'date': '2026-05-25',
            'time': '18:00',
            'guests': 2,
            'customer_name': 'Demo',
            'phone': '+380000000000',
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_graphql_available_tables_filters_reserved_tables(self):
        result = schema.execute(
            '''
            query {
              availableTables(date: "2026-05-25", time: "18:00", guests: 4, zone: "VIP") {
                id
                number
              }
            }
            '''
        )
        self.assertIsNone(result.errors)
        table_numbers = [row['number'] for row in result.data['availableTables']]
        self.assertEqual(table_numbers, [1])

# Create your tests here.
