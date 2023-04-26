from gene_models import model_processed
from postprocessor_trim import PostprocessorTrim 

DATA_SURVIVORS_PATH = '../data/processed/survivors'
DATA_DECEASED_PATH = '../data/processed/deceased'

DESTINATION_SURVIVORS_PATH = '../data/trimmed/survivors'
DESTINATION_DECEASED_PATH = '../data/trimmed/deceased'

model_type = model_processed
deceased_cutoff  = 50. # 17. # smaller sample--less variation close to the median
survivors_cutoff = 50. # 50. 

expression_count_floor = 300

survivors_processor = PostprocessorTrim(model_type, DATA_SURVIVORS_PATH, DESTINATION_SURVIVORS_PATH, survivors_cutoff, expression_count_floor)
deceased_processor = PostprocessorTrim(model_type, DATA_DECEASED_PATH, DESTINATION_DECEASED_PATH, deceased_cutoff, expression_count_floor)

deceased_processor.trim_outliers()
survivors_processor.trim_outliers()



