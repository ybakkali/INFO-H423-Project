import json


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


def getLineInfo(file_path):  # lines = {(num_line, var) : [(succession, stop_id, dist), ...], ...}
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
        temp_lines[l].sort(key=lambda a: a[0])
        lines[l] = [(s[1], s[2]) for s in temp_lines[l]]

    return lines


def getStopsName(file_path):
    stopsName = {}
    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            info = line.strip().split(",")
            line = info[0]
            name = info[2]
            stopsName[line] = name

    return stopsName


def getPositions(file_path, transport):
    input_file = open(file_path, "r")
    data = json.load(input_file)
    positions = {}
    times = []
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
                                    t = time["time"]
                                    l = line["lineId"]
                                    direction = position["directionId"]
                                    distance = position["distanceFromPoint"]
                                    last = position["pointId"]
                                    variance = transport.getVariance(l, direction)
                                    # i += 1 if variance != "0" else 0
                                    # j += 1

                                    if variance != "0":
                                        if (l, variance) not in positions.keys():
                                            positions[(l, variance)] = [(t, last, distance)]
                                        else:
                                            positions[(l, variance)].append((t, last, distance))

    # print(i)
    # print(j)
    input_file.close()

    return positions


def getPositionsFromCSV(file_path):
    positions = {}

    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            info = line.strip().split(",")

            time = int(info[0])
            line = info[1]
            terminus = info[2]
            variance = info[3]
            distance = float(info[4])
            last_stop = info[5]

            if (line, variance) not in positions.keys():
                positions[(line, variance)] = [(time, last_stop, distance, terminus)]

            else:
                positions[(line, variance)].append((time, last_stop, distance, terminus))

    return positions
