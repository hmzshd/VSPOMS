import csv

with open("demo.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print(', '.join(row))
