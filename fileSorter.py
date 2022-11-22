from records_generator import generate_random_records, load_records_from_keyboard, load_records_from_test_file
from tape import Tape


class FileSorter:
    def __init__(self):
        self.tape1 = Tape("tape1.txt")
        self.tape2 = Tape("tape2.txt")
        self.tape3 = Tape("tape3.txt")
        self.next_tape = self.tape2
        self.file_sorted = False
        self.number_of_phases = 0

    def run(self):
        self.display_main_menu()
        program_exit = self.choose_menu_option()
        if not program_exit:
            self.sort()

    @staticmethod
    def display_main_menu():
        print("======= DATABASE STRUCTURES - PROJECT 1: FILE SORTING =======")
        print("================ Bartosz Lesniewski,  184783 ================")
        print("1. Generate random records.")
        print("2. Load records using keyboard.")
        print("3. Load test data from file.")
        print("4. Exit.")

    def choose_menu_option(self):
        program_exit = False
        option_number = input("Please enter an option number: ")

        if option_number == "1":
            generate_random_records(self.tape1)
        elif option_number == "2":
            load_records_from_keyboard(self.tape1)
        elif option_number == "3":
            test_file_name = input("Please enter a test file name: ")
            load_records_from_test_file(test_file_name, self.tape1)
        elif option_number == "4":
            program_exit = True
        else:
            print("Incorrect option.")
            program_exit = True

        return program_exit

    def sort(self):
        while not self.file_sorted:
            self.distribute()
            self.merge()
            self.next_tape = self.tape2
            self.number_of_phases += 1
        pass

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
            tape.flush()

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
