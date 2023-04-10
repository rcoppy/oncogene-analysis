from gene_models import model_gencode_36 as gencode

TEST_DATA_PATH = '../data/d1f7678a-8106-46c9-95b7-5ec5d940f08c.rna_seq.augmented_star_gene_counts.tsv'
model_type = gencode

reads_map: dict[str, model_type] = {}

with open(TEST_DATA_PATH) as f: 
    
    # skip the header data
    for i in range(0, model_type.skippable_rows_count): 
        print(f.readline())

    while line := f.readline(): 
        gene = gencode(line.split())
        if gene.gene_type != 'protein_coding': continue # there are 40 distinct gene types, for purposes of scope we are constraining to just ones coding for proteins

        reads_map[gene.gene_name] = gene

with open('./results/coding_gene_list.txt', 'w', encoding='utf-8') as f: 
    unique_gene_count = len(reads_map.keys())
    header = f"data origin: '{TEST_DATA_PATH}'\n"
    header += f"{unique_gene_count} coding genes total\n"
    print(header)
    f.write(header)
    
    for gene in reads_map.keys(): 
        f.write(gene + '\n')

