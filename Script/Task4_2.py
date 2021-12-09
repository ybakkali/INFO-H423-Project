import time

def readTracks(tracks_file):
	tracks = {}
	with open(tracks_file) as file :
		file.readline()
		for point in file:
			point = point.split(",")
			trackId = int(point[0])
			lat = float(point[1])
			lon = float(point[2])
			time = point[3]

			if trackId in tracks:
				tracks[trackId].append((lat,lon,time))
			else:
				tracks[trackId] = (lat,lon,time)

def readDataAndFirstRoundVoting(file_path):
	dico_vote = {}
	f = open(file_path, "r")
	f.readline()
	for line in f:
		line = line.split(",")
		if line[-3] != "" and line[-2] != "":
			the_key = (line[-3], line[-2])
			if the_key not in dico_vote:
				dico_vote[the_key] = 1
			else :
				dico_vote[the_key] += 1
		n = int(line[0])
	f.close()
	return n, dico_vote



def secondRoundVoting(n, dico_vote):
	p = 0.95*n
	res = []
	for k in dico_vote:
		if dico_vote[k] >= p :
			res.append(k)
	return res


def thirdRoundVoting():
	pass
	# Calculate Speed
	# Compare Speed between track and line(s)
	# 5km/h difference ?


def extractInfo(line_mode):
	line = str(int(line_mode[:-1]))
	transport_mode = line_mode[-1]
	return line, transport_mode


def convertTime(time_str):
	pattern = "%Y-%m-%dT%H:%M:%SZ"
	epoch = int(time.mktime(time.strptime(time_str,pattern)))
	return epoch


def computeDistance(lon1, lat1, lon2, lat2): # Copy Paste
	from math import radians, cos, sin, asin, sqrt
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
	return c * r


def computeSpeed(file_path):
	dico_speed = {}
	with open(file_path) as f :
		f.readline()
		lines = f.readlines()
		for i in range(len(lines)-1):
			line_info = lines[i].strip().split(",")
			line_info_next = lines[i+1].strip().split(",")
			t1 = convertTime(line_info[3])
			t2 = convertTime(line_info_next[3])
			delta_t = t2 - t1
			lon1, lat1 = float(line_info[2]), float(line_info[1])
			lon2, lat2 = float(line_info_next[2]), float(line_info_next[1])
			distance = computeDistance(lon1, lat1, lon2, lat2)
			speed = distance/delta_t
			dico_speed[(i, i+1)] = speed*3600 #3.6 and 1000 for milisec of epoch
	return dico_speed





def main():
	'''
	# Read Shape file for line data
	tracks = readTracks("../Data/GPStracks.csv")

	for trackId, points in tracks:
		geometry = [Point(a[1], a[0]) for a in points]
		count = {}

		for point in geometry:
		    for line_index, line in lines.iterrows():
		        distance = point.distance(line["geometry"])
		        if distance <= 10.0:
					if (line["LIGNE"], line["VARIANTE"]) in count:
						count[(line["LIGNE"], line["VARIANTE"])] += 1
					else:
						count[(line["LIGNE"], line["VARIANTE"])] = 1

		p = 0.95 * len(points)
		res = []
		for k in count:
			if count[k] >= p :
				res.append(k)
	'''
	n, dico_vote = readDataAndFirstRoundVoting("../ahaha.csv")
	more_than_90 = secondRoundVoting(n, dico_vote)
	speeds = computeSpeed("../Data/Track 7.csv")
	#print(n, "\n", dico_vote, "\n", more_than_90, "\n")
	for k,v in speeds.items():
		print(k, v)



if __name__ == '__main__':
	main()
