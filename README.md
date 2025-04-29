# Tourism Guide

A comprehensive tourism management system that allows users to explore destinations, book tours, and manage their travel experiences.

## Features

- User authentication and profile management
- Destination exploration with maps and weather information
- Tour package booking system
- Wishlist functionality
- Admin dashboard for content management
- Real-time weather updates
- Interactive maps
- Photo galleries and attraction management

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tourism-guide
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
```

2. Configure media and static files:
```bash
python manage.py collectstatic
```

## Admin Guide

### Accessing the Admin Panel
1. Visit `http://localhost:8000/admin/`
2. Log in with your superuser credentials

### Managing Destinations
1. Click on "Destinations" in the admin panel
2. Add a new destination with:
   - Name and description
   - Country and climate
   - Latitude and longitude (for maps and weather)
   - Upload destination image
   - Add additional information (best time to visit, activities, etc.)

### Managing Tour Packages
1. Click on "Tour Packages" in the admin panel
2. Create new packages with:
   - Package name and description
   - Select destination
   - Set price and duration
   - Add package image
   - Configure availability and capacity

### Managing Content
1. Add destination images:
   - Go to destination detail
   - Click "Manage Content"
   - Upload images with captions
   - Mark featured images

2. Add attractions:
   - Go to destination detail
   - Click "Manage Content"
   - Add attraction details
   - Upload attraction images
   - Set opening hours and ticket prices

## User Guide

### Registration and Login
1. Visit the registration page
2. Fill in your details:
   - Email address
   - Password
   - Personal information
3. Verify your email (if enabled)
4. Log in with your credentials

### Exploring Destinations
1. Browse destinations on the home page
2. Use filters to find specific destinations
3. View destination details:
   - See location on map
   - Check current weather
   - View photo gallery
   - Explore attractions

### Managing Wishlist
1. Log in to your account
2. Visit any destination
3. Click "Add to Wishlist" to save
4. View your wishlist in your profile

### Booking Tours
1. Select a destination
2. Browse available tour packages
3. Click "View Details" on a package
4. Select dates and number of people
5. Complete the booking process
6. View your bookings in your profile

### Profile Management
1. Access your profile from the navigation menu
2. Update personal information
3. View booking history
4. Manage wishlist
5. Update profile picture

## Development

### Project Structure
```
tourism_guide/
├── destinations/         # Destination management
├── packages/            # Tour package management
├── bookings/           # Booking system
├── users/              # User authentication and profiles
├── static/             # Static files
└── templates/          # HTML templates
```

### Adding New Features
1. Create a new app for the feature:
```bash
python manage.py startapp new_feature
```

2. Add the app to `INSTALLED_APPS` in settings.py
3. Create models, views, and templates
4. Add URLs and forms as needed

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please open an issue in the repository or contact the development team.

## Acknowledgments
- OpenStreetMap for map data
- Open-Meteo for weather data
- Font Awesome for icons
- Django framework 