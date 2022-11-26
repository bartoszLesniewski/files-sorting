import random
from constans import MAX_RECORD_LENGTH, MIN_NUMBER, MAX_NUMBER
from diskOperationsHandler import DiskOperationsHandler
from record import Record


def generate_random_records(tape, number_of_records):
    """
    Generates random records and writes them to the tape.

    :param tape: Tape on which records are saved.
    :type tape: Tape
    :param number_of_records: Number of records to rand.
    :type number_of_records: int
    """
    DiskOperationsHandler.disable_counting()
    while number_of_records:
        record_length = random.randint(1, MAX_RECORD_LENGTH)
        tape.add_record(Record(rand_record(record_length)))
        number_of_records -= 1

    tape.flush()
    DiskOperationsHandler.enable_counting()


def rand_record(record_length):
    """
    Rands a record of the given length.

    :param record_length: The length of the record (set of numbers).
    :type record_length: int
    :return: A list of the given length containing random numbers.
    :rtype: list[int]
    """
    numbers = []
    while record_length:
        numbers.append(random.randint(MIN_NUMBER, MAX_NUMBER))
        record_length -= 1

    return numbers


def load_records_from_keyboard(tape, number_of_records):
    """
    Allows the user to enter records from the keyboard and save them to tape.

    :param tape: Tape on which records are saved.
    :type tape: Tape
    :param number_of_records: The number of records that the user has to enter.
    :type number_of_records: int
    """
    DiskOperationsHandler.disable_counting()
    print("TIP: As a record, enter a set of numbers (maximum 15) separated by a space.")

    for i in range(number_of_records):
        record = input(f"Please enter the {i + 1} record: ")
        tape.add_record(record)

    tape.flush()
    DiskOperationsHandler.enable_counting()


def load_records_from_test_file(test_file_name, tape):
    """
    Loads records from the specified file to the tape and returns the number of loaded records.

    :param test_file_name: The name of the file from which records should be loaded.
    :type test_file_name: str
    :param tape: Tape on which the loaded records should be saved.
    :type tape: Tape
    :return: Number of loaded records.
    :rtype: int
    """
    DiskOperationsHandler.disable_counting()
    number_of_records = 0
    with open(test_file_name, "r") as initial_file:
        while True:
            record_line = initial_file.readline()
            if record_line:
                tape.add_record(record_line)
                number_of_records += 1
            else:
                break

    tape.flush()
    DiskOperationsHandler.enable_counting()

    return number_of_records
