from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from destinations.models import Destination, DestinationImage, Attraction
from packages.models import Package, TravelStyle
from users.models import Profile, UserPreferences
from feedback.models import Feedback
from bookings.models import Booking
import random
from datetime import datetime, timedelta
from django.utils.text import slugify
import os
from django.core.files import File
from urllib.request import urlretrieve
import tempfile

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate data...')

        # Create sample users
        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password123',
                first_name=f'User{i}',
                last_name='Test'
            )
            profile = Profile.objects.create(
                user=user,
                phone=f'+123456789{i}',
                location=f'City {i}',
                bio=f'This is a sample bio for user {i}'
            )
            users.append(user)

        # Create travel styles
        travel_styles = [
            'Adventure', 'Luxury', 'Budget', 'Family', 'Solo',
            'Romantic', 'Cultural', 'Beach', 'Mountain', 'City'
        ]
        style_objects = []
        for style in travel_styles:
            style_obj = TravelStyle.objects.create(name=style)
            style_objects.append(style_obj)

        # Sample destinations data
        destinations_data = [
            {
                'name': 'Bali, Indonesia',
                'country': 'Indonesia',
                'climate': 'Tropical',
                'description': 'Bali is a province of Indonesia and the westernmost of the Lesser Sunda Islands. East of Java and west of Lombok, the province includes the island of Bali and a few smaller neighboring islands.',
                'rating': 4.8,
                'review_count': 1200,
                'images': [
                    'https://images.unsplash.com/photo-1537996194471-e657df975ab4',
                    'https://images.unsplash.com/photo-1537996194471-e657df975ab4',
                    'https://images.unsplash.com/photo-1537996194471-e657df975ab4'
                ],
                'attractions': [
                    {'name': 'Uluwatu Temple', 'description': 'Ancient sea temple on a cliff'},
                    {'name': 'Tegallalang Rice Terrace', 'description': 'Beautiful rice fields'},
                    {'name': 'Mount Batur', 'description': 'Active volcano with sunrise views'}
                ]
            },
            {
                'name': 'Paris, France',
                'country': 'France',
                'climate': 'Temperate',
                'description': 'Paris, France\'s capital, is a major European city and a global center for art, fashion, gastronomy and culture. Its 19th-century cityscape is crisscrossed by wide boulevards and the River Seine.',
                'rating': 4.7,
                'review_count': 1500,
                'images': [
                    'https://images.unsplash.com/photo-1502602898657-3e91760cbb34',
                    'https://images.unsplash.com/photo-1502602898657-3e91760cbb34',
                    'https://images.unsplash.com/photo-1502602898657-3e91760cbb34'
                ],
                'attractions': [
                    {'name': 'Eiffel Tower', 'description': 'Iconic iron tower'},
                    {'name': 'Louvre Museum', 'description': 'World\'s largest art museum'},
                    {'name': 'Notre-Dame Cathedral', 'description': 'Medieval Catholic cathedral'}
                ]
            },
            {
                'name': 'Tokyo, Japan',
                'country': 'Japan',
                'climate': 'Temperate',
                'description': 'Tokyo, Japan\'s busy capital, mixes the ultramodern and the traditional, from neon-lit skyscrapers to historic temples. The opulent Meiji Shinto Shrine is known for its towering gate and surrounding woods.',
                'rating': 4.6,
                'review_count': 1100,
                'images': [
                    'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf',
                    'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf',
                    'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf'
                ],
                'attractions': [
                    {'name': 'Shibuya Crossing', 'description': 'World\'s busiest pedestrian crossing'},
                    {'name': 'Senso-ji Temple', 'description': 'Ancient Buddhist temple'},
                    {'name': 'Tokyo Skytree', 'description': 'Tallest structure in Japan'}
                ]
            }
        ]

        # Create destinations
        for dest_data in destinations_data:
            destination = Destination.objects.create(
                name=dest_data['name'],
                slug=slugify(dest_data['name']),
                country=dest_data['country'],
                climate=dest_data['climate'],
                description=dest_data['description'],
                rating=dest_data['rating'],
                review_count=dest_data['review_count']
            )

            # Add images
            for img_url in dest_data['images']:
                with tempfile.NamedTemporaryFile(delete=True) as tmp:
                    urlretrieve(img_url, tmp.name)
                    destination_image = DestinationImage.objects.create(
                        destination=destination,
                        image=File(open(tmp.name, 'rb'))
                    )

            # Add attractions
            for attr_data in dest_data['attractions']:
                with tempfile.NamedTemporaryFile(delete=True) as tmp:
                    urlretrieve(img_url, tmp.name)
                    Attraction.objects.create(
                        destination=destination,
                        name=attr_data['name'],
                        description=attr_data['description'],
                        image=File(open(tmp.name, 'rb'))
                    )

            # Create packages for each destination
            for i in range(1, 4):
                package = Package.objects.create(
                    name=f'{destination.name} Package {i}',
                    slug=slugify(f'{destination.name}-package-{i}'),
                    destination=destination,
                    description=f'Experience the best of {destination.name} with this amazing package.',
                    price=random.randint(500, 2000),
                    duration=random.randint(3, 10),
                    is_available=True
                )
                package.travel_styles.set(random.sample(style_objects, random.randint(1, 3)))

                # Create bookings
                for user in users:
                    if random.random() > 0.7:  # 30% chance of booking
                        check_in = datetime.now() + timedelta(days=random.randint(30, 180))
                        Booking.objects.create(
                            user=user,
                            package=package,
                            check_in_date=check_in,
                            check_out_date=check_in + timedelta(days=package.duration),
                            status=random.choice(['confirmed', 'pending', 'cancelled']),
                            total_price=package.price
                        )

                # Create feedback
                for user in users:
                    if random.random() > 0.7:  # 30% chance of feedback
                        Feedback.objects.create(
                            user=user,
                            package=package,
                            rating=random.randint(3, 5),
                            content=f'Amazing experience in {destination.name}! The package was well organized and the activities were fantastic.'
                        )

        # Create user preferences
        for user in users:
            preferences = UserPreferences.objects.create(user=user)
            preferences.destinations.set(random.sample(list(Destination.objects.all()), random.randint(1, 3)))
            preferences.travel_styles.set(random.sample(style_objects, random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS('Successfully populated data!')) 