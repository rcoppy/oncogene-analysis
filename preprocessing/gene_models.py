class base_model: 
    def __init__(self, row_data) -> None:
        pass

    model_name = "Abstract gene model format"
    skippable_rows_count = 6 # skip the first n lines of the file, if they're not data but a header

class model_processed(base_model): 
    model_name = "training-ready format"
    skippable_rows_count = 4

    def __init__(self, row_data) -> None:
        self.gene_name = row_data[0]
        self.unstranded = row_data[1]
        self.unstranded_normalized = row_data[2]

class model_gencode_36(base_model): 
    def __init__(self, row_data) -> None:
        self.gene_id = row_data[0]
        self.gene_name = row_data[1]
        self.gene_type = row_data[2]
        self.unstranded = row_data[3]
        self.stranded_first = row_data[4]
        self.stranded_second = row_data[5]
        self.tpm_unstranded = row_data[6]
        self.fpkm_unstranded = row_data[7]
        self.fpkm_uq_unstranded = row_data[8]

    model_name = "GENCODE v36"
    skippable_rows_count = 6
    