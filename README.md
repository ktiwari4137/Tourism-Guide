# Tourism Guide

A comprehensive tourism management system built with Django.

## Features

- User authentication and profile management
- Destination and hotel listings
- Package bookings
- Weather forecasts
- User feedback system
- Real-time chat
- Booking management
- Responsive design with Bootstrap 5

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
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

- `tourism_guide/` - Main project configuration
- `users/` - User authentication and profile management
- `destinations/` - Destination listings and details
- `hotels/` - Hotel listings and details
- `packages/` - Tour package management
- `bookings/` - Booking system
- `feedback/` - User feedback system
- `chat/` - Real-time chat functionality
- `weather/` - Weather forecast integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 