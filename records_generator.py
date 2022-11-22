import random
from constans import MAX_RECORD_LENGTH, MIN_NUMBER, MAX_NUMBER
from diskOperationsHandler import DiskOperationsHandler
from record import Record


def generate_random_records(tape, number_of_records=1000):
    while number_of_records:
        record_length = random.randint(1, MAX_RECORD_LENGTH)
        tape.add_record(Record(rand_record(record_length)))
        number_of_records -= 1

    tape.flush()
    DiskOperationsHandler.reset_counters()


def rand_record(record_length):
    numbers = []
    while record_length:
        numbers.append(random.randint(MIN_NUMBER, MAX_NUMBER))
        record_length -= 1

    return numbers


def load_records_from_keyboard(tape):
    pass


def load_records_from_test_file(test_file_name, tape):
    with open(test_file_name, "r") as initial_file, open(tape.fileHandler.filename, "w") as tape_file:
        for line in initial_file:
            tape_file.write(line)

    tape.fileHandler.update_filesize()
