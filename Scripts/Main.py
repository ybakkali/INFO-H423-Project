from Scripts.Analyze import createVehiclesID, getAllVehicles
from Scripts.ExtractData import getLineInfo, getStopsName, getPositionsFromCSV
from Scripts.Transport import Transport

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
    lines = getLineInfo("../Data/LinesInformation.csv")
    stopsName = getStopsName("../Data/gtfs23Sept/stops.txt")

    transport = Transport(lines, stopsName)

    positions = getPositionsFromCSV("../Data/CSV/vehiclePosition.csv")

    # yoyo(positions, transport)
    createVehiclesID(getAllVehicles(positions, transport), "../Data/CSV/vehiclePositionID.csv")

    # analyseStopsID(list(stopsName.keys()), positions)


if __name__ == '__main__':
    main()
