from Scripts.ExtractData import getLineInfo, getStopsName
from Scripts.Transport import Transport
from shapely.geometry import Point
from shapely.ops import transform
# import time as T
from datetime import datetime, date, time, timedelta
import pyproj
from copy import deepcopy

RUNNING = 10  # 10 km/h

Lines = getLineInfo("../Data/LinesInformation.csv")
StopsName = getStopsName("../Data/gtfs23Sept/stops.txt")

STIB = Transport(Lines, StopsName)


def getStops(filename):
    wgs84 = pyproj.CRS('EPSG:4326')
    be = pyproj.CRS('EPSG:31370')
    project = pyproj.Transformer.from_crs(wgs84, be, always_xy=True).transform

    stops = {}

    with open(filename, "r") as file:
        file.readline()

        for line in file:
            line = line.strip().split(",")
            stopID = line[0]
            wgs84_point = Point((float(line[5]), float(line[4])))  # TODO
            be_point = transform(project, wgs84_point)

            stops[stopID] = be_point

    return stops


StopsInformation = getStops("../Data/gtfs23Sept/stops.txt")


def getLinesForStopID(stopID):
    lines = [line for line, stops in STIB.lines.items() if stopID in [stop[0] for stop in stops]]

    return lines


def getStopsByRadius(position, distance):
    stops = []

    for stop, point in StopsInformation.items():
        d = point.distance(position)
        if d <= distance:
            stops.append((stop, d))
    return stops


def getStopsByRunning(position, t, limit):
    time_left = limit - t
    distance = RUNNING * time_left.total_seconds()/3600
    stops = {}

    for stop, d in getStopsByRadius(position, distance*1000):
        h = timedelta(d / 1000 / RUNNING)
        new_time = t + h

        stops[stop] = new_time

    return stops


def getStopsByTransport(stopID, t, limit):
    stops = {}
    lines = getLinesForStopID(stopID)

    for line in lines:
        destination = STIB.getNextStop(line, stopID)

        if destination is not None:
            # arrival_time = STIB.getArrivalTime(line, t, stopID, destination)
            arrival_time = t + timedelta(0, 1, 0)  # TODO WIP
            if arrival_time <= limit:
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


def main():
    # position = Point(146975.7, 163304.6)
    position = Point(146991.7, 163406.6)

    t = datetime.now()
    time_interval = timedelta(0, 1.5, 0)
    limit = t + time_interval

    stops = getStopsByRunning(position, t, limit)

    modified = set(stop for stop, _ in stops.items())

    while len(modified) > 0:
        last_stops = deepcopy(stops)
        new_modified = set()
        for stop, t in last_stops.items():
            if stop in modified:
                position = StopsInformation[stop]  # position of stopID
                stopsRunning = getStopsByRunning(position, t, limit)
                stopsTransport = getStopsByTransport(stop, t, limit)
                print("stopsRunning", stopsRunning)
                print("stopsTransport", stopsTransport)

                mergeStops(stopsRunning, stopsTransport)
                mergeStops(stops, stopsRunning, new_modified)

        modified = new_modified

    print("len(stops)", len(stops), "stops", stops)

if __name__ == '__main__':
    main()
