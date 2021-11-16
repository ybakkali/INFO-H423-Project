import json

def jsonToCSV(input_file_path, output_file_path):
    input_file = open(input_file_path, "r")
    data = json.load(input_file)

    output_file = open(output_file_path, "w")

    output_file.write("Time, LineID, DirectionID, Variance, DistanceFromPoint, PointID \n")

    for time in data["data"]:
        if time is not None:
            for response in time["Responses"]:
                if response is not None:
                    for line in response["lines"]:
                        if line is not None:
                            for position in line["vehiclePositions"]:
                                if position is not None:
                                    output_file.write(",".join( [time["time"],
                                                                line["lineId"],
                                                                position["directionId"],
                                                                getVariance(line["lineId"], position["directionId"], "lol"),
                                                                str(position["distanceFromPoint"]),
                                                                position["pointId"]]) + "\n")
    output_file.close()

    input_file.close()

# data["data"][250]["Responses"][0]["lines"][0]["vehiclePositions"]


def getPositions(file_path):
    input_file = open(file_path, "r")
    data = json.load(input_file)
    positions = {}
    i = 0
    j = 0
    for time in data["data"]:
        if time is not None:
            for response in time["Responses"]:
                if response is not None:
                    for line in response["lines"]:
                        if line is not None:
                            for position in line["vehiclePositions"]:
                                if position is not None:
                                    # output_file.write(",".join([time["time"], line["lineId"], position["directionId"], str(position["distanceFromPoint"]), position["pointId"]]) + "\n")
                                    time = time["time"]
                                    l = line["lineId"]
                                    direction = position["directionId"]
                                    distance = position["distanceFromPoint"]
                                    last = position["pointId"]
                                    variance = getVariance(l, direction, last)
                                    i += 1 if variance != "0" else 0
                                    j += 1

                                    position[(l, variance)] = [(last, distance)]

                                    # position = {(lineID,variance) : (time, lastStop, distance)}
                                    # position = {(lineID,variance) : [time, [(lastStop, distance), ...], ...]}
                                    #if (num_line, var) not in temp_lines.keys():
                                    #    temp_lines[(num_line, var)] = [(succession, stop_id, dist)]
                                    #else:
                                    #    temp_lines[(num_line, var)].append((succession, stop_id, dist))
    print(i)
    print(j)
    input_file.close()

    return positions

def getVariance(line, direction, last):

    if lines[(line, "1")][-1][0] == direction:
        return "1"

    if lines[(line, "2")][-1][0] == direction:
        return "2"

    if direction in parentStation.keys(): # Parent Station
        if lines[(line, "1")][-1][0] in parentStation.keys() and parentStation[lines[(line, "1")][-1][0]] == parentStation[direction]:
            return "1"

        if lines[(line, "2")][-1][0] in parentStation.keys() and parentStation[lines[(line, "2")][-1][0]] == parentStation[direction]:
            return "2"

    if lines[(line, "1")][-1][0][:-1] == direction:
        return "1"

    if lines[(line, "2")][-1][0][:-1] == direction:
        return "2"

    return "0" # "1" or "2" / 0 == error



def createCSVs(directory):
	for i in range(1, 14):
		jsonToCSV(directory + "/vehiclePosition{:02d}.json".format(i), directory + "/vehiclePosition{:02d}.csv".format(i))



def getParentStation(file_path):
    res = {}
    with open(file_path, "r") as input_file:
        input_file.readline()

        for line in input_file:
            line = line.strip()
            info = line.split(",")
            if info[9] != "":
                res[info[0]] = info[9]
    return res


def getLineInfo(file_path):
    temp_lines = {}
    with open(file_path, "r") as input_file:
        input_file.readline()
        for line in input_file:
            line = line.strip()
            info = line.split(",")

            num_line = info[11].strip("\"")
            var = info[1].strip("\"")
            succession = int(info[2].strip("\""))
            stop_id = info[3].strip("\"")
            dist = float(info[13].strip("\""))


            if (num_line, var) not in temp_lines.keys():
                temp_lines[(num_line, var)] = [(succession, stop_id, dist)]
            else:
                temp_lines[(num_line, var)].append((succession, stop_id, dist))

    lines = {}

    for l in temp_lines.keys():
        temp_lines[l].sort(key = lambda a : a[0])
        lines[l] = [(s[1], s[2]) for s in temp_lines[l]]


    return lines



if __name__ == '__main__':
    parentStation = getParentStation("Data/gtfs23Sept/stops.txt")
    lines = getLineInfo("Data/Stops Distance.csv")

    createCSVs("Data") # Path to data

    # positions = getPositions("Data/vehiclePosition01.json")
