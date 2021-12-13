def analyseSpeed(positions, transport):

    allVehicles = getAllVehicles(positions, transport)

    for k in allVehicles.keys():
        vehicles = allVehicles[k]

        stops = transport.lines[k]
        speed = [[] for _ in range(len(stops) - 1)]
        transport.printVehicles(vehicles)


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
                if t[0][0] - vehicles[a][-1][0] > 300000:
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


def analyseStopsID(stopsID, positions):
    stopsID = [s for s in stopsID if len(s) > 2]

    # print(stopsID)
    """
    a = {}
    for s in stopsID:
        if len(s) not in a.keys():
            a[len(s)] = 1
        else:
            a[len(s)] += 1

    print("Length of stopsID :", a)
    """

    posStopID = set()
    for line in positions.keys():
        for pos in positions[line]:
            posStopID.add(pos[1])

    # print(posStopID)
    """
    b = {}
    for s in posStopID:
        if len(s) not in b.keys():
            b[len(s)] = 1
        else:
            b[len(s)] += 1
    print("Length of stopsID :", b)
    """

    # print("Intersection :", stopsID.intersection(posStopID))
    # print("Difference :", stopsID.difference(posStopID))

    print(len(posStopID), "different stops")

    not_found = [s for s in posStopID if s not in stopsID]
    print("Not found : (" + str(len(not_found)) + ")", not_found)

    not_found = [s.zfill(4) for s in not_found if s.zfill(4) not in stopsID]
    print("Not found : (" + str(len(not_found)) + ")", not_found)

    temp = []
    for s in not_found:
        found = False
        last_found = ""
        for t in stopsID:
            #print(s, "|", t, "".join([a for a in t if a.isdigit()]))
            if s == "".join([a for a in t if a.isdigit()]):
                #if found:
                #    print("Strange", last_found, "|", t)
                found = True
                last_found = t

        if not found:
            temp.append(s)

    not_found = temp
    print("Not found : (" + str(len(not_found)) + ")", not_found)


def getAllVehiclesTest(positions, transport):
    allVehicles = {}

    for k in positions.keys():
        # k = ("7","2") # TEST
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
                    variance = str(int(k[1]) - 1)  # Fuck Yahya
                    distance = str(position[2])
                    last_stop = position[1]
                    vehicleID = str(i)

                    file.write(",".join([time, line, terminus, variance, distance, last_stop, vehicleID]) + "\n")
