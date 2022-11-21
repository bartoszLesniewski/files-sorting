import math

from constans import NUMBER_OF_RECORDS, RECORD_SIZE, MAX_BLOCK_SIZE
from diskOperationsHandler import DiskOperationsHandler
from fileSorter import FileSorter
from tabulate import tabulate

from records_generator import generate_random_records


def main():
    sorter = FileSorter()
    sorter.run()
    show_statistics(sorter)


def show_statistics(sorter):
    b = MAX_BLOCK_SIZE / RECORD_SIZE
    worst_number_of_phases = math.ceil(math.log(NUMBER_OF_RECORDS, 2))
    worst_number_of_rw = (4 * NUMBER_OF_RECORDS * worst_number_of_phases) / b

    average_number_of_phases = math.ceil(math.log(NUMBER_OF_RECORDS/2, 2))
    average_number_of_rw = (4 * NUMBER_OF_RECORDS * average_number_of_phases) / b

    headers = ["Parameter", "Achieved value", "Worst value", "Average value"]
    table = [["Number of reads", DiskOperationsHandler.number_of_reads, worst_number_of_rw, average_number_of_rw],
             ["Number of writes", DiskOperationsHandler.number_of_writes, worst_number_of_rw, average_number_of_rw],
             ["Number of phases", sorter.number_of_phases, worst_number_of_phases, average_number_of_phases]]

    print(tabulate(table, headers, tablefmt="pretty"))


if __name__ == "__main__":
    main()
