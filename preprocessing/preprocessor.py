import os, math, utils
import numpy as np

class Preprocessor: 

    def __init__(self, model_type, data_path, destination_path, segments: list[tuple], count_floor=1) -> None:
        self.model_type = model_type
        self.data_path = data_path
        self.destination_path = destination_path
        self.count_floor = count_floor # disregard reads below this raw count

        self.reads_map: dict[str, model_type] = {}
        self.reads_metadata: dict = {}

        self.reads_metadata['unstranded_total_count'] = 0

        self.segments = segments

    def process_segments(self): 
        # get total count of files in data directory
        file_folders = next(os.walk(self.data_path))[1]
        total_file_count = len(file_folders)

        pos = 0

        for s in self.segments:
            segment_name = s[0]
            percentage = s[1] / 100.00
            segment_count = math.floor(total_file_count * percentage)

            segment_folders = file_folders[pos:pos+segment_count]
            pos += segment_count

            for dir in segment_folders: 
                destination = os.path.join(self.destination_path, segment_name)

                for root, dirs, files in os.walk(os.path.join(self.data_path, dir)):
                    for file in files:
                        if file.endswith(".tsv"):
                            self.process_file(os.path.join(root, file), destination, file)


    def process_file(self, file_path, destination_path, filename) -> None: 
        
        with open(file_path) as f: 
            
            # skip the header data
            for i in range(0, self.model_type.skippable_rows_count): 
                print(f.readline())

            while line := f.readline(): 
                gene = self.model_type(line.split())
                if gene.gene_type != 'protein_coding': continue # there are 40 distinct gene types, for purposes of scope we are constraining to just ones coding for proteins
                if int(gene.unstranded) < self.count_floor: continue # don't count genes below the count floor
                
                self.reads_map[gene.gene_name] = gene
                self.reads_metadata['unstranded_total_count'] += int(gene.unstranded)

        path = os.path.join(destination_path, filename.replace('.tsv', '.csv'))

        with open(path, 'w', encoding='utf-8') as f: 
            unique_gene_count = len(self.reads_map.keys())
            header = f"data origin: '{file_path}'\n"
            header += f"{unique_gene_count} coding genes total\n"
            header += f"{self.reads_metadata['unstranded_total_count']} total expressions counted\n"
            header += 'gene name,unstranded count,normalized_count\n'
            print(header)
            f.write(header)

            dtype = [('name', 'U20'),('count', np.int32),('count_normalized', np.float32)]
            values = list()

            for gene in self.reads_map.values(): 
                name = gene.gene_name
                count = int(gene.unstranded)
                count_normalized = count / self.reads_metadata['unstranded_total_count']

                values.append((name, count, count_normalized))

                

            array = np.array(values, dtype=dtype)
            array.sort(order='count')

            print(array[-11:-1])

            array_descending = array[::-1]

            for i in array_descending: # write to file in descending order 
                f.write(utils.format_csv_line([i[0], i[1], i[2]]))