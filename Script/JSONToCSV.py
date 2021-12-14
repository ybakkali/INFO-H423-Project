import json
import os

from Script.ExtractData import getStopsName, getLineInfo
from Script.Transport import Transport


def jsonToCSV(input_file_path, output_file_path, transport, mode="w"):
    input_file = open(input_file_path, "r")
    data = json.load(input_file)

    output_file = open(output_file_path, mode)

    # output_file.write("Time, LineID, DirectionID, Variance, DistanceFromPoint, PointID \n")

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
                                    if terminus is not None:
                                        variance = transport.getVariance(line_id, terminus)
                                        pointID = transport.getRealStop(position["pointId"], line_id, variance)
                                        distanceFromPoint = position["distanceFromPoint"]
                                        if pointID is not None and transport.isDistanceValid((line_id, variance), pointID, distanceFromPoint):

                                            output_file.write(",".join([time["time"],
                                                                    line_id,
                                                                    terminus,
                                                                    variance,
                                                                    str(distanceFromPoint),
                                                                    pointID]) + "\n")
    output_file.close()

    input_file.close()


def createCSVs(directory_in, directory_out, transport):
    if not os.path.exists(directory_out):
        os.makedirs(directory_out)
    print("0 / 13 (0%) done")
    for i in range(1, 14):
        with open(directory_out + "/vehiclePosition{:02d}.csv".format(i), "w") as output_file:
            output_file.write("Time, LineID, DirectionID, Variance, DistanceFromPoint, PointID \n")

        jsonToCSV(directory_in + "/vehiclePosition{:02d}.json".format(i),
                  directory_out + "/vehiclePosition{:02d}.csv".format(i), transport)
        print(str(i) + " / 13 (" + str(round(i / 13 * 100)) + "%) done")


def createCSV(directory_in, directory_out, transport):
    if not os.path.exists(directory_out):
        os.makedirs(directory_out)
    with open(directory_out + "/vehiclePosition.csv", "w") as output_file:
        output_file.write("Time, LineID, DirectionID, Variance, DistanceFromPoint, PointID \n")
    print("0 / 13 done (0%)")
    for i in range(1, 14):
        jsonToCSV(directory_in + "/vehiclePosition{:02d}.json".format(i),
                  directory_out + "/vehiclePosition.csv", transport, "a")
        print(str(i) + " / 13 done (" + str(round(i / 13 * 100)) + "%)")


def main():
    lines = getLineInfo("../Data/Stops Distance.csv")
    stopsName = getStopsName("../Data/gtfs23Sept/stops.txt")
    transport = Transport(lines, stopsName)
    # createCSVs("../Data/JSON", "../Data/CSV", transport)
    createCSV("../Data/JSON", "../Data/CSV", transport)


if __name__ == '__main__':
    main()
