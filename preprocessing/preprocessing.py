from gene_models import model_gencode_36 as gencode
import numpy as np
import os, math, utils
from preprocessor import Preprocessor 

DATA_SURVIVORS_PATH = '../data/decompressed/survivors'
DATA_DECEASED_PATH = '../data/decompressed/deceased'

DESTINATION_SURVIVORS_PATH = '../data/processed/survivors'
DESTINATION_DECEASED_PATH = '../data/processed/deceased'

model_type = gencode

default_segmentation = [("training", 70), ("validation", 15), ("testing", 15)]

survivors_processor = Preprocessor(model_type, DATA_SURVIVORS_PATH, DESTINATION_SURVIVORS_PATH, default_segmentation)
deceased_processor = Preprocessor(model_type, DATA_DECEASED_PATH, DESTINATION_DECEASED_PATH, default_segmentation)

deceased_processor.process_segments()
survivors_processor.process_segments()



