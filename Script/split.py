n = "Stop-times+lines split"

input_file = open("Stop-times+lines modified.csv", "r")

line_number = -1
header = input_file.readline()

for line in input_file:
    if line.strip().split(";")[0].strip('"') != line_number:
        line_number = line.strip().split(";")[0].strip('"')
        output_file = open("{}/Line {}.csv".format(n,line_number), "w")
        output_file.write(header)

    output_file.write(line)
