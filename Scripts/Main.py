from Scripts.Analyze import createVehiclesID, getAllVehicles, analysePositions
from Scripts.ExtractData import getLineInfo, getStopsName, getPositionsFromCSV
from Scripts.Transport import Transport


def main():

    lines = getLineInfo("../Data/LinesInformation.csv")

    stopsName = getStopsName("../Data/gtfs23Sept/stops.txt")

    transport = Transport(lines, stopsName)

    positions = getPositionsFromCSV("../Data/CSV/vehiclePosition.csv")

    createVehiclesID(getAllVehicles(positions, transport), "../Data/CSV/vehiclePositionID.csv")

    # analyseStopsID(list(stopsName.keys()), positions)

    # analysePositions(transport)


if __name__ == '__main__':
    main()
