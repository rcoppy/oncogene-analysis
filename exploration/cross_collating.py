from gene_models import model_processed
from postprocessor_filter import PostprocessorFilter

DATA_SURVIVORS_PATH = '../data/collated/survivors'
DATA_DECEASED_PATH = '../data/collated/deceased'

DESTINATION_SURVIVORS_PATH = '../data/filtered-collated/survivors'
DESTINATION_DECEASED_PATH = '../data/filtered-collated/deceased'


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


survivors_processor = PostprocessorFilter(global_genes, DATA_SURVIVORS_PATH, DESTINATION_SURVIVORS_PATH)
deceased_processor = PostprocessorFilter(global_genes, DATA_DECEASED_PATH, DESTINATION_DECEASED_PATH)

deceased_processor.filter_genes()
survivors_processor.filter_genes()

