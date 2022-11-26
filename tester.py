import random
import os

from diskOperationsHandler import DiskOperationsHandler
from fileSorter import FileSorter
from records_generator import generate_random_records, load_records_from_test_file
from tape import Tape


def generate_test_files(number_of_tests):
    for i in range(number_of_tests):
        number_of_records = random.randint(1, 100)
        tape = Tape(f"tests/test{i+1}.txt")
        generate_random_records(tape, number_of_records)


def run_tests():
    for file in os.listdir("tests"):
        if "result" not in file:
            DiskOperationsHandler.number_of_reads = 0
            DiskOperationsHandler.number_of_writes = 0
            normal_sorted_records = normal_sorting("tests/" + file)
            sorter = FileSorter("tests/result_" + file)
            sorter.number_of_records = len(normal_sorted_records)
            load_records_from_test_file("tests/" + file, sorter.tape1)
            sorter.natural_merge_sort()
            natural_sorted_records = get_records("tests/result_" + file)
            compare_results(natural_sorted_records, normal_sorted_records, file)
            sorter.show_statistics()


def normal_sorting(filename):
    records = get_records(filename)
    records.sort(key=lambda x: x[0])
    return records


def get_records(filename):
    records = []
    with open(filename, "r") as file:
        for record_line in file.readlines():
            str_record = record_line.split()
            record = []

            for item in str_record:
                if item != "None":
                    record.append(int(item))
                else:
                    break

            records.append(record)

    return records


def compare_results(natural_sorting, normal_sorting, file):
    # print(f"Checking {file}")
    if len(natural_sorting) != len(normal_sorting):
        print("Different lengths of sorted lists!")
    else:
        for i in range(len(natural_sorting)):
            if natural_sorting[i][0] != normal_sorting[i][0]:
                print(f"Different order detected in line {i}!")
                print("result file: " + str(natural_sorting[i]))
                print("normal sorting: " + str(normal_sorting[i]))


if __name__ == "__main__":
    # number_of_tests = int(input("How many tests do you want to generate? "))
    # generate_test_files(number_of_tests)
    run_tests()
