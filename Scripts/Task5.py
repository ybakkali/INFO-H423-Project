from Scripts.ExtractData import getLineInfo, getStopsName
from Scripts.Transport import Transport

RUNNING = 10  # 10 km/h

Lines = getLineInfo("../Data/LinesInformation.csv")
StopsName = getStopsName("../Data/gtfs23Sept/stops.txt")

STIB = Transport(Lines, StopsName)


def getLinesForStopID(stopID):
    lines = [line for line in STIB.lines if stopID in [s[0] for s in line]]

    return lines


def getStopsByRadius(position, distance):
    stops = []

    return stops


def getStopsByRunning(position, time, limit):
    time_left = limit - time

    distance = RUNNING * time_left

    stops = getStopsByRadius(position, distance)

    # get arrival time

    return stops


def getStopsByTransport(stopID, time, limit):
    stops = []
    lines = getLinesForStopID(stopID)
    for line in lines:
        destination = STIB.getNextStop(line, stopID)
        if destination is not None:
            arrival_time = STIB.getArrivalTime(line, time, stopID, destination)
            if arrival_time <= limit:
                stops.append(destination)

    return stops


def mergeStops(set_1, set_2, modify=None):
    return set_1


def main():
    position = (0, 0)
    time = 0
    limit = 10

    stops = set(getStopsByRunning(position, time, limit))

    modified = set((stop[0]) for stop in stops)

    while len(modified) > 0:
        new_modified = set()
        for stop in stops:
            if stop in modified:
                position = None  # position of stopID
                new_stops = mergeStops(set(getStopsByRunning(position, stop[1], limit)), set(getStopsByTransport(stop[0], stop[1], limit)))

                stops = mergeStops(stops, new_stops, modified)


if __name__ == '__main__':
    main()