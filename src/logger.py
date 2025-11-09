import csv
import datetime

def log_to_csv(filename, event):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().isoformat(), event])
