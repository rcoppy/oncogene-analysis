from gene_models import model_processed
from postprocessor_collate import PostprocessorCollate

DATA_SURVIVORS_PATH = '../data/trimmed/survivors'
DATA_DECEASED_PATH = '../data/trimmed/deceased'

DESTINATION_SURVIVORS_PATH = '../data/collated/survivors'
DESTINATION_DECEASED_PATH = '../data/collated/deceased'

model_type = model_processed

survivors_processor = PostprocessorCollate(model_type, DATA_SURVIVORS_PATH, DESTINATION_SURVIVORS_PATH)
deceased_processor = PostprocessorCollate(model_type, DATA_DECEASED_PATH, DESTINATION_DECEASED_PATH)

deceased_processor.collate_data()
survivors_processor.collate_data()



