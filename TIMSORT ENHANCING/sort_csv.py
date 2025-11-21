import csv
import time
from enhanced_timsort import EnhancedTimsort

def sort_csv(file_path, output_path=None, reverse=False):
    """
    Sort the CSV file using EnhancedTimsort.
    Assumes the CSV has a header and one column of integers.
    """
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                data.append(int(row[0]))

    print(f"Loaded {len(data)} values from {file_path}")

    sorter = EnhancedTimsort(data)
    start_time = time.time()
    sorted_data = sorter.sort(reverse=reverse)
    end_time = time.time()

    print(f"Sorting took {end_time - start_time:.4f} seconds")

    if output_path is None:
        output_path = file_path.replace('.csv', '_sorted.csv')

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for value in sorted_data:
            writer.writerow([value])

    print(f"Sorted data saved to {output_path}")

if __name__ == "__main__":
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'timsort_dataset_500k.csv')
    sort_csv(file_path, reverse=False)
