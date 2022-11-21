import random
from constans import MAX_RECORD_LENGTH, MIN_NUMBER, MAX_NUMBER, NUMBER_OF_RECORDS


def generate_records():
    records = []
    number_of_records = NUMBER_OF_RECORDS

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
