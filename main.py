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


def main() -> None:
    records = generate_records()
    for record in records:
        print(record)

    save_records(records)


if __name__ == "__main__":
    main()
