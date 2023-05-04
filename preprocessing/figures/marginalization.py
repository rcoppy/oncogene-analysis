import csv

input_paths = ['/Users/arcop/code/git/oncogene-analysis/data/archives/3k-filtered-collated/deceased-filtered-collated-data-training.csv',
         '/Users/arcop/code/git/oncogene-analysis/data/archives/3k-filtered-collated/survivors-filtered-collated-data-training.csv'
         ]

output_paths = ['deceased-average-expression.csv', 'survivors-average-expression.csv']

def marginalize_data(input_path: str, output_path: str): 

    average_expressions: dict[str, float] = dict()

    with open(input_path, 'r') as f: 
            
        # skip the header data
        for i in range(0, 2): 
            print(f.readline())

        reader = csv.DictReader(f)

        total_expressions: dict[str, float] = dict()
        sample_count: int = 0

        for sample in reader:
            sample_count += 1

            for column, value in sample.items(): 
                if column == 'sample_id':
                    # output_values[column] = value
                    continue

                if not column in average_expressions.keys(): 
                    try:
                        average_expressions[column] = float(value)
                    except ValueError:
                        print(column, value)
                else: 
                    average_expressions[column] += float(value)

        
        for gene, expression in total_expressions.items(): 
            average_expressions[gene] = expression / sample_count

    with open(output_path, 'w', encoding='utf-8') as f: 
        writer = csv.DictWriter(f, fieldnames=['gene', 'expression'])

        writer.writeheader()

        for gene, expression in average_expressions.items(): 
            writer.writerow({'gene': gene, 'expression': expression})

        print(len(average_expressions.keys()))

for i in range(len(input_paths)):
    marginalize_data(input_paths[i], output_paths[i])