import os
from constans import MAX_BLOCK_SIZE
from record import Record


class DiskOperationsHandler:
    number_of_reads = 0
    number_of_writes = 0

    def __init__(self, filename):
        self.filename = filename
        open(filename, "w").close()  # create an empty file or overwrite file if it already exists
        self.eof = False
        self.last_position = 0
        self.filesize = os.path.getsize(filename)

    def read_block(self, tape):
        with open(self.filename, "r") as file:
            file.seek(self.last_position)
            while tape.block.current_size < MAX_BLOCK_SIZE:
                if self.last_position == self.filesize:
                    self.eof = True
                    break
                else:
                    record_line = file.readline()
                    # if record_line:
                    record = Record()
                    record.deserialize(record_line)
                    tape.add_record(record)
                    self.last_position = file.tell()
                # else:
                #     self.eof = True
                #     break
            DiskOperationsHandler.number_of_reads += 1

    def write_block(self, tape):
        with open(self.filename, "a") as file:
            if self.filesize == 0:
                file.write(tape.block.serialize())
            else:
                file.write("\n" + tape.block.serialize())

            tape.block.clear()

        self.filesize = os.path.getsize(self.filename)
        DiskOperationsHandler.number_of_writes += 1

    def reset(self):
        self.eof = False
        self.last_position = 0
        self.filesize = 0
        open(self.filename, "w").close()

    def update_filesize(self):
        self.filesize = os.path.getsize(self.filename)

    @staticmethod
    def reset_counters():
        DiskOperationsHandler.number_of_reads = 0
        DiskOperationsHandler.number_of_writes = 0
