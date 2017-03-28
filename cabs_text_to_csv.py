import csv
import glob

csv_file = r"cabsdata.csv"
cab_id = 1
with open(csv_file, 'w') as out_file:
     out_csv = csv.writer(open(csv_file, 'wb'))
     for fname in glob.glob('Datasets\\cabspottingdata\\*.txt'):
            with open(fname) as f:
                in_txt = csv.reader(open(f.name, "rb"), delimiter = ' ')
                for row in in_txt:
                    row = [str(cab_id)] + row
                    out_csv.writerow(row)
            cab_id += 1