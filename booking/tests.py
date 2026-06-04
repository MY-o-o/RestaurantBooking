from datetime import date, time

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from .models import Hall, MenuItem, Reservation, RestaurantTable
from .schema import schema


class BookingProjectTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(
            username='demo',
            email='demo@example.com',
            password='pass12345',
        )
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

    def test_login_page_shows_password_reset_link(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Forgot Password?')
        self.assertContains(response, 'data-password-toggle')

    def test_registration_flow_saves_email_and_logs_user_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'Str0ng-passw0rd!',
            'password2': 'Str0ng-passw0rd!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='newuser', email='new@example.com').exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_request_sends_email(self):
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Reset your Urban Table password', mail.outbox[0].subject)
        self.assertIn('/accounts/reset/', mail.outbox[0].body)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_confirm_updates_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {
            'new_password1': 'An0ther-strong-pass!',
            'new_password2': 'An0ther-strong-pass!',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('An0ther-strong-pass!'))

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_rate_limit_blocks_excess_requests(self):
        url = reverse('password_reset')
        for _ in range(3):
            response = self.client.post(url, {'email': self.user.email})
            self.assertEqual(response.status_code, 302)

        response = self.client.post(url, {'email': self.user.email})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please wait before requesting another reset link.')
        self.assertEqual(len(mail.outbox), 3)

# Create your tests here.
