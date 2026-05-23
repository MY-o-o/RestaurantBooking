from datetime import time

from django.core.management.base import BaseCommand

from booking.models import Hall, MenuItem, RestaurantTable, WorkingHours


class Command(BaseCommand):
    help = 'Create demo restaurant data for the module project.'

    def handle(self, *args, **options):
        menu = [
            (
                'Bruschetta',
                'Tomatoes, basil, olive oil and toasted bread.',
                180,
                'starter',
                'https://images.unsplash.com/photo-1506280754576-f6fa8a873550?auto=format&fit=crop&w=900&q=80',
            ),
            (
                'Caesar Salad',
                'Chicken, romaine, parmesan and house dressing.',
                240,
                'starter',
                'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=900&q=80',
            ),
            (
                'Margherita Pizza',
                'Tomato sauce, mozzarella and fresh basil.',
                310,
                'main',
                'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=80',
            ),
            (
                'Ribeye Steak',
                'Grilled beef steak with seasonal vegetables.',
                620,
                'main',
                'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=900&q=80',
            ),
            (
                'Tiramisu',
                'Coffee dessert with mascarpone cream.',
                190,
                'dessert',
                'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=900&q=80',
            ),
            (
                'Lemonade',
                'House citrus lemonade with mint.',
                95,
                'drink',
                'https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=80',
            ),
        ]
        for name, description, price, category, image_url in menu:
            MenuItem.objects.update_or_create(
                name=name,
                defaults={
                    'description': description,
                    'price': price,
                    'category': category,
                    'image_url': image_url,
                    'is_available': True,
                },
            )

        days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пʼятниця', 'Субота', 'Неділя']
        for day in days:
            WorkingHours.objects.update_or_create(
                day=day,
                defaults={
                    'open_time': time(10, 0),
                    'close_time': time(22, 0),
                    'is_closed': False,
                },
            )

        main_hall, _ = Hall.objects.update_or_create(
            name='Main Hall',
            defaults={'zone': 'Main', 'description': 'Основний зал біля бару.'},
        )
        vip_hall, _ = Hall.objects.update_or_create(
            name='VIP Room',
            defaults={'zone': 'VIP', 'description': 'Тиха зона для невеликих компаній.'},
        )
        terrace, _ = Hall.objects.update_or_create(
            name='Terrace',
            defaults={'zone': 'Terrace', 'description': 'Літня тераса.'},
        )

        table_rows = [
            (main_hall, 1, 2, 1, 1),
            (main_hall, 2, 2, 2, 1),
            (main_hall, 3, 4, 3, 1),
            (main_hall, 4, 4, 1, 2),
            (main_hall, 5, 6, 2, 2),
            (vip_hall, 6, 4, 5, 1),
            (vip_hall, 7, 6, 6, 1),
            (terrace, 8, 2, 4, 3),
            (terrace, 9, 4, 5, 3),
            (terrace, 10, 8, 6, 3),
        ]
        for hall, number, seats, x, y in table_rows:
            RestaurantTable.objects.update_or_create(
                hall=hall,
                number=number,
                defaults={'seats': seats, 'x': x, 'y': y, 'is_active': True},
            )

        self.stdout.write(self.style.SUCCESS('Demo data created.'))
