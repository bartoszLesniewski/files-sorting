import os
from constans import MAX_BLOCK_SIZE


class DiskOperationsHandler:
    """The class representing a handler of disk operations."""
    # static variables common to all objects of this class
    number_of_reads = 0
    number_of_writes = 0
    count = True

    def __init__(self, filename):
        """
        Initializes DiskOperationHandler object.

        :param filename: The name of the file (tape) to read/write blocks with records.
        :type filename: str
        """
        self.filename = filename
        open(filename, "w").close()  # create an empty file or overwrite file if it already exists
        self.eof = False
        self.last_position = 0
        self.filesize = os.path.getsize(filename)

    def read_block(self, tape):
        """
        Reads a block of records from a file and saves them to the tape.

        :param tape: Tape on which records are saved.
        :type tape: Tape
        """
        # read = False
        with open(self.filename, "r") as file:
            file.seek(self.last_position)
            while tape.block.current_size < MAX_BLOCK_SIZE:
                record_line = file.readline()
                tape.add_record(record_line)
                self.last_position = file.tell()

                if self.last_position == self.filesize:
                    self.eof = True
                    break

            if self.count:
                DiskOperationsHandler.number_of_reads += 1

            #     if self.last_position == self.filesize:
            #         self.eof = True
            #         break
            #     else:
            #         record_line = file.readline()
            #         record = Record()
            #         record.deserialize(record_line)
            #         tape.add_record(record)
            #         self.last_position = file.tell()
            #         read = True
            #
            # if read:
            #     DiskOperationsHandler.number_of_reads += 1

    def write_block(self, tape):
        """
        Writes a block of record from the tape to a file.

        :param tape: The tape object from which a block is written to a file.
        :type tape: Tape
        """
        with open(self.filename, "a") as file:
            if self.filesize == 0:
                file.write(tape.block.serialize())
            else:
                file.write("\n" + tape.block.serialize())

            tape.block.clear()

        self.filesize = os.path.getsize(self.filename)

        if self.count:
            DiskOperationsHandler.number_of_writes += 1

    def reset(self):
        """
        Resets the parameters of the processed file and clears its contents.
        """
        self.make_file_readable()
        self.filesize = 0
        open(self.filename, "w").close()

    def make_file_readable(self):
        """
        Sets the end-of-file flag to false and the last read position to 0 (beginning of file),
        making the file readable.
        """
        self.eof = False
        self.last_position = 0

    # @staticmethod
    # def reset_counters():
    #     DiskOperationsHandler.number_of_reads = 0
    #     DiskOperationsHandler.number_of_writes = 0

    @staticmethod
    def enable_counting():
        """
        Enables counting of reads and writes operations.
        """
        DiskOperationsHandler.count = True

    @staticmethod
    def disable_counting():
        """
        Disables counting of reads and writes operations.
        """
        DiskOperationsHandler.count = False
