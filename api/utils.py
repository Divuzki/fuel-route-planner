import csv

def read_fuel_prices(file_path):
    fuel_prices = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            fuel_prices.append({
                'id': int(row['OPIS Truckstop ID']),
                'name': row['Truckstop Name'],
                'address': row['Address'],
                'city': row['City'],
                'state': row['State'],
                'rack_id': int(row['Rack ID']),
                'price': float(row['Retail Price'])
            })
    return fuel_prices

def calculate_fuel_stops(route, fuel_prices, max_range=500, mpg=10):
    stops = []
    total_cost = 0
    remaining_range = max_range

    for leg in route['features'][0]['properties']['segments'][0]['steps']:
        leg_distance = leg['distance'] / 1609.34  # Convert meters to miles
        if leg_distance > remaining_range:
            # Need to refuel
            nearest_stop = min(fuel_prices, key=lambda x: x['price'])
            stops.append(nearest_stop)
            total_cost += (max_range / mpg) * nearest_stop['price']
            remaining_range = max_range - leg_distance
        else:
            remaining_range -= leg_distance

    return stops, total_cost

