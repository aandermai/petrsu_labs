import read_data_from_file_module
import split_data_module
import calculate_statistics_module
import print_stats_module

file = "ccsv.csv"

lines = read_data_from_file_module.read_data_from_file(file)
splitdata = split_data_module.split_data(lines, 300)
stats = calculate_statistics_module.calculate_statistics(splitdata)
n = int(input("Какой сегмент вывести?\nЕсли хотите вывести все, то напишите 0\n")) - 1
print_stats_module.print_stats(stats, n)
