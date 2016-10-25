#!/usr/bin/python3
import csv
import os

from sys import argv


def convert_time(raw_time):
    seconds = float(raw_time)
    if seconds < 60:
        return "%ds" % seconds
    return "%dm%ds" % (seconds // 60, seconds % 60)


def compute_cpu(sys_t_raw, usr_t_raw, wall_t_raw):
    sys_t = float(sys_t_raw)
    usr_t = float(usr_t_raw)
    wall_t = float(wall_t_raw)
    return "%.2f" % (((sys_t + usr_t) / wall_t) * 100)

if __name__ == "__main__":
    raw_data_path = argv[1]
    output_file = argv[2]
    if not os.path.exists(raw_data_path):
        print("Path \"{}\" does not exist!".format(raw_data_path))
        exit(1)

    with open(raw_data_path, newline='') as f:
        reader = csv.DictReader(f)
        with open(output_file, "w") as out:
            out.write("subject,system_t,user_t,elapsed_t,elapsed_t_debug,cpu_usage")
            out.write("\n")
            for row in reader:
                if not row["tests"] == "0":
                    elapsed_t_debug = convert_time(row["elapsed_t"])
                    sys_t = row["system_t"]
                    usr_t = row["user_t"]
                    wall_t = row["elapsed_t"]
                    cpu_usage = compute_cpu(sys_t, usr_t, wall_t)

                    columns = [row["subject"], sys_t, usr_t, wall_t,
                               elapsed_t_debug, cpu_usage]

                    out.write(",".join(columns))
                    out.write("\n")

