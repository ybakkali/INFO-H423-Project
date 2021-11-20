n = "Stop-times+lines split"

input_file = open("Stop-times+lines.csv", "r")
output_file = open("Stop-times+lines modified.csv", "w")

header = input_file.readline()
output_file.write(header)


for line in input_file:

    line = line.strip().split(";")

    time = line[3].strip('"').split(":")
    time_ = line[4].strip('"').split(":")

    time[0] = "{:02d}".format(int(time[0]) % 24)
    time_[0] = "{:02d}".format(int(time_[0]) % 24)

    line[3] = '"' + ":".join(time) + '"'
    line[4] = '"' + ":".join(time_) + '"'

    line = ";".join(line)
    output_file.write(line + "\n")
