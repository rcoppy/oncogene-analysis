import numpy as np
import os, utils
from gene_models import base_model
import pathlib
from datetime import datetime

class PostprocessorCollate: 
    def __init__(self, model_type: base_model, data_path, destination_path) -> None:
        self.model_type = model_type
        self.data_path = data_path 
        self.destination_path = destination_path
        self.global_gene_set: set = set()
        self.lexicographic_gene_list: list = list()
        self.in_memory_data: dict[str, dict[str, dict[str, float]]] = dict() 
        
        '''
        { 
            segment: { 
                sample_id: {
                    gene_name: frequency 
                } 
            }
        }
        '''

    def collate_data(self): 
        # get segment folders
        segment_subfolders = [f.name for f in os.scandir(self.data_path) if f.is_dir()]
        print(segment_subfolders)

        for s in segment_subfolders:
                destination = os.path.join(self.destination_path, s)

                # make destination folder if doesn't exist
                pathlib.Path(destination).mkdir(parents=True, exist_ok=True)

                table_path = os.path.join(destination, 'collated-data-' + s + '.csv')
                

                for root, dirs, files in os.walk(os.path.join(self.data_path, s)):
                    for file in files:
                        if file.endswith(".csv"):
                            sample_id = file.replace('trimmed-', '')
                            sample_id = sample_id.replace('.csv', '')

                            self.process_file(os.path.join(root, file), sample_id, s)

        print(f'total genes in common across all samples within {self.data_path}: {len(self.global_gene_set)}')
        # print(1 + '2')


        # global gene set is already fully intersected across segments
        # now need to go back into segments and strip out new outlier genes
        for s in segment_subfolders: 
            pruned_segment = dict()
            for sample_id, gene_data in self.in_memory_data[s].items(): 
                pruned_gene_data = dict()
                for gene_name, frequency in gene_data.items(): 
                    if not gene_name in self.global_gene_set: continue

                    pruned_gene_data[gene_name] = frequency

                pruned_segment[sample_id] = pruned_gene_data

            self.in_memory_data[s] = pruned_segment

        # convert the global gene set to a fixed-order list to make sure 
        # genes stay synchronized with frequencies 
        self.lexicographic_gene_list = sorted(list(self.global_gene_set))

        # finally ready to write segment tables
        for s in segment_subfolders: 
            destination = os.path.join(self.destination_path, s)
            table_path = os.path.join(destination, 'collated-data-' + s + '.csv')

            self.write_table_header(table_path, s)
            self.write_table_rows(table_path, s)

    def write_table_header(self, table_path, segment_name): 
        with open(table_path, 'w', encoding='utf-8') as f: 
            unique_gene_count = len(self.global_gene_set)

            header = f"{segment_name} segment, collated on {datetime.today().strftime('%Y-%m-%d')}\n"
            header += f"{unique_gene_count} coding genes total\n"
            header += 'sample_id,'

            # add each gene name as a column, in lexicographic order
            for g in self.lexicographic_gene_list:  
                header += f'{g},'

            # last comma should be swapped with newline
            f.write(header[:-1] + '\n')

    def write_table_rows(self, table_path, segment_name): 
        # append new rows to previous
        with open(table_path, 'a', encoding='utf-8') as f:
            for sample_id, gene_data in self.in_memory_data[segment_name].items():
                row = f'{sample_id},'

                # maintain ordering by referencing list
                for gene_name in self.lexicographic_gene_list: 
                    row += f'{gene_data[gene_name]},'

                # last comma should be swapped with newline
                f.write(row[:-1] + '\n')

    def process_file(self, file_path, sample_id, segment): 
        input_values: dict[str, float] = dict()
        output_values: dict[str, float] = dict()

        with open(file_path) as f: 
            
            # skip the header data
            for i in range(0, self.model_type.skippable_rows_count): 
                print(f.readline())

            while line := f.readline(): 
                gene: base_model = self.model_type(line.split(','))                
                frequency = float(gene.unstranded_normalized)

                input_values[gene.gene_name] = frequency

        local_genes = input_values.keys()
        
        if len(self.global_gene_set) < 1: 
            # completely empty, this is the first sample being processed
            self.global_gene_set = set(local_genes)
        else: 
            self.global_gene_set.intersection_update(local_genes)

        for gene_name, frequency in input_values.items(): 
            # discard outlier genes
            if not gene_name in self.global_gene_set: continue

            output_values[gene_name] = frequency

        # store gene frequencies tagged by sample id within proper segment
        if not segment in self.in_memory_data.keys(): 
            self.in_memory_data[segment] = dict()
        
        self.in_memory_data[segment][sample_id] = output_values