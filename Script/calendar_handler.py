"""
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

"""
import datetime

dico_excep_1 = {}
dico_excep_2 = {}


def before_after_day(s):
    d = datetime.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    before = str(d - datetime.timedelta(days=1))
    after = str(d + datetime.timedelta(days=1))
    before = "".join(before.split("-"))
    after = "".join(after.split("-"))
    return before, after


def read_cal_dates(file_path):
    global dico_excep_1
    f = open(file_path, "r")

    for line in f:
        line = line.strip().split(",")

        if line[2] == "1":
            dico_excep_1[line[0]] = line[1]
        if line[2] == "2":

            if line[0] not in dico_excep_2:
                dico_excep_2[line[0]] = [[line[1]]]
            else:
                lst = dico_excep_2[line[0]]
                s = line[1]
                d = datetime.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
                found = False
                for i in range(len(lst)):
                    for k in lst[i]:
                        g = datetime.date(int(k[0:4]), int(k[4:6]), int(k[6:8]))
                        if abs((g - d).days) == 1:
                            dico_excep_2[line[0]][i].append(s)
                            found = True
                            break
                    if found:
                        break
                if not found:
                    dico_excep_2[line[0]] += [[s]]

    f.close()


def insert_date(s):
    global dico_excep_1
    lst = ["0" for _ in range(7)]
    date = datetime.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    lst[date.weekday() - 1] = "1"
    return "," + ",".join(lst) + "," + s + "," + s


def read_cal(file_path, out_path):
    f = open(file_path, "r")
    w = open(out_path, "w")
    w.write(f.readline())
    for line in f:
        t = line.strip()
        line = line.strip().split(",")

        if line[0] in dico_excep_1:
            if t != line[0] + insert_date(dico_excep_1[line[0]]):
                start = datetime.date(int(line[8][0:4]), int(line[8][4:6]), int(line[8][6:8]))
                end = datetime.date(int(line[9][0:4]), int(line[9][4:6]), int(line[9][6:8]))
                s = dico_excep_1[line[0]]
                new_date = datetime.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
                if not (start <= new_date <= end):
                    w.write(line[0] + insert_date(dico_excep_1[line[0]]) + "\n")

        if line[0] in dico_excep_2:
            w.write(remove_date(line))
        else:
            w.write(",".join(line) + "\n")

    f.close()
    w.close()


def remove_date(line):
    dates = dico_excep_2[line[0]]

    lines = ""
    start = line[8]
    end = line[9]

    for lst in dates:

        before = before_after_day(lst[0])[0]
        after = before_after_day(lst[-1])[1]

        str = ",".join(line[:8])
        if start == before:
            start = after
        elif end == after:
            lines += str + "," + start + "," + before + "\n"
            break
        else:
            lines += str + "," + start + "," + before + "\n"
            start = after

    return lines


if __name__ == '__main__':
    read_cal_dates("../Data/gtfs23Sept/calendar_dates.txt")
    read_cal("../Data/gtfs23Sept/calendar.txt", "../Data/gtfs23Sept/new_calendar.txt")
