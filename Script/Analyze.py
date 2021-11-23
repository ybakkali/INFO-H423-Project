def analyseSpeed(positions, transport):

    allVehicles = getAllVehicles(positions, transport)

    for k in allVehicles.keys():
        vehicles = allVehicles[k]

        stops = transport.lines[k]
        speed = [[] for _ in range(len(stops) - 1)]
        transport.printVehicles(vehicles)


def getAllVehicles(allPositions, transport):
    allVehicles = {}

    for line in allPositions.keys():

        positions = allPositions[line]

        # Group + sorted by time
        times = groupSortByTime(positions)

        vehicles = [[p] for p in times[0]]

        for t in times[1:]:
            while len(t) > 0:

                index = transport.getIndexClosestVehicle(t[0], vehicles, line)

                if index != -1:
                    vehicles[index].append(t.pop(0))

                else:  # Not found
                    vehicles.append([t.pop(0)])

        allVehicles[line] = vehicles

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
