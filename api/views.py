import os
import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import read_fuel_prices, calculate_fuel_stops


class RouteView(APIView):
    def get(self, request):
        start_address = request.query_params.get("start")
        finish_address = request.query_params.get("finish")

        cache_key = f"route_{start_address}_{finish_address}"
        cached_route = cache.get(cache_key)

        if cached_route:
            return Response(cached_route)

        # Geocode addresses to get coordinates
        geocode_url = "https://api.openrouteservice.org/geocode/search"
        headers = {"Authorization": os.getenv("OPENROUTESERVICE_API_KEY")}

        start_coords_response = requests.get(
            geocode_url, headers=headers, params={"text": start_address, "size": 1}
        )
        finish_coords_response = requests.get(
            geocode_url, headers=headers, params={"text": finish_address, "size": 1}
        )

        if (
            start_coords_response.status_code != 200
            or finish_coords_response.status_code != 200
        ):
            return Response(
                {"error": "Error geocoding addresses"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_coords = start_coords_response.json()["features"][0]["geometry"][
            "coordinates"
        ]
        finish_coords = finish_coords_response.json()["features"][0]["geometry"][
            "coordinates"
        ]

        # Fetch route from OpenRouteService
        route_url = "https://api.openrouteservice.org/v2/directions/driving-car"
        route_params = {
            "start": f"{start_coords[0]},{start_coords[1]}",
            "end": f"{finish_coords[0]},{finish_coords[1]}",
        }

        route_response = requests.get(route_url, headers=headers, params=route_params)

        if route_response.status_code != 200:
            return Response(
                {"error": "Error fetching route"}, status=status.HTTP_400_BAD_REQUEST
            )

        route_data = route_response.json()
        fuel_prices = read_fuel_prices("fuel_prices.csv")

        # Calculate fuel stops and total cost
        fuel_stops, total_cost = calculate_fuel_stops(route_data, fuel_prices)

        response_data = {
            "route": route_data,
            "fuel_stops": fuel_stops,
            "total_cost": total_cost,
        }

        cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour

        return Response(response_data)
