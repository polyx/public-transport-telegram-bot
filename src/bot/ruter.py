import arrow
import requests

import location


def get_nearby_stops(coordinates):
    x = coordinates['latitude']
    y = coordinates['longitude']
    x, y = location.get_utm_location(x, y)
    url = "http://reisapi.ruter.no/Place/GetClosestPlacesExtension"
    querystring = {
        "coordinates": f"(x={x},y={y})",
        "proposals": 5,
        "maxdistance": 800
    }

    response = requests.request("GET", url, params=querystring)
    nearby = "Nearby Stops:\n"
    stops = dict()
    for stop in response.json()[0]['Stops']:
        nearby += stop['Name']+'\n'
        stops[stop['ID']] = stop['Name']

    return nearby, stops


def get_departures_by_id(stop_id=3012211):
    url = f"http://reisapi.ruter.no/StopVisit/GetDepartures/{stop_id}"
    # querystring = {"transporttypes": "2"}

    response = requests.get(url) # params=querystring

    bus_schedule = ''
    counter = 0;
    for departure in response.json():
        if counter > 10:
            break
        line = departure['MonitoredVehicleJourney']['PublishedLineName']  # Line name
        dest = departure['MonitoredVehicleJourney']['DestinationName']
        scheduled_arrival = departure['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']  # scheduled
        expected_arrival = departure['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']  # real arrival

        # occupancy_percentage = departure['Extensions']['OccupancyData']['OccupancyPercentage']

        bus_schedule += f'Line: {line}, ->{dest}\n'
        bus_schedule += f'Arrives in: {arrow.get(scheduled_arrival).humanize()}\n'
        bus_schedule += f'Maybe in: {arrow.get(expected_arrival).humanize()}\n'
        bus_schedule += '\n==========\n\n'
        counter += 1
    return bus_schedule


if __name__ == '__main__':
    # print(get_departures_by_id())
    get_nearby_stops()