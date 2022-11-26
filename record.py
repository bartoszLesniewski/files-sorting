from constans import MAX_RECORD_LENGTH


class Record:
    """The class representing a record that is a set of numbers."""
    def __init__(self, numbers=None):
        """
        Initializes Record object.
        :param numbers: List of numbers that make up a record.
        :type numbers: list[int]
        """
        self.numbers = [] if numbers is None else numbers

    def deserialize(self, serialized_record):
        """
        Deserializes a record - converts a set of numbers stored as text into a list of integers,
        ignoring the null values (None) that are used to fill a record size in a file.

        :param serialized_record: Serialized record in text format.
        :type serialized_record: str
        """
        serialized_record = serialized_record.split()

        for item in serialized_record:
            if item != "None":
                self.numbers.append(int(item))
            else:
                break

    def serialize(self):
        """
        Returns a serialized record.

        :return: Serialized record.
        :rtype: str
        """
        elements_to_serialize = [self.numbers[i] if i < len(self.numbers) else "None" for i in range(MAX_RECORD_LENGTH)]
        serialized_record = " ".join(map(str, elements_to_serialize))

        return serialized_record

    def get_sum(self):
        """
        Returns the sum of numbers in a record.

        :return: Sum of numbers in a record.
        :rtype: int
        """
        return sum(self.numbers)

    def __lt__(self, other):
        """
        Overloads the '<' operator for comparing objects of record class based on the sum of numbers in a record.
        It also takes into account the situation when the object to be compared is empty (None).

        :param other: Object of record class or None.
        :type other: Record | None
        :return: True if the sum of numbers in the current object is less than the sum of numbers in
                 the other object, or the other object is None.
        :rtype: bool
        """
        if other is None:
            return False

        return self.get_sum() < other.get_sum()

    def __le__(self, other):
        """
        Overloads the '<=' operator for comparing objects of record class based on the sum of numbers in a record.
        It also takes into account the situation when the object to be compared is empty (None).

        :param other: Object of record class or None.
        :type other: Record | None
        :return: True if the sum of numbers in the current object is less than or equal to the sum of numbers in
                 the other object, or the other object is None.
        :rtype: bool
        """
        if other is None:
            return False

        return self.get_sum() <= other.get_sum()

    def __gt__(self, other):
        """
        Overloads the '>' operator for comparing objects of record class based on the sum of numbers in a record.
        It also takes into account the situation when the object to be compared is empty (None).

        :param other: Object of record class or None.
        :type other: Record | None
        :return: True if the sum of numbers in the current object is greater than the sum of numbers in
                 the other object, or the other object is None.
        :rtype: bool
        """
        if other is None:
            return True

        return self.get_sum() > other.get_sum()

    def __ge__(self, other):
        """
        Overloads the '>=' operator for comparing objects of record class based on the sum of numbers in a record.
        It also takes into account the situation when the object to be compared is empty (None).

        :param other: Object of record class or None.
        :type other: Record | None
        :return:
        :rtype:
        """
        if other is None:
            return True

        return self.get_sum() >= other.get_sum()

    def __eq__(self, other):
        """
        Overloads the '==' operator for comparing objects of record class based on the sum of numbers in a record.
        It also takes into account the situation when the object to be compared is empty (None).

        :param other: Object of record class or None.
        :type other: Record | None
        :return:
        :rtype:
        """
        if other is None:
            return False

        return self.get_sum() == other.get_sum()

    def print(self):
        """
        Prints the set of numbers stored in a record.
        """
        # for number in self.numbers:
        #     print(number, end=" ")
        for i in range(MAX_RECORD_LENGTH):
            if i < len(self.numbers):
                print(self.numbers[i], end=" ")
            else:
                print("None", end=" ")

    # def is_empty(self):
    #     return len(self.numbers) == 0
