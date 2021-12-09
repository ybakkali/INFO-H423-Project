



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
	return n, dico_vote



def secondRoundVoting(n, dico_vote):
	p = 0.95*n
	res = []
	for k in dico_vote:
		if dico_vote[k] >= p :
			res.append(k)
	return res


#def thirdRoundVoting()




def main():
	n, dico_vote = readDataAndFirstRoundVoting("../ahaha.csv")
	more_than_90 = secondRoundVoting(n, dico_vote)
	print(n, "\n", dico_vote, "\n", more_than_90)



if __name__ == '__main__':
	main()
