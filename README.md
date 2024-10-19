# FuelRoutePlanner

**FuelRoutePlanner** is a Django-based API that calculates the optimal fuel stops along a given route within the USA, based on real-time fuel prices. It provides a detailed route map and calculates the total fuel cost for the journey.

## Features

- **Routing**: Calculates the route between a start and end location using the OpenRouteService API.
- **Fuel Stop Optimization**: Identifies cost-effective fuel stops along the route based on vehicle range and fuel consumption.
- **Total Fuel Cost Calculation**: Computes the total fuel cost for the journey.

## Requirements

- Python 3.8+
- Django 3.2.23
- Django Rest Framework
- requests
- OpenRouteService API key

## Installation

1. **Clone the repository**:

```sh
git clone https://github.com/divuzki/FuelRoutePlanner.git
cd FuelRoutePlanner
```

2. **Create and activate a virtual environment**:

```sh
python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. **Install the dependencies**:

```sh
pip install -r requirements.txt
```

4. **Set up the Django project**:

```sh
python manage.py migrate
```

## Add your [OpenRouteService](https://openrouteservice.org/) API key to .env

# Run the development server:

```sh
python manage.py runserver
```
