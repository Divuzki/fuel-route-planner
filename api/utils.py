import csv


def read_fuel_prices(file_path):
    fuel_prices = []
    with open(file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            fuel_prices.append(row)
    return fuel_prices

def calculate_fuel_stops(route_data, fuel_prices):
    fuel_stops = []
    for step in route_data['steps']:
        for fuel_price in fuel_prices:
            if fuel_price['fuel_type'] == step['fuel_type']:
                fuel_stops.append({
                    'location': step['location'],
                    'price': fuel_price['price'],
                })
    return fuel_stops