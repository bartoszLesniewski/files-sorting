import random
MAX_RECORD_LENGTH = 15
MIN_NUMBER = -100
MAX_NUMBER = 100


def generate_records() -> list[list[int]]:
    records = []
    number_of_records = 40

    while number_of_records:
        record_length = random.randint(1, MAX_RECORD_LENGTH)
        records.append(rand_record(record_length))
        number_of_records -= 1

    return records


def rand_record(record_length) -> list[int]:
    numbers = []
    while record_length:
        numbers.append(random.randint(MIN_NUMBER, MAX_NUMBER))
        record_length -= 1

    return numbers


def main() -> None:
    records = generate_records()
    for record in records:
        print(record)


if __name__ == "__main__":
    main()
