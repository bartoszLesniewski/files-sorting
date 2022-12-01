import math
from tabulate import tabulate

from constans import b
from diskOperationsHandler import DiskOperationsHandler
from enums import *
from records_generator import generate_random_records, load_records_from_keyboard, load_records_from_test_file
from tape import Tape


class FileSorter:
    """The class which handles all operations related to sorting a file."""
    def __init__(self, tape1_filename="tape1.txt", tape2_filename="tape2.txt", tape3_filename="tape3.txt",
                 experiment_input_filename=None):
        """
        Initializes FileSorter object which is responsible for the entire sorting process.
        """
        self.tape1 = Tape(tape1_filename)
        self.tape2 = Tape(tape2_filename)
        self.tape3 = Tape(tape3_filename)
        self.next_tape = self.tape2
        self.file_sorted = False
        self.number_of_phases = 0
        self.number_of_records = 0
        self.mode = None
        self.experiment_input_filename = experiment_input_filename

    def run(self):
        """
        Displays menu and runs sorting if required data has been loaded.
        :rtype: None
        """
        self.display_main_menu()
        program_exit = self.choose_menu_option()
        if not program_exit:
            self.choose_mode()
            self.print_file(PrintStage.BEFORE_SORTING)
            self.natural_merge_sort()
            self.print_file(PrintStage.AFTER_SORTING)
            self.show_statistics()

    @staticmethod
    def display_main_menu():
        """
        Displays main menu with options which the user can select.
        """
        print("======= DATABASE STRUCTURES - PROJECT 1: FILE SORTING =======")
        print("================ Bartosz Lesniewski,  184783 ================")
        print("1. Generate random records.")
        print("2. Load records using keyboard.")
        print("3. Load test data from file.")
        print("4. Exit.")

    def choose_menu_option(self):
        """
        Asks the user to choose an option and performs the action associated with it.
        :return: Specifies whether the program should end or continue running.
        :rtype: bool
        """
        program_exit = False
        option_number = int(input("Please enter an option number: "))

        if option_number == MainMenuOptions.RANDOM_RECORDS.value:
            self.choose_number_of_records()
            generate_random_records(self.tape1, self.number_of_records)
        elif option_number == MainMenuOptions.KEYBOARD.value:
            self.choose_number_of_records()
            load_records_from_keyboard(self.tape1, self.number_of_records)
        elif option_number == MainMenuOptions.FILE.value:
            test_file_name = input("Please enter a test file name: ")
            self.number_of_records = load_records_from_test_file(test_file_name, self.tape1)
        elif option_number == MainMenuOptions.EXIT.value:
            program_exit = True
        else:
            print("Invalid option.")
            program_exit = True

        return program_exit

    def choose_number_of_records(self):
        """
        Asks the user to enter a number of records and stores it in the appropriate class field.
        :rtype: None
        """
        self.number_of_records = int(input("How many records do you want to generate? "))

    def choose_mode(self):
        """
        Asks the user to select a file display mode.
        """
        print("-------------- MODE SELECTION --------------")
        print("1. Verbose mode with printing entire records.")
        print("2. Verbose mode with printing the sorting criterion (sum of numbers in the record).")
        print("3. Non verbose mode (without additional messages).")
        selected_mode = int(input("Choose the mode of printing the message after each phase: "))

        if selected_mode == Mode.VERBOSE_RECORDS.value:
            self.mode = Mode.VERBOSE_RECORDS
        elif selected_mode == Mode.VERBOSE_SUM.value:
            self.mode = Mode.VERBOSE_SUM
        elif selected_mode == Mode.NON_VERBOSE:
            self.mode = Mode.NON_VERBOSE
        else:
            print("Invalid option!")
            self.mode = Mode.NON_VERBOSE

    def natural_merge_sort(self):
        """
        Invokes successive sorting phases (which consist of distribution and merging) until the file is sorted
        and counts them.
        """
        while not self.file_sorted and self.number_of_records > 1:
            self.distribute()
            self.merge()
            self.next_tape = self.tape2
            self.number_of_phases += 1
            if self.mode != Mode.NON_VERBOSE:
                self.print_file(PrintStage.AFTER_PHASE)

        pass

    def distribute(self):
        """
        Alternately distributes runs from tape 1 to tapes 2 and 3.
        """
        while True:
            record = self.tape1.fetch_record()
            if record is None:
                break
            else:
                if self.next_tape.block.current_size > 0 and self.next_tape.block.records[-1] > record:
                    self.next_tape = self.tape2 if self.next_tape == self.tape3 else self.tape3

                self.next_tape.add_record(record)

        # if the blocks are not completely filled, they are still in memory, so we need to flush them to a file
        self.flush_tapes(self.tape2, self.tape3)

        # in case the input file was already sorted we do not need to do anything else
        if self.tape2.fileHandler.filesize == 0 or self.tape3.fileHandler.filesize == 0:
            self.file_sorted = True

    def merge(self):
        """
        Merges runs created "on the fly" from tape 2 and 3 and writes them to tape 1.
        """
        # It the input file was already sorted, it will be detected during distribution so there is no need to merge
        if not self.file_sorted:
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
                    # if tape 2 has finished, the run from tape 3 has no run to merge with,
                    # so just rewrite records it
                    if tape2_record is None:
                        self.tape1.add_record(tape3_record)
                        tape3_last_record = tape3_record
                        tape3_record = None
                    # if tape 3 has finished, the run from tape 2 has no run to merge with,
                    # so just rewrite record from it
                    elif tape3_record is None:
                        self.tape1.add_record(tape2_record)
                        tape2_last_record = tape2_record
                        tape2_record = None
                    else:
                        # 1. If there are records from the previous run left on tape 2, write them to tape 1
                        # 2. If the matching runs on tape 2 and tape 3 are currently being processed
                        # and the record from tape 2 is smaller, write it to tape 1
                        if (tape2_runs_counter < tape3_runs_counter or
                           tape2_record <= tape3_record and tape2_runs_counter == tape3_runs_counter):
                            self.tape1.add_record(tape2_record)
                            tape2_last_record = tape2_record
                            tape2_record = None
                        # 1. If there are records from the previous run left on tape 3, write them to tape 1
                        # 2. If the matching runs on tape 2 and tape 3 are currently being processed
                        # and the record from tape 3 is smaller, write it to tape 1
                        elif (tape3_runs_counter < tape2_runs_counter or
                              tape3_record < tape2_record and tape2_runs_counter == tape3_runs_counter):
                            self.tape1.add_record(tape3_record)
                            tape3_last_record = tape3_record
                            tape3_record = None
                        # It should not occur - delete after tests
                        else:
                            print("Unhandled condition occurred!")

            self.flush_tapes(self.tape1)
            self.clear_tapes(self.tape2, self.tape3)

            # If the total number of runs on both tapes does not exceed 2, then the file is sorted.
            # (merging one run from tape 2 with one run from tape 3 produces one sorted run)
            if tape2_runs_counter + tape3_runs_counter <= 2:
                self.file_sorted = True

    @staticmethod
    def flush_tapes(*args):
        """
        Flushes the blocks of all passed tapes.

        :param args: A variable number of arguments - tapes whose blocks need to be flushed.
        :type args: Tape
        """
        for tape in args:
            tape.flush()

    @staticmethod
    def clear_tapes(*args):
        """
        Clears all tapes passed as arguments.

        :param args: A variable number of arguments - tapes to be cleared.
        :type args: Tape
        """
        for tape in args:
            tape.clear()

    @staticmethod
    def update_numbers_of_runs(current_record, last_record, counter):
        """
        Compares the current record with the previous one to detect if it starts a new run.

        :param current_record: The currently fetched record from the specific tape.
        :type current_record: Record
        :param last_record: The last processed record from the specific tape.
        :type last_record: Record
        :param counter: Runs counter for a specific tape.
        :type counter: int
        :return: Updated values of the last record and the runs counter.
        :rtype: tuple
        """
        if current_record is not None:
            if last_record > current_record or counter == 0:
                counter += 1
                last_record = None  # to avoid incrementing counter in the next iteration under the same condition

        return last_record, counter

    def show_statistics(self):
        """
        Prints the table comparing the calculated values of the number of reads and writes and the number of phases
        with the theoretical values.
        """
        theoretical_values = self.calculate_theoretical_values()

        headers = ["Parameter", "Real value", "Worst value", "Average value"]
        table = [["Number of reads and writes (reads + writes)",
                  f"{DiskOperationsHandler.number_of_reads + DiskOperationsHandler.number_of_writes} "
                  f"({DiskOperationsHandler.number_of_reads} + {DiskOperationsHandler.number_of_writes})",
                  theoretical_values["worst number of rw"], theoretical_values["average number of rw"]],
                 ["Number of phases", self.number_of_phases, theoretical_values["worst number of phases"],
                  theoretical_values["average number of phases"]]]

        print(f"\nStatistics for {self.number_of_records} records:")
        print(tabulate(table, headers, tablefmt="pretty"))

    def calculate_theoretical_values(self):
        """
        Calculates theoretical values of the number of reads and writes and the number of phases
        in the worst and average cases.

        :return: The above-mentioned theoretical values.
        :rtype: dict
        """
        worst_number_of_phases = math.ceil(math.log(self.number_of_records, 2))
        worst_number_of_rw = (4 * self.number_of_records * worst_number_of_phases) / b

        average_number_of_phases = math.ceil(math.log(self.number_of_records / 2, 2))
        average_number_of_rw = (4 * self.number_of_records * average_number_of_phases) / b
        theoretical_values = {"worst number of phases": worst_number_of_phases,
                              "worst number of rw": worst_number_of_rw,
                              "average number of phases": average_number_of_phases,
                              "average number of rw": average_number_of_rw}

        return theoretical_values

    def get_statistics(self):
        """
        Returns statistics (only used for the experiment).

        :return: Statistics containing calculated theoretical values and obtained values.
        :rtype: dict
        """
        statistics = self.calculate_theoretical_values()
        statistics.update({"number of reads": DiskOperationsHandler.number_of_reads,
                           "number of writes": DiskOperationsHandler.number_of_writes,
                           "total number of rw": DiskOperationsHandler.number_of_reads +
                           DiskOperationsHandler.number_of_writes,
                           "number of phases": self.number_of_phases})

        return statistics

    def print_file(self, print_stage):
        """
        Prints the content of the file (records) after a specific stage, i.e. before sorting, after sorting
        or after a specific phase.

        :param print_stage: The stage after which the file is printed (only used to display appropriate information)
        :type print_stage: PrintStage
        """
        DiskOperationsHandler.disable_counting()
        print("\n---------- File "
              f"{print_stage.value} "
              f'{str(self.number_of_phases) + " " if print_stage == PrintStage.AFTER_PHASE else ""}'
              "----------")

        while True:
            record = self.tape1.fetch_record()
            if record is None:
                break
            else:
                if self.mode == Mode.VERBOSE_RECORDS or \
                   print_stage == PrintStage.BEFORE_SORTING or \
                   print_stage == PrintStage.AFTER_SORTING:
                    record.print()
                    print()
                else:
                    print(record.get_sum())

        DiskOperationsHandler.enable_counting()
        self.tape1.fileHandler.make_file_readable()

    def run_for_experiment(self):
        """
        Runs the sorting program for the experiment, i.e. bypassing the menu, loading records from the file
        generated for the experiment

        :return: Statistics generated for the experiment file.
        :rtype: dict
        """
        self.number_of_records = load_records_from_test_file(self.experiment_input_filename, self.tape1)
        self.mode = Mode.NON_VERBOSE
        self.natural_merge_sort()
        self.show_statistics()
        statistics = self.get_statistics()

        return statistics
