import json
from datetime import datetime

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



def getPositionsFromCSV(file_path):
    positions = {}
    i = 0 # TEST
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

            if line == ("2"): # TEST
                i += 1 # TEST
                if i > 1000: break # TEST
                if variance != "0":
                    if (line, variance) not in positions.keys():
                        positions[(line, variance)] = [(time, last_stop, distance, terminus)]
                    else:
                        positions[(line, variance)].append((time, last_stop, distance, terminus))

    return positions


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

def getPositions(file_path):
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
                                    variance = getVariance(l, direction, last)
                                    #i += 1 if variance != "0" else 0
                                    #j += 1

                                    if variance != "0":
                                        if (l, variance) not in positions.keys():
                                            positions[(l, variance)] = [(t, last, distance)]
                                        else:
                                            positions[(l, variance)].append((t, last, distance))

    #print(i)
    #print(j)
    input_file.close()

    return positions

def getVariance(line, direction, last): # TODO intermediate terminus stops
    global Lines

    if isSameStop(Lines[(line, "1")][-1][0], direction):
        return "1"

    if isSameStop(Lines[(line, "2")][-1][0], direction):
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


def removeTechnicalStops(position, line):
    global Lines
    p = 0
    while p < len(position):
        pos = position[p]
        found = False
        i = 0
        while not found and i < len(Lines[line]):
            stop = Lines[line][i]
            if isSameStop(stop[0], pos[1]):
                found = True
            i += 1

        # TEST

        i = 0
        while not found and i < len(StopsName.keys()):
            stop = list(StopsName.keys())[i]
            if isSameStop(stop, pos[1]):
                found = True
                print("Stop " + pos[1] + " not in line " + line[0] + " but is an existing stop")
            i += 1

        if not found:
            print("Stop " + pos[1] + " is a technical stop")
            position.pop(p)
        else:
            p += 1
    return position


def groupSortByTime(position):
    position.sort(key=lambda x: x[0])
    times = []
    last_time = "-1"
    for p in position:
        if last_time != p[0]:
            last_time = p[0]
            times.append([])
        times[-1].append(p)

    return times


    # positions[(l, variance)] = [(time, last, distance), ...]
def analyseSpeed(positions):
    global StopsName

    for k in positions.keys():
        #k = ("7","2") # TEST
        position = positions[k]

        # Remove technical stops
        position = removeTechnicalStops(position, k)

        # Group + sorted by time
        times = groupSortByTime(position)


        vehicles = [[p] for p in times[0]]

        for t in times[1:]:
            # TEST

            input("Press to continue")
            print("-" * 150)
            printVehicles(vehicles)
            print()
            print("Positions : " + ", ". join([getStringPos(p) for p in t]))
            # TEST

            for i in range(len(vehicles)-1, -1, -1):
                # search the closest forward vehicle
                index = getIndexClosestVehicle(vehicles[i][-1], t, k)
                if index != -1:
                    vehicles[i].append(t.pop(index))

            if len(t) > 0:
                # It means new vehicle(s)
                for p in t:
                    vehicles.append([p])
        print("-" * 150) # TEST
        printVehicles(vehicles)


        break # TEST

def printVehicles(vehicles):
    for v in range(len(vehicles)):
        t = []
        for pos in vehicles[v][-2:]: # TEST
            a = getStringPos(pos)
            t.append(a)
        print("Vehicle " + str(v) + " : " + " --> ".join(t) + "\n")

def getStringPos(pos):
    return getStationName(pos[1]) + " : " + str(pos[2]) + " m at " + datetime.utcfromtimestamp(pos[0]/1000).strftime("%H:%M:%S") #+ " (terminus : " + getStationName(pos[3]) + ")" # datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def getIndexStop(stop, stops):
    i = 0
    for i in range(len(stops)):
        if isSameStop(stop, stops[i][0]):
            return i
    raise


def getIndexClosestVehicle(vehicle_last_position, positions, line): # positions* # position = (time, last_stop, distance, terminus)
    global Lines
    index = -1
    stop_dist = -1
    stops = Lines[line]
    for i in range(len(positions)):
        try:
            position = positions[i]
            if isSameStop(vehicle_last_position[3], position[3]): # Same terminus
                current_stop_dist = getIndexStop(position[1], stops) - getIndexStop(vehicle_last_position[1], stops)

                if (current_stop_dist == 0 and vehicle_last_position[2] <= position[2]) or (current_stop_dist > 0):
                    if index == -1: # first valid
                        index = i
                        stop_dist = current_stop_dist

                    elif current_stop_dist < stop_dist: # current closer than last
                        index = i
                        stop_dist = current_stop_dist

                    elif current_stop_dist == stop_dist: # current + last same segment
                        if position[2] <= positions[index][2]:
                            index = i
                            stop_dist = current_stop_dist

        except Exception as e:
            # print(e, "|",stops)
            pass
    return index


def isSameStop(stop_1, stop_2):
    global ParentStation
    pos_1 = [stop_1, stop_1[:-1], "0" + stop_1]
    pos_2 = [stop_2, stop_2[:-1], "0" + stop_2]

    for t_1 in pos_1:
        for t_2 in pos_2:
            if t_1 == t_2:
                return True
            if t_1 in ParentStation.keys() and t_2 in ParentStation.keys() and ParentStation[t_1] == ParentStation[t_2]: # Parent Station
                return True

    return False

def getStationName(stop):
    global StopsName
    for s in StopsName.keys():
        if stop in s:
            return StopsName[s]
    return "Unknown (" + stop + ")"

def main():
    global ParentStation, Lines, StopsName

    ParentStation = getParentStation("Data/gtfs23Sept/stops.txt")
    Lines = getLineInfo("Data/Stops Distance.csv")
    StopsName = getStopsName("Data/gtfs23Sept/stops.txt")

    # createCSVs("Data") # Path to data
    positions = getPositionsFromCSV("Data/vehiclePosition01.csv")
    # positions = getPositions("Data/vehiclePosition01.json")

    analyseSpeed(positions)

if __name__ == '__main__':
    main()
