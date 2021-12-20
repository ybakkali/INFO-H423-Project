import json

from Scripts.ExtractData import getRawPositions, getStopsName


def getAllVehicles(allPositions, transport):
    allVehicles = {}
    i = 0
    print("0 /", len(allPositions.keys()), "lines done")
    for line in allPositions.keys():

        positions = allPositions[line]

        # Group + sorted by time
        times = groupSortByTime(positions)

        vehicles = [[p] for p in times[0]]
        oldVehicles = []

        for t in times[1:]:

            a = 0
            while a < len(vehicles):
                if t[0][0] - vehicles[a][-1][0] > 2.5 * 60 * 1000:
                    oldVehicles.append(vehicles.pop(a))
                else:
                    a += 1

            t.sort(key=lambda p: transport.getDistanceStop(p[1], line) + p[2])

            while len(t) > 0:

                index = transport.getIndexClosestVehicle(t[0], vehicles, line)

                if index != -1:
                    vehicles[index].append(t.pop(0))

                else:  # Not found
                    vehicles.append([t.pop(0)])

        allVehicles[line] = oldVehicles + vehicles
        i += 1
        print(i, "/", len(allPositions.keys()), "lines done")

    return allVehicles


def groupSortByTime(positions):
    positions.sort(key=lambda x: x[0])
    times = []
    last_time = "-1"
    for position in positions:
        if last_time != position[0]:
            last_time = position[0]
            times.append([])
        times[-1].append(position)

    return times


def analyseStopsID():
    realStops = set()
    posStops = set()

    for stop in getStopsName("../Data/gtfs23Sept/stops.txt").keys():
        realStops.add(stop)

    for i in range(1, 14):
        for position in getRawPositions("../Data/JSON/vehiclePosition{:02d}.json".format(i)):
            posStops.add(position[2])
            posStops.add(position[3])

    n = len(posStops)
    print(n, "different stops")

    posStops = [s for s in posStops if s not in realStops]
    print("Not found : (" + str(len(posStops)) + ")", posStops)

    posStops = [s.zfill(4) for s in posStops if s.zfill(4) not in realStops]
    print("Not found : (" + str(len(posStops)) + ")", posStops)

    digit = ["".join([a for a in stop if a.isdigit()]) for stop in realStops]
    posStops = [s.zfill(4) for s in posStops if s.zfill(4) not in digit]

    print("Not found : (" + str(len(posStops)) + ")", posStops)


def analysePositions(transport):
    input_file = open("../Data/JSON/vehiclePosition01.json", "r")
    data = json.load(input_file)

    varianceNotFound = 0
    distanceNotValid = 0
    posCounter = 0

    for time in data["data"]:
        if time is not None:
            for response in time["Responses"]:
                if response is not None:
                    for line in response["lines"]:
                        if line is not None:
                            for position in line["vehiclePositions"]:
                                if position is not None:

                                    line_id = line["lineId"]
                                    terminus = transport.getRealStop(position["directionId"], line_id)
                                    if terminus is None:
                                        varianceNotFound += 1
                                        posCounter += 1
                                    else:
                                        variance = transport.getVariance(line_id, terminus)
                                        pointID = transport.getRealStop(position["pointId"], line_id, variance)
                                        distanceFromPoint = position["distanceFromPoint"]
                                        if pointID is not None:
                                            if not transport.isDistanceValid((line_id, variance),
                                                                             pointID,
                                                                             distanceFromPoint):
                                                distanceNotValid += 1
                                            else:
                                                posCounter += 1
    input_file.close()

    print("Variance not found :", varianceNotFound)
    print("Distance not valid :", distanceNotValid)
    print("Valid position :", posCounter)


def getAllVehiclesTest(positions, transport):
    allVehicles = {}

    for k in positions.keys():

        position = positions[k]

        # Remove technical stops
        position = transport.removeTechnicalStops(position, k)

        # Group + sorted by time
        times = groupSortByTime(position)

        vehicles = [[p] for p in times[0]]

        for t in times[1:]:

            input("Press to continue")
            print("-" * 150)
            transport.printVehicles(vehicles)
            print()
            print("Positions : " + ", ".join([transport.getStringPos(p) for p in t]))

            while len(t) > 0:

                index = transport.getIndexClosestVehicle(t[0], vehicles, k)

                if index != -1:
                    vehicles[index].append(t.pop(0))
                else:  # Not found
                    vehicles.append([t.pop(0)])

        print("-" * 150)
        transport.printVehicles(vehicles)
        allVehicles[k] = vehicles

    return allVehicles


def createVehiclesID(allVehicles, file_path):
    with open(file_path, "w") as file:
        file.write("Time, LineID, DirectionID, Variance, DistanceFromPoint, PointID, VehicleID \n")
        for k in allVehicles.keys():
            vehicles = allVehicles[k]
            for i in range(len(vehicles)):
                vehicle = vehicles[i]
                for position in vehicle:
                    time = str(position[0])
                    line = k[0]
                    terminus = position[3]
                    variance = str(int(k[1]) - 1)
                    distance = str(position[2])
                    last_stop = position[1]
                    vehicleID = str(i)

                    file.write(",".join([time, line, terminus, variance, distance, last_stop, vehicleID]) + "\n")


if __name__ == '__main__':
    analyseStopsID()
