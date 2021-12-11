import math
from datetime import datetime


class Transport:

    def __init__(self, parentStation=None, lines=None, stopsName=None, speedStop=None):
        self.parentStation = parentStation
        self.lines = lines
        self.stopsName = stopsName
        self.speedStop = speedStop

    def getRealStop(self, stopID, lineID, variance=None):
        if variance is None:
            stopsID = self.getStops((lineID, "1")) + self.getStops((lineID, "2"))

        else:
            stopsID = self.getStops((lineID, variance))

        if stopID in stopsID:
            return stopID

        stopID = stopID.zfill(4)

        if stopID in stopsID:
            return stopID

        for t in stopsID:
            if stopID == "".join([a for a in t if a.isdigit()]):
                return t

        return None

    def getStops(self, line):
        return [s[0] for s in self.lines[line]]

    def getStationName(self, stop):
        for s in self.stopsName.keys():
            if stop in s:
                return self.stopsName[s]
        return "Unknown (" + stop + ")"

    def getIndexClosestVehicle(self, position, vehicles, line):  # position = (time, last_stop, distance, terminus)

        # [distance(pos, v) for v in vehicles] (stops_number, distance)
        index = -1
        stop_dist = -1

        for i in range(len(vehicles) - 1, -1, -1):
            vehicle = vehicles[i]

            if (vehicle[-1][3] == position[3]) and (vehicle[-1][0] < position[0]):  # Same Terminus + Later time
                if ((position[0] - vehicle[-1][0]) < 120000) and (self.getSpeed(vehicle[-1], position, line) <= 100):  # 2 min timeout + 100km/h limit
                    current_stop_dist = self.getIndexStop(position[1], line) - self.getIndexStop(vehicle[-1][1], line)

                    if (current_stop_dist <= 1) and ((current_stop_dist == 0 and vehicle[-1][2] <= position[2]) or (
                            current_stop_dist > 0)):  # Forward

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

    def getSpeed(self, vehicle_last_position, position, line):
        d = ((self.getDistanceStop(position[1], line) + position[2]) - (self.getDistanceStop(vehicle_last_position[1], line) + vehicle_last_position[2])) / 1000
        t = (position[0] - vehicle_last_position[0]) / 3600000
        return d/t

    def getDistanceStop(self, stop, line):
        return self.lines[line][self.getIndexStop(stop, line)][1]

    def getIndexStop(self, stop, line):
        return self.getStops(line).index(stop)

    def getVariance(self, line, direction):
        if direction in self.getStops((line, "1")):
            return "1"
        elif direction in self.getStops((line, "2")):
            return "2"
        else:
            raise

    def isDistanceValid(self, line, pointID, distanceFromPoint):
        i = self.getIndexStop(pointID, line)
        return (i + 1 == len(self.lines[line])) or (self.lines[line][i+1][1] - self.lines[line][i][1] >= distanceFromPoint)

    def printVehicles(self, vehicles):
        for v in range(len(vehicles)):
            t = []
            for pos in vehicles[v]:
                a = self.getStringPos(pos)
                t.append(a)
            print("Vehicle {0}({1}) : {2}\n".format(str(v), self.getStationName(vehicles[v][0][3]), " --> ".join(t)))

    def getStringPos(self, pos):
        return self.getStationName(pos[1]) + " : " + str(pos[2]) + " m at " + \
               datetime.utcfromtimestamp(pos[0] / 1000).strftime("%H:%M:%S")

    def getAverageSpeedStop(self, line, stop_1, stop_2):
        index_1 = self.getIndexStop(stop_1, line)
        index_2 = self.getIndexStop(stop_2, line)

        if index_2 - index_1 <= 0:
            return -math.inf

        speeds = self.speedStop[line][index_1:index_2]

        average = sum(speeds)/len(speeds)

        return average
