import matplotlib.pyplot as plt

from diskOperationsHandler import DiskOperationsHandler
from fileSorter import FileSorter
from records_generator import generate_random_records
from tape import Tape

numbers_of_records = [10, 20, 50, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000]
all_statistics = {}


def generate_test_files():
    for number_of_records in numbers_of_records:
        generate_random_records(Tape(f"experiment/test_files/test_{number_of_records}.txt"), number_of_records)


def collect_results():
    for number_of_records in numbers_of_records:
        DiskOperationsHandler.reset_counters()
        sorter = FileSorter(tape1_filename=f"experiment/results_files/results_{number_of_records}.txt",
                            tape2_filename="experiment/results_files/tape2.txt",
                            tape3_filename="experiment/results_files/tape3.txt",
                            experiment_input_filename=f"experiment/test_files/test_{number_of_records}.txt")
        statistics = sorter.run_for_experiment()
        all_statistics[number_of_records] = statistics

    generate_plots()


def generate_plots():
    generate_phase_plot()
    generate_disk_operations_plot()


def generate_phase_plot():
    plt.figure(figsize=(10, 5))
    plt.plot(numbers_of_records, [stat["number of phases"] for _, stat in all_statistics.items()],
             label="Uzyskana liczba faz", color="red", linewidth=4)
    plt.plot(numbers_of_records, [stat["worst number of phases"] for _, stat in all_statistics.items()],
             label="Liczba faz w najgorszym przypadku", color="green", linewidth=4)
    plt.plot(numbers_of_records, [stat["average number of phases"] for _, stat in all_statistics.items()],
             label="Liczba faz w średnim przypadku", color="blue", linestyle="dashed")
    plt.title("Liczba faz w zależności od liczby rekordów", fontweight="bold")
    plt.xlabel("Liczba rekordów")
    plt.ylabel("Liczba faz")
    plt.legend()
    plt.grid()
    plt.savefig('fazy.png', dpi=600)
    plt.show()


def generate_disk_operations_plot():
    plt.figure(figsize=(10, 5))
    plt.plot(numbers_of_records, [stat["total number of rw"] for _, stat in all_statistics.items()],
             label="Uzyskana liczba operacji dyskowych", color="red", linewidth=4)
    plt.plot(numbers_of_records, [stat["worst number of rw"] for _, stat in all_statistics.items()],
             label="Liczba operacji dyskowych w najgorszym przypadku", color="green", linewidth=4)
    plt.plot(numbers_of_records, [stat["average number of rw"] for _, stat in all_statistics.items()],
             label="Liczba operacji dyskowych w średnim przypadku", color="blue", linestyle="dashed")
    plt.title("Liczba operacji dyskowych w zależności od liczby rekordów", fontweight="bold")
    plt.xlabel("Liczba rekordów")
    plt.ylabel("Liczba operacji dyskowych")
    plt.legend()
    plt.grid()
    plt.savefig('operacje.png', dpi=600)
    plt.show()


def run_experiment():
    choice = input("Do you want to generate test files with random records? [y/n]: ")
    if choice == "y":
        generate_test_files()

    collect_results()


run_experiment()
