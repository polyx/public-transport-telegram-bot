import arrow
import requests

import location

BASE_API_URL = "http://reisapi.ruter.no/"


def get_nearby_stops(coordinates):
    x = coordinates['latitude']
    y = coordinates['longitude']

    x, y = location.get_utm_location(x, y)
    url = f"{BASE_API_URL}/Place/GetClosestStops"

    querystring = {
        "coordinates": f"(x={x},y={y})",
        "proposals": 5,
        "maxdistance": 500
    }

    response = requests.request("GET", url, params=querystring)

    nearby = "Nearby Stops:\n"
    stops = dict()

    for stop in response.json():
        nearby += stop['Name']+'\n'
        stops[stop['ID']] = stop['Name']

    return nearby, stops


def get_departures_by_id(stop_id=3012211):
    url = f"{BASE_API_URL}/StopVisit/GetDepartures/{stop_id}"

    response = requests.get(url)

    bus_schedule = ''
    counter = 0
    for departure in response.json():
        if counter > 6:  # limit number of departures shown to the user so that it fits on screen hopefuly.
            break
        line = departure['MonitoredVehicleJourney']['PublishedLineName']  # Line name
        dest = departure['MonitoredVehicleJourney']['DestinationName']

        scheduled_arrival = departure['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']  # scheduled
        expected_arrival = departure['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']  # real arrival

        bus_schedule += f'Line: {line}->{dest}\n'
        bus_schedule += f'Arrives in: {arrow.get(scheduled_arrival).humanize()}\n'
        bus_schedule += f'Maybe in: {arrow.get(expected_arrival).humanize()}\n'
        bus_schedule += '==========\n'
        counter += 1
    return bus_schedule
