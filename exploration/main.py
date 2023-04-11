from gene_models import model_gencode_36 as gencode
import utils 
import numpy as np

TEST_DATA_PATH = '../data/d1f7678a-8106-46c9-95b7-5ec5d940f08c.rna_seq.augmented_star_gene_counts.tsv'
model_type = gencode

reads_map: dict[str, model_type] = {}
reads_metadata: dict = {}

reads_metadata['unstranded_total_count'] = 0

with open(TEST_DATA_PATH) as f: 
    
    # skip the header data
    for i in range(0, model_type.skippable_rows_count): 
        print(f.readline())

    while line := f.readline(): 
        gene = gencode(line.split())
        if gene.gene_type != 'protein_coding': continue # there are 40 distinct gene types, for purposes of scope we are constraining to just ones coding for proteins
        if int(gene.unstranded) < 1: continue # don't count genes with no reads
         
        reads_map[gene.gene_name] = gene
        reads_metadata['unstranded_total_count'] += int(gene.unstranded)

with open('./results/coding_gene_list.csv', 'w', encoding='utf-8') as f: 
    unique_gene_count = len(reads_map.keys())
    header = f"data origin: '{TEST_DATA_PATH}'\n"
    header += f"{unique_gene_count} coding genes total\n"
    header += f"{reads_metadata['unstranded_total_count']} total expressions counted\n"
    header += 'gene name,unstranded count,normalized_count\n'
    print(header)
    f.write(header)

    dtype = [('name', 'U20'),('count', np.int32),('count_normalized', np.float32)]
    values = list()

    for gene in reads_map.values(): 
        name = gene.gene_name
        count = int(gene.unstranded)
        count_normalized = count / reads_metadata['unstranded_total_count']

        values.append((name, count, count_normalized))

        

    array = np.array(values, dtype=dtype)
    array.sort(order='count')

    print(array[-11:-1])

    array_descending = array[::-1]

    for i in array_descending: # write to file in descending order 
        f.write(utils.format_csv_line([i[0], i[1], i[2]]))


    total = 0
    count = 0
    for i in array_descending: 
        if total > 0.5: break

        total += i[2]
        count += 1

    genes_total = len(reads_map.keys())
    print(f"{count} genes out of {genes_total} ({int(100 * count / genes_total)}%) account for 50% of transcripts")