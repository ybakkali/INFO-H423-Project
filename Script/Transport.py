from datetime import datetime
import re


class Transport:

    def __init__(self, parentStation, lines, stopsName):
        self.parentStation = parentStation
        self.lines = lines
        self.stopsName = stopsName

    def getRealStop(self, stopID, line):
        stopsID = [s[0] for s in self.lines[(line, "1")] + self.lines[(line, "2")]]

        if stopID in stopsID:
            return stopID

        stopID = stopID.zfill(4)

        if stopID in stopsID:
            return stopID

        for t in stopsID:
            if stopID == "".join([a for a in t if a.isdigit()]):
                return t

        return None

    def isSameStop(self, stop_1, stop_2):
        r = re.findall(stop_1, stop_2)
        if len(r) > 0:
            print(stop_1, ",", stop_2, ",", r)
        pos_1 = [stop_1, stop_1[:-1], "0" + stop_1]
        pos_2 = [stop_2, stop_2[:-1], "0" + stop_2]

        for t_1 in pos_1:
            for t_2 in pos_2:
                if t_1 == t_2:
                    return True
                #if t_1 in self.parentStation.keys() and t_2 in self.parentStation.keys() and \
                #        self.parentStation[t_1] == self.parentStation[t_2]:
                #    return True

        return False

    def getStationName(self, stop):
        for s in self.stopsName.keys():
            if stop in s:
                return self.stopsName[s]
        return "Unknown (" + stop + ")"

    def getIndexClosestVehicle(self, position, vehicles, line):  # position = (time, last_stop, distance, terminus)

        # [distance(pos, v) for v in vehicles] (stops_number, distance)
        stops = self.lines[line]
        index = -1
        stop_dist = -1

        for i in range(len(vehicles) - 1, -1, -1):
            vehicle = vehicles[i]
            # if isSameStop(vehicle[-1][3], position[3]): # Same terminus
            current_stop_dist = self.getIndexStop(position[1], stops) - self.getIndexStop(vehicle[-1][1], stops)

            if (vehicle[-1][0] < position[0]) and ((current_stop_dist == 0 and vehicle[-1][2] <= position[2]) or (
                    current_stop_dist > 0)):  # Later time + Forward

                if index == -1:  # first valid
                    index = i
                    stop_dist = current_stop_dist

                elif current_stop_dist < stop_dist:  # current closer than last
                    index = i
                    stop_dist = current_stop_dist

                elif current_stop_dist == stop_dist:  # current + last same segment
                    if vehicle[-1][2] <= vehicles[index][-1][2]:
                        index = i
                        stop_dist = current_stop_dist

        return index

    def getIndexStop(self, stop, stops):
        i = 0
        for i in range(len(stops)):
            if self.isSameStop(stop, stops[i][0]):
                return i
        raise

    def getVariance(self, line, direction):
        if direction in [s[0] for s in self.lines[(line, "1")]]:
            return "1"
        elif direction in [s[0] for s in self.lines[(line, "2")]]:
            return "2"
        else:
            raise

    def removeTechnicalStops(self, position, line):
        p = 0
        while p < len(position):
            pos = position[p]
            found = False
            i = 0
            while not found and i < len(self.lines[line]):
                stop = self.lines[line][i]
                if self.isSameStop(stop[0], pos[1]):
                    found = True
                i += 1

            # TEST

            i = 0
            while not found and i < len(self.stopsName.keys()):
                stop = list(self.stopsName.keys())[i]
                if self.isSameStop(stop, pos[1]):
                    found = True
                    print("Stop " + pos[1] + " not in line " + line[0] + " but is an existing stop")
                i += 1

            if not found:
                print("Stop " + pos[1] + " is a technical stop")
                position.pop(p)
            else:
                p += 1
        return position

    def printVehicles(self, vehicles):
        for v in range(len(vehicles)):
            t = []
            for pos in vehicles[v]:  # [-2:]: # TEST
                a = self.getStringPos(pos)
                t.append(a)
            print("Vehicle " + str(v) + "(" + str(len(vehicles[v])) + ")" + " : " + " --> ".join(t) + "\n")

    def getStringPos(self, pos):
        return self.getStationName(pos[1]) + " : " + str(pos[2]) + " m at " + \
               datetime.utcfromtimestamp(pos[0] / 1000).strftime("%H:%M:%S")
        # + " (terminus : " + getStationName(pos[3]) + ")" # datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
