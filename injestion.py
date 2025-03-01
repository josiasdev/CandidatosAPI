import zipfile
import csv
import io

ZIP_PATH = 'resources/Acidentes_DadosAbertos_20230912.csv.zip'
CSV_FILENAME = 'Acidentes_DadosAbertos_20230912.csv'  # File inside ZIP

data_array = []  # List to store rows as dictionaries

# Open the ZIP and read the CSV
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME) as csv_file:
        # Decode bytes to text and read it as a CSV
        csv_text = io.TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.DictReader(csv_text, delimiter=';')  # Read as dictionary
        
        # Store all rows in an array
        acidentes_array = [row for row in csv_reader]

# Print the first two rows for verification
for row in acidentes_array[:2]:
    print(row.keys())
