import time

def convert(filename, i):

    input_file = open("vehiclePosition split" + filename, "r")

    line_number = -1
    header = input_file.readline()

    for line in input_file:

        line = line.strip().split(";")
        line[4] = time.strftime('%H:%M:%S', time.localtime(int(line[4])))

        if line[0] != line_number:
            line_number = line[0]
            output_file = open("vehiclePosition split/{:02d}/Line {}.csv".format(i,line_number), "w")
            output_file.write(header)

        line = ";".join(line)
        line += '\n'
        output_file.write(line)

for i in range(1, 14):
    convert("/vehiclePosition{:02d}-reord.csv".format(i), i)
