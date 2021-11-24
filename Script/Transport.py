from datetime import datetime


class Transport:

    def __init__(self, parentStation, lines, stopsName):
        self.parentStation = parentStation
        self.lines = lines
        self.stopsName = stopsName

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

            if (vehicle[-1][3] == position[3]) and ((position[0] - vehicle[-1][0]) < 120000):  # Same terminus + timeout 2 minutes TODO distance limit
                current_stop_dist = self.getIndexStop(position[1], line) - self.getIndexStop(vehicle[-1][1], line)

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

    def getIndexStop(self, stop, line):
        return self.getStops(line).index(stop)

    def getVariance(self, line, direction):
        if direction in self.getStops((line, "1")):
            return "1"
        elif direction in self.getStops((line, "2")):
            return "2"
        else:
            raise

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
