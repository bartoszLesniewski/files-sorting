from constans import MAX_RECORD_LENGTH


class Record:
    def __init__(self, numbers=None):
        self.numbers = [] if numbers is None else numbers
        self.tmp_sum = 0

    def deserialize(self, serialized_record):
        serialized_record = serialized_record.split()

        for item in serialized_record:
            if item != "None":
                self.numbers.append(int(item))
            else:
                break

    def serialize(self):
        elements_to_serialize = [self.numbers[i] if i < len(self.numbers) else "None" for i in range(MAX_RECORD_LENGTH)]
        serialized_record = " ".join(map(str, elements_to_serialize))

        return serialized_record

    def get_sum(self):
        # return sum(self.numbers)
        return self.numbers[0]

    def __lt__(self, other):
        if other is None:
            return False

        return self.get_sum() < other.get_sum()

    def __le__(self, other):
        if other is None:
            return False

        return self.get_sum() <= other.get_sum()

    def __gt__(self, other):
        if other is None:
            return True

        return self.get_sum() > other.get_sum()

    def __ge__(self, other):
        if other is None:
            return True

        return self.get_sum() >= other.get_sum()

    def __eq__(self, other):
        if other is None:
            return False

        return self.get_sum() == other.get_sum()

    def print(self):
        # for number in self.numbers:
        #     print(number, end=" ")
        for i in range(MAX_RECORD_LENGTH):
            if i < len(self.numbers):
                print(self.numbers[i], end=" ")
            else:
                print("None", end=" ")
