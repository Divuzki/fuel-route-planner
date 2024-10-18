import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import read_fuel_prices


class RouteView(APIView):
    def get(self, request):
        start = request.query_params.get("start")
        finish = request.query_params.get("finish")

        # Fetch route from OpenRouteService
        route_response = requests.get(
            "https://api.openrouteservice.org/v2/directions/driving-car",
            params={
                "start": start,
                "end": finish,
                "api_key": os.getenv("OPENROUTESERVICE_API_KEY"),
            },
        )

        if route_response.status_code != 200:
            return Response(
                {"error": "Error fetching route"}, status=status.HTTP_400_BAD_REQUEST
            )

        route_data = route_response.json()
        fuel_prices = read_fuel_prices("fuel_prices.csv")

        # Calculate fuel stops and total cost based on route_data and fuel_prices
        # This is where your logic will go

        return Response(
            {
                "route": route_data,
                "fuel_stops": [],
                "total_cost": 0,
            }
        )
