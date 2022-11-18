from constans import MAX_BLOCK_SIZE, MAX_RECORD_LENGTH
from record import Record


class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        self.eof = False
        self.last_position = 0

    def read_block(self, tape):
        with open(self.filename, "r") as file:
            file.seek(self.last_position)
            while tape.block.current_size < MAX_BLOCK_SIZE:
                record_line = file.readline()
                if record_line:
                    record = Record()
                    record.deserialize(record_line)
                    tape.add_record(record)
                    self.last_position = file.tell()
                else:
                    self.eof = True
                    break

    # @staticmethod
    # def convert_record(record_line):
    #     record_line_split = record_line.split()
    #     record = Record()
    #
    #     for item in record_line_split:
    #         if item != "None":
    #             record.add(int(item))
    #         else:
    #             break
    #
    #     return record

    def write_block(self, tape):
        with open(self.filename, "a") as file:
            file.write(tape.block.serialize())
            tape.block.clear()
