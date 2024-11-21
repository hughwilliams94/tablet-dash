import requests
import os
import random

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timezone
from collections import namedtuple


class dashStop():
    def __init__(self, lineId, stationId, direction, colour):
        self.lineId = lineId
        self.direction = direction
        self.stationId = stationId
        self.colour = colour



def find_next_trains(data, count=2):
    current_time = datetime.now(timezone.utc)
    sorted_arrivals = sorted(data, key=lambda item: abs(current_time - datetime.fromisoformat(item['expectedArrival'])))
    return sorted_arrivals[:count]


def get_upcoming_trains(dashStop: dashStop):
    api_url = f"https://api.tfl.gov.uk/Line/{dashStop.lineId}/Arrivals/{dashStop.stationId}"

    parameters = {
        'direction': dashStop.direction
    }
    try:
        response = requests.get(api_url, params=parameters)

        if response.status_code == 200:
            arrivals = response.json()  # Assuming the response is in JSON format
            nearest_trains = find_next_trains(arrivals)  # Call the new function
            for train in nearest_trains:
                train['expectedArrivalTime'] = datetime.fromisoformat(train['expectedArrival']).strftime("%H:%M")
                train['shortDestination'] = train['destinationName'].split('(', 1)[0]
                train['colour'] = dashStop.colour
            data = nearest_trains  # Return the list of nearest trains
        else:
            data = []
    except requests.exceptions.RequestException as e:
        # For handling any kind of request exceptions
        print(f"An error occurred while calling the API: {e}")
        data = []  # Empty list in case of errors

    return data
    

# Create your views here.
def home(request):
    stop_dict = {
        "actonCentralRichmond": dashStop("london-overground", "910GACTNCTL", "inbound", "#EE7C0E"),
        "actonCentralStratford": dashStop("london-overground", "910GACTNCTL", "outbound", "#EE7C0E"),
        "actonMainLine": dashStop("elizabeth", "910GACTONML", "inbound", "#6950a1")
    }
    
    # External API URL we want to call

    dashStopData = []
    for value in stop_dict.values():
        dashStopData.append(get_upcoming_trains(value))

    # Pass the API data to the template
    return render(request, 'core/home.html', {'trains': dashStopData})

def get_random_image(request):
    image_paths = []

    for filename in os.listdir(settings.MEDIA_ROOT):
        image_paths.append(os.path.join(settings.MEDIA_URL, filename))

    image_url = random.choice(image_paths)

    return JsonResponse({'image_url': image_url})
