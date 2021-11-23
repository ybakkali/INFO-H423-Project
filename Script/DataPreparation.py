from Script.Analyze import analyseSpeed, groupSortByTime
from Script.ExtractData import getParentStation, getLineInfo, getStopsName, getPositionsFromCSV

# data["data"][250]["Responses"][0]["lines"][0]["vehiclePositions"]
from Script.Transport import Transport


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


"""
def yoyo(positions, transport):
    lines = [p[0] for p in positions.keys() if p[1] == "0"]
    lines.sort(key=lambda x: int(x))
    a = 0
    b = 0
    for line in lines:
        j = 0
        k = 0
        for position in positions[(line, "0")]:
            belong = False
            for stop in transport.lines[(line, "1")] + transport.lines[(line, "2")]:
                if transport.isSameStop(position[3], stop[0]):
                    belong = True

            if not belong:
                j += 1
                a += 1

            else:
                k += 1
                b += 1

        print("Line", str(line), ":", str(j), "not in line |", str(k), "in line")
    print("Total :", str(a), "not in line |", str(b), "in line")
"""


def main():
    parentStation = getParentStation("../Data/gtfs23Sept/stops.txt")
    lines = getLineInfo("../Data/Stops Distance.csv")
    stopsName = getStopsName("../Data/gtfs23Sept/stops.txt")

    transport = Transport(parentStation, lines, stopsName)

    # createCSVs("../Data") # Path to data
    positions = getPositionsFromCSV("../Data/CSV/vehiclePosition01.csv")

    # yoyo(positions, transport)
    # createVehiclesID(getAllVehicles(positions, transport), "../Data/vehicleIDPosition01.csv")
    analyseSpeed(positions, transport)

    # analyseStopsID(list(stopsName.keys()), positions)


if __name__ == '__main__':
    main()
