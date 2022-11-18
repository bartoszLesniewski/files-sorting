from tape import Tape


class FileSorter:
    def __init__(self, initial_filename):
        self.initial_filename = initial_filename
        self.tape1 = Tape("tape1.txt")
        self.tape2 = Tape("tape2.txt")
        self.tape3 = Tape("tape3.txt")
        self.next_tape = self.tape2

    def copy_initial_file(self):
        with open(self.initial_filename, "r") as initial_file, open("tape1.txt", "w") as tape_file:
            for line in initial_file:
                tape_file.write(line)

    def sort(self):
        self.copy_initial_file()

        while not self.tape1.fileHandler.eof:
            self.tape1.read_block_from_file()
            self.distribution()

        self.flush_tapes()
        pass

    def distribution(self):
        while self.tape1.block.current_size > 0:
            record = self.tape1.fetch_record()

            if self.next_tape.block.current_size > 0 and self.next_tape.block.records[-1] > record:
                self.next_tape = self.tape2 if self.next_tape == self.tape3 else self.tape3

            self.next_tape.add_record(record)

    def flush_tapes(self):
        if not self.tape2.block.is_empty():
            self.tape2.save_block_to_file()
        if not self.tape3.block.is_empty():
            self.tape3.save_block_to_file()
