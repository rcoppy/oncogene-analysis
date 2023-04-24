from gene_models import model_processed
from postprocessor_trim import PostprocessorTrim 

DATA_SURVIVORS_PATH = '../data/processed/survivors'
DATA_DECEASED_PATH = '../data/processed/deceased'

DESTINATION_SURVIVORS_PATH = '../data/trimmed/survivors'
DESTINATION_DECEASED_PATH = '../data/trimmed/deceased'

model_type = model_processed
cutoff = 2.

survivors_processor = PostprocessorTrim(model_type, DATA_SURVIVORS_PATH, DESTINATION_SURVIVORS_PATH, cutoff)
deceased_processor = PostprocessorTrim(model_type, DATA_DECEASED_PATH, DESTINATION_DECEASED_PATH, cutoff)

deceased_processor.trim_outliers()
survivors_processor.trim_outliers()



