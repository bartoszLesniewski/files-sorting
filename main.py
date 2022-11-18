import random

from constans import *
from tape import Tape

next_tape = None  # it needs to be fixed


def generate_records():
    records = []
    number_of_records = 40

    while number_of_records:
        record_length = random.randint(1, MAX_RECORD_LENGTH)
        records.append(rand_record(record_length))
        number_of_records -= 1

    return records


def rand_record(record_length):
    numbers = []
    while record_length:
        numbers.append(random.randint(MIN_NUMBER, MAX_NUMBER))
        record_length -= 1

    return numbers


def save_records(records):
    with open("data.txt", "w") as file:
        for index, record in enumerate(records):
            for i in range(MAX_RECORD_LENGTH):
                if i < len(record):
                    file.write(str(record[i]))
                else:
                    file.write("None")

                if i != MAX_RECORD_LENGTH - 1:
                    file.write(" ")

            if index < len(records) - 1:
                file.write("\n")


def read_file2():
    # reader = FileHandler("data.txt")
    tape1 = Tape("tape1.txt")
    tape2 = Tape("tape2.txt")
    distribution.next_tape = tape2
    tape3 = Tape("tape3.txt")
    copy_initial_file()

    while not tape1.fileHandler.eof:
        tape1.read_from_file()
        distribution(tape1, tape2, tape3)

    pass


def copy_initial_file():
    with open("data.txt", "r") as initial_file, open("tape1.txt", "w") as tape_file:
        for line in initial_file:
            tape_file.write(line)


def distribution(tape1, tape2, tape3):
    # next_tape = tape2
    while tape1.block.current_size > 0:
        record = tape1.fetch_record()

        if distribution.next_tape.block.current_size > 0 and distribution.next_tape.block.records[-1] > record:
            distribution.next_tape = tape2 if distribution.next_tape == tape3 else tape3

        distribution.next_tape.add_record(record)


distribution.next_tape = None


def main() -> None:
    # records= generate_records()
    # save_records(records)
    read_file2()


if __name__ == "__main__":
    main()
