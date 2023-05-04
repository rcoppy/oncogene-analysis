import numpy as np
import os, utils, csv
from gene_models import base_model
import pathlib
from datetime import datetime

class PostprocessorFilter: 
    # exclude all but the genes passed in as parameter
    def __init__(self, global_gene_set, data_path, destination_path) -> None:
        self.data_path = data_path 
        self.destination_path = destination_path
        self.global_gene_set: set[str] = global_gene_set
        self.lexicographic_gene_list: list = sorted(list(global_gene_set))
        self.csv_fieldnames = ['sample_id'] + self.lexicographic_gene_list

    def filter_genes(self): 
        # get segment folders
        segment_subfolders = [f.name for f in os.scandir(self.data_path) if f.is_dir()]
        print(segment_subfolders)

        for s in segment_subfolders:
            destination = os.path.join(self.destination_path, s)
            # make destination folder if doesn't exist
            pathlib.Path(destination).mkdir(parents=True, exist_ok=True)

            table_path = os.path.join(destination, 'filtered-collated-data-' + s + '.csv')

            for root, dirs, files in os.walk(os.path.join(self.data_path, s)):
                for file in files:
                    if file.endswith(".csv"):
                        self.process_file(os.path.join(root, file), table_path)

    def process_file(self, file_path, destination_path): 
        # input_values: dict[str, float] = dict()
        
        rows: list[dict] = list()
        header_lines: list[str] = [f'origin: {file_path}\n', f'{len(self.global_gene_set)} coding genes\n']

        with open(file_path, 'r') as f: 
            
            # skip the header data
            for i in range(0, 2): 
                print(f.readline())

            reader = csv.DictReader(f)

            for gene in reader:
                output_values: dict = dict()
                expression_total: float = 0.

                for column, value in gene.items(): 
                    if column == 'sample_id':
                        output_values[column] = value
                        continue

                    if not column in self.global_gene_set: continue

                    expression_total += float(value)

                for column, value in gene.items(): 
                    if column == 'sample_id': continue
                    if not column in self.global_gene_set: continue

                    output_values[column] = float(value) / expression_total

                rows.append(output_values)

        with open(destination_path, 'w', encoding='utf-8') as f: 
            # restore header
            f.writelines(header_lines)

            writer = csv.DictWriter(f, fieldnames=self.csv_fieldnames)

            writer.writeheader()
            writer.writerows(rows)