import webbrowser

from Scripts.ExtractData import getLineInfo, getStopsName, getFullSpeed
from Scripts.Transport import Transport
from datetime import datetime, timedelta
from copy import deepcopy
from haversine import haversine, Unit
import folium
import folium.plugins

RUNNING = 5  # 5 km/h

Lines = getLineInfo("../Data/LinesInformation.csv")
StopsName = getStopsName("../Data/gtfs23Sept/stops.txt")
Speed = getFullSpeed("../Data/CSV/SpeedAnalyzeDayHour.csv")
STIB = Transport(Lines, StopsName, speed=Speed)


def getStops(filename):
    stops = {}

    with open(filename, "r") as file:
        file.readline()

        for line in file:
            line = line.strip().split(",")
            stopID = line[0]
            lat, lon = (float(line[4]), float(line[5]))
            stops[stopID] = (lat, lon)

    return stops


StopsInformation = getStops("../Data/gtfs23Sept/stops.txt")


def getLinesForStopID(stopID):
    lines = [line for line, stops in STIB.lines.items() if stopID in [stop[0] for stop in stops]]

    return lines


def getStopsByRadius(position, distance):
    stops = []

    for stop, point in StopsInformation.items():
        d = haversine(point, position, Unit.KILOMETERS)
        if d <= distance:
            stops.append((stop, d))

    return stops


def getStopsByRunning(position, t, limit):
    time_left = limit - t
    distance = RUNNING * time_left.total_seconds()/3600

    stops = {}

    for stop, d in getStopsByRadius(position, distance):
        h = timedelta(hours=d / RUNNING)
        new_time = t + h

        stops[stop] = new_time

    return stops


def getStopsByTransport(stopID, t, limit):
    stops = {}
    lines = getLinesForStopID(stopID)

    for line in lines:
        destination = STIB.getNextStop(line, stopID)
        if destination is not None:
            arrival_time = STIB.getArrivalTime(line, t, stopID, destination)
            if arrival_time is not None and arrival_time <= limit:
                stops[destination] = arrival_time

    return stops


def mergeStops(dict_1, dict_2, modify=None):
    for stop, t in dict_2.items():
        if stop not in dict_1:
            dict_1[stop] = t
            if modify is not None:
                modify.add(stop)
        else:
            if dict_1[stop] > t:
                dict_1[stop] = t
                if modify is not None:
                    modify.add(stop)


def generateCircle(stops, limit):
    circles = []

    for stop, t in stops.items():
        if stop in StopsInformation:
            time_left = limit - t
            distance = RUNNING * time_left.total_seconds() / 3600
            circles.append((StopsInformation[stop], distance))

    return circles


def showOnMap(circles, stops):
    brussels_map = folium.Map((50.813154, 4.382225), zoom_start=12)

    fg = folium.FeatureGroup()

    for position, distance in circles:
        folium.vector_layers.Circle(
            location=position,
            tooltip=None,
            radius=distance * 1000,
            color='grey',
            opacity=0,
            fill=True,
            fill_color='black',
            fill_opacity=1
        ).add_to(fg)

    brussels_map.add_child(fg)

    for stop in stops:
        if stop in StopsInformation:
            folium.Marker(location=StopsInformation[stop],
                          popup=STIB.getStationName(stop).strip("\""), icon=folium.Icon(color="blue")).add_to(brussels_map)

    folium.Marker(location=circles[-1][0],
                  popup="Start position", icon=folium.Icon(color="red")).add_to(brussels_map)

    brussels_map.save('map.html')
    with open("map.html", "a") as f:
        f.write('\n<script>var list = document.getElementsByClassName("leaflet-zoom-animated");var i = 0;for (i = 0; i < list.length; i++) {if (list[i].classList.length === 1) {break;}}list[i].style.opacity = "0.5";</script>\n')
    webbrowser.open('map.html')


def main():

    start_position = (50.813154, 4.382225)

    t = datetime.now()
    time_interval = timedelta(minutes=15)
    limit = t + time_interval

    stops = getStopsByRunning(start_position, t, limit)

    modified = set(stop for stop, _ in stops.items())

    while len(modified) > 0:
        last_stops = deepcopy(stops)
        new_modified = set()
        for stop, t in last_stops.items():
            if stop in modified and stop in StopsInformation:
                position = StopsInformation[stop]  # position of stopID
                stopsRunning = getStopsByRunning(position, t, limit)
                stopsTransport = getStopsByTransport(stop, t, limit)

                mergeStops(stopsRunning, stopsTransport)
                mergeStops(stops, stopsRunning, new_modified)

        modified = new_modified

    circles = generateCircle(stops, limit)
    circles.append((start_position, RUNNING * (limit - t).total_seconds() / 3600))

    showOnMap(circles, stops)


if __name__ == '__main__':
    main()
