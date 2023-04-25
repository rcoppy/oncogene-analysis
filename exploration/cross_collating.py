from gene_models import model_processed
from postprocessor_collate import PostprocessorCollate

# DATA_SURVIVORS_PATH = '../data/trimmed/survivors'
# DATA_DECEASED_PATH = '../data/trimmed/deceased'

# DESTINATION_SURVIVORS_PATH = '../data/collated/survivors'
# DESTINATION_DECEASED_PATH = '../data/collated/deceased'

# model_type = model_processed

# survivors_processor = PostprocessorCollate(model_type, DATA_SURVIVORS_PATH, DESTINATION_SURVIVORS_PATH)
# deceased_processor = PostprocessorCollate(model_type, DATA_DECEASED_PATH, DESTINATION_DECEASED_PATH)

# deceased_processor.collate_data()
# survivors_processor.collate_data()

survivor_genes: set[str] = set()
deceased_genes: set[str] = set()

with open('../data/collated/deceased/testing/collated-data-testing.csv', 'r') as f: 
    f.readline()
    f.readline()

    deceased_genes = set(f.readline().split(','))
    deceased_genes.remove('sample_id')

with open('../data/collated/survivors/testing/collated-data-testing.csv', 'r') as f: 
    f.readline()
    f.readline()

    survivor_genes = set(f.readline().split(','))
    survivor_genes.remove('sample_id')

global_genes: set[str] = survivor_genes.intersection(deceased_genes)

# print(deceased_genes)
# print('------')
# print(survivor_genes)

print(global_genes)
print(len(global_genes), 'global genes')

