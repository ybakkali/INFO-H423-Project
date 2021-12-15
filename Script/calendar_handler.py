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
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().split(",")

            if line[2] == "1":
                dico_excep_1[line[0]] = line[1]
            elif line[2] == "2":
                add_exception_2(line)


def add_exception_2(line):
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


def insert_date(s):
    lst = ["0" for _ in range(7)]
    date = datetime.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    lst[date.weekday()] = "1"
    return "," + ",".join(lst) + "," + s + "," + s


def read_cal(file_path, out_path):
    f = open(file_path, "r")
    w = open(out_path, "w")
    w.write(f.readline())
    for line in f:
        t = line.strip()
        line = line.strip().split(",")

        if line[0] in dico_excep_1:
            excep_date = dico_excep_1[line[0]]
            """
            if t != line[0] + insert_date(excep_date):
                start = datetime.date(int(line[8][0:4]), int(line[8][4:6]), int(line[8][6:8]))
                end = datetime.date(int(line[9][0:4]), int(line[9][4:6]), int(line[9][6:8]))
                new_date = datetime.date(int(excep_date[0:4]), int(excep_date[4:6]), int(excep_date[6:8]))
                if not (start <= new_date <= end):
                    w.write(line[0] + insert_date(excep_date) + "\n")
            """
            w.write(",".join(line) + "\n")
            w.write(line[0] + insert_date(excep_date) + "\n")

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

        prefix = ",".join(line[:8])

        if before < start:
            start = after
        elif start == before:
            lines += prefix + "," + start + "," + before + "\n"
            start = after
        elif end == after:
            lines += prefix + "," + after + "," + end + "\n"
            break
        else:
            lines += prefix + "," + start + "," + before + "\n"
            start = after

    return lines


if __name__ == '__main__':
    read_cal_dates("../Data/gtfs23Sept/calendar_dates.txt")
    read_cal("../Data/gtfs23Sept/calendar.txt", "../Data/gtfs23Sept/new_calendar.txt")
