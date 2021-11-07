import json


#"Data/vehiclePosition08.json"
#Data/raw.csv


def jsonToCSV(input_file_path, output_file_path):
    input_file = open(input_file_path, "r")
    data = json.load(input_file)

    output_file = open(output_file_path, "w")

    output_file.write("Time, LineID, DirectionID, DistanceFromPoint, PointID \n")

    for time in data["data"]:
        if time is not None:
            for response in time["Responses"]:
                if response is not None:
                    for line in response["lines"]:
                        if line is not None:
                            for position in line["vehiclePositions"]:
                                if position is not None:
                                    output_file.write(",".join([time["time"], line["lineId"], position["directionId"], str(position["distanceFromPoint"]), position["pointId"]]) + "\n")
    output_file.close()

    input_file.close()
# data["data"][250]["Responses"][0]["lines"][0]["vehiclePositions"]

# print(data)

for i in range(1, 14):
    jsonToCSV("Data/vehiclePosition{:02d}.json".format(i), "Data/vehiclePosition{:02d}.csv".format(i))
