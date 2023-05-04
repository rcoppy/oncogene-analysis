import numpy as np
import os, utils
from gene_models import base_model
import pathlib

class PostprocessorTrim: 
    def __init__(self, model_type: base_model, data_path, destination_path, deviation_cutoff: int, count_floor: int = 1000) -> None:
        self.model_type = model_type
        self.data_path = data_path 
        self.destination_path = destination_path
        self.deviation_cutoff = deviation_cutoff
        self.count_floor = count_floor

    # https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    # FYI: reasonable to assume transcriptome follows negative binomial distribution: https://www.biostars.org/p/463301/
    # m is max acceptable number of deviations from median 
    # data must be shape [name, count]
    def reject_outliers(data, m = 2.):
        d = np.abs(data['count'] - np.median(data['count']))
        mdev = np.median(d)
        s = d/mdev if mdev else np.zero(len(d))

        dtype = [('name', 'U20'),('count', np.int32)]

        # tried to do something with masking but got confused
        # hacky approach to filter by column value
        converted = np.row_stack([data['name'], data['count']])

        filtered = converted[:, s<m].T
        values = [(x[0], x[1]) for x in filtered]

        return np.array(values, dtype)

    
    def trim_outliers(self): 
        # get segment folders
        segment_subfolders = [f.name for f in os.scandir(self.data_path) if f.is_dir()]
        print(segment_subfolders)

        for s in segment_subfolders:
                destination = os.path.join(self.destination_path, s)

                for root, dirs, files in os.walk(os.path.join(self.data_path, s)):
                    for file in files:
                        if file.endswith(".csv"):
                            self.process_file(os.path.join(root, file), destination, file)

    def process_file(self, file_path, destination_path, filename): 
        dtype_input = [('name', 'U20'),('count', np.int32)]
        dtype_output = [('name', 'U20'),('count', np.int32),('count_normalized', np.float32)]

        input_values = list()
        output_values = list()

        with open(file_path) as f: 
            
            # skip the header data
            for i in range(0, self.model_type.skippable_rows_count): 
                print(f.readline())

            while line := f.readline(): 
                gene: base_model = self.model_type(line.split(','))                
                count = int(gene.unstranded)

                # reject counts less than count floor 
                if count < self.count_floor: continue

                input_values.append((gene.gene_name, count))

        input_array = np.array(input_values, dtype=dtype_input)
        trimmed_input = PostprocessorTrim.reject_outliers(input_array, self.deviation_cutoff)
        
        # during preprocessing the data was already sorted
        # trimmed_input.sort(order='count')
        # array_descending = array[::-1]

        total_count = np.sum(trimmed_input['count'])

        path = os.path.join(destination_path, 'trimmed-' + filename)

        # make destination folder if doesn't exist
        pathlib.Path(destination_path).mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f: 
            unique_gene_count = len(trimmed_input['count'])

            header = f"data origin: '{file_path}'\n"
            header += f"{unique_gene_count} coding genes total, with outliers removed (>{self.deviation_cutoff} deviations from median)\n"
            header += f"{total_count} total expressions counted\n"
            header += 'gene name,unstranded count,normalized_count\n'
            # print(header)
            f.write(header)

            for name, count in trimmed_input: 
                count_normalized = count / total_count

                output_values.append((name, count, count_normalized))
                
            final_output = np.array(output_values, dtype=dtype_output)
            
            for i in final_output: 
                f.write(utils.format_csv_line([i[0], i[1], i[2]]))