from tape import Tape


class FileSorter:
    def __init__(self, initial_filename):
        self.initial_filename = initial_filename
        self.tape1 = Tape("tape1.txt")
        self.tape2 = Tape("tape2.txt")
        self.tape3 = Tape("tape3.txt")
        self.next_tape = self.tape2
        self.file_sorted = False

    def sort(self):
        self.copy_initial_file()
        while not self.file_sorted:
            self.distribute()
            self.merge()
            self.next_tape = self.tape2

    def copy_initial_file(self):
        with open(self.initial_filename, "r") as initial_file, open("tape1.txt", "w") as tape_file:
            for line in initial_file:
                tape_file.write(line)

    def distribute(self):
        while True:
            record = self.tape1.fetch_record()
            if record is None:
                break
            else:
                if self.next_tape.block.current_size > 0 and self.next_tape.block.records[-1] > record:
                    self.next_tape = self.tape2 if self.next_tape == self.tape3 else self.tape3

                self.next_tape.add_record(record)

        self.flush_tapes(self.tape2, self.tape3)

    def merge(self):
        self.tape1.clear()
        tape2_record, tape2_last_record = None, None
        tape3_record, tape3_last_record = None, None
        tape2_runs_counter, tape3_runs_counter = 0, 0

        while True:
            # Already merged record is marked as None.
            # If record is not merged yet, it will be used in the next iteration.
            tape2_record = self.tape2.fetch_record() if tape2_record is None else tape2_record
            tape3_record = self.tape3.fetch_record() if tape3_record is None else tape3_record

            tape2_last_record, tape2_runs_counter = self.update_numbers_of_runs(tape2_record,
                                                                                tape2_last_record,
                                                                                tape2_runs_counter)
            tape3_last_record, tape3_runs_counter = self.update_numbers_of_runs(tape3_record,
                                                                                tape3_last_record,
                                                                                tape3_runs_counter)

            if tape2_record is None and tape3_record is None:
                break
            else:
                if tape2_record is None:
                    self.tape1.add_record(tape3_record)
                    tape3_last_record = tape3_record
                    tape3_record = None
                elif tape3_record is None:
                    self.tape1.add_record(tape2_record)
                    tape2_last_record = tape2_record
                    tape2_record = None
                else:
                    if (tape2_runs_counter < tape3_runs_counter or
                       tape2_record <= tape3_record and tape2_runs_counter == tape3_runs_counter):
                        self.tape1.add_record(tape2_record)
                        tape2_last_record = tape2_record
                        tape2_record = None
                    elif (tape3_runs_counter < tape2_runs_counter or
                          tape3_record < tape2_record and tape2_runs_counter == tape3_runs_counter):
                        self.tape1.add_record(tape3_record)
                        tape3_last_record = tape3_record
                        tape3_record = None
                    else:
                        print("Unhandled condition occurred!")

        self.flush_tapes(self.tape1)
        self.clear_tapes(self.tape2, self.tape3)

        if tape2_runs_counter + tape3_runs_counter <= 2:
            self.file_sorted = True

    @staticmethod
    def flush_tapes(*args):
        for tape in args:
            if not tape.block.is_empty():
                tape.save_block_to_file()

    @staticmethod
    def clear_tapes(*args):
        for tape in args:
            tape.clear()

    @staticmethod
    def update_numbers_of_runs(current_record, last_record, counter):
        if current_record is not None:
            if last_record > current_record or counter == 0:
                counter += 1
                last_record = None  # to avoid incrementing counter in the next iteration under the same condition

        return last_record, counter
