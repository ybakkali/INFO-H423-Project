import pandas as pd
import geopandas as gpd
import io
from fiona.io import ZipMemoryFile
from shapely.geometry import Point
import time
from haversine import haversine, Unit

from ExtractData import getLineInfo, getStopsName, getSpeed
from Transport import Transport


def getLines(file='../Data/shapefiles23Sept.zip'):
    zipshp = io.BytesIO(open(file, 'rb').read())

    with (ZipMemoryFile(zipshp)) as memfile:
        with memfile.open("2109_STIB_MIVB_Network") as src:
            lines = gpd.GeoDataFrame.from_features(src)
            lines.set_crs(epsg=31370)
    return lines


def readTracks(tracks_file):
    tracks = {}
    with open(tracks_file) as file:
        file.readline()
        for point in file:
            point = point.strip().split(",")
            trackId = int(point[0])
            lat = float(point[1])
            lon = float(point[2])
            t = point[3]

            if trackId in tracks:
                tracks[trackId].append((lat, lon, t))
            else:
                tracks[trackId] = [(lat, lon, t)]

    return tracks


def countPointsDistanceLines(geo_df, lines):
    count = {}
    for _, point in geo_df.iterrows():
        for line_index, line in lines.iterrows():
            distance = point["geometry"].distance(line["geometry"])
            if distance <= 10.0:
                if (line["LIGNE"], line["VARIANTE"]) in count:
                    count[(line["LIGNE"], line["VARIANTE"])] += 1
                else:
                    count[(line["LIGNE"], line["VARIANTE"])] = 1
    return count


def extractInfo(line_mode):
    line = (str(int(line_mode[0][:-1])), str(line_mode[1]))
    transport_mode = line_mode[0][-1]
    return line, transport_mode


def convertTime(time_str):
    try:
        epoch = int(time.mktime(time.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")))
    except:
        epoch = int(time.mktime(time.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")))

    return epoch


def computeSpeed(points):  # (lat, lon, time)
    speeds = []
    time_counter = 0
    distance_sum = 0
    for i in range(len(points) - 1):
        point = points[i]
        next_point = points[i + 1]
        t1 = convertTime(point[2])
        t2 = convertTime(next_point[2])
        delta_t = (t2 - t1)
        time_counter += delta_t
        point1 = (float(point[0]), float(point[1]))
        point2 = (float(next_point[0]), float(next_point[1]))
        distance = haversine(point1, point2, unit=Unit.KILOMETERS)
        distance_sum += distance
        if time_counter >= 30:
            speed = (distance_sum / time_counter) * 3600  # km/s --> km/h
            speeds.append(speed)
            time_counter = 0
            distance_sum = 0

    return speeds


def getClosestStop(stops, point):
    min = None
    id = None

    for _, stop in stops.iterrows():
        if min is None:
            min = point["geometry"].distance(stop["geometry"])
            id = stop["ID"]

        else:
            distance = point["geometry"].distance(stop["geometry"])
            if distance < min:
                min = distance
                id = stop["ID"]

    return id


def getStops(file_path, line):
    stops = []
    points = []
    with open(file_path) as file:
        file.readline()
        for data in file:
            data = data.split(",")
            if data[11] == '"' + line[0] + '"' and data[1] == '"' + line[1] + '"':
                point = Point((float(data[8]), float(data[9])))
                points.append(point)
                stops.append(data[3])
    df = pd.DataFrame()
    df["ID"] = stops
    geo_df = gpd.GeoDataFrame(df, geometry=points).set_crs(epsg=31370)
    return geo_df


def main():
    lines = getLines()
    tracks = readTracks("../Data/GPStracks.csv")

    stopsName = getStopsName("../Data/gtfs23Sept/stops.txt")
    speedStop = getSpeed("../Data/CSV/SpeedStop.csv")

    transport = Transport(lines=getLineInfo("../Data/LinesInformation.csv"), stopsName=stopsName, speedStop=speedStop)

    for trackId, points in tracks.items():
        geometry = [Point((a[1], a[0])) for a in points]
        geo_df = gpd.GeoDataFrame(points, geometry=geometry).set_crs(epsg=4326).to_crs(epsg=31370)
        count = countPointsDistanceLines(geo_df, lines)

        p = 0.75 * len(points)
        vote = []
        candidate_lines = []
        for k in count:
            if count[k] >= p:
                vote.append(count[k])
                candidate_lines.append(k)

        print("Track ID:  ", trackId)
        print("."*25)
        print("Position analysis: \n")
        print("Candidate lines: ", candidate_lines, "\nVotes: ", vote, " / ", len(points))
        percentages = [round(elem/len(points)*100, 3) for elem in vote]
        print("Percentages: ", percentages)
        print("."*25)
        print("Speed analysis:\n")

        if len(candidate_lines) == 0:
            track_transport_mode = None
            line_info = (None, None)
            print("."*25)

        else:
            speeds = computeSpeed(points)

            average_speed = sum(speeds) / len(speeds)

            i = 0
            while i < len(candidate_lines):
                candidate_line = candidate_lines[i]
                line, _ = extractInfo(candidate_line)

                stops = getStops("../Data/LinesInformation.csv", line)

                stop_1 = getClosestStop(stops, geo_df.iloc[0]).strip('"')  # [1:-1]
                stop_2 = getClosestStop(stops, geo_df.iloc[-1]).strip('"')  # [1:-1]
                average_line_speed = transport.getAverageSpeedStop(line, stop_1, stop_2)

                print("Line and variance ", line, "\nstops (from --> to): ", stop_1, " --> ", stop_2)
                print("Average line speed: ", average_line_speed)
                print("Average track speed: ", average_speed)
                print("."*25)

                if abs(average_line_speed - average_speed) > 20:
                    candidate_lines.pop(i)
                else:
                    i += 1

            if len(candidate_lines) == 0:
                track_transport_mode = None
                line_info = (None, None)

            else:
                lst = [(candidate_line, count[candidate_line]) for candidate_line in candidate_lines]
                lst.sort(key=lambda x: x[1])
                line_info, track_transport_mode = extractInfo(lst[-1][0])

        string_transport_mode = "Other" if track_transport_mode is None else track_transport_mode
        print("Result: \n")
        print("Track: ", trackId, " --> transport mode", string_transport_mode, end="")
        print(" (Probably the line is: ", line_info[0], ")")
        print("*"*100, "\n")


if __name__ == '__main__':
    main()
