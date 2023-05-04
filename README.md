# oncogene-analysis
COMS 4761 final project, spring 2023. 

The data is archived in data/archives folder and we had to zip the files because they were huge. We used git-lfs for storing actual transciptome data.

Models Testing<br>
The models are categorized into three different folder: 214, 3k and 6k genes, which refers to the number of genes we used for building the models (Originally we had 17k genes).

Each subfolder contains the csv and three models file: Logistic Regression, Decision Tree and Random Forest. Hence the python file is called breast_cancer_3k_genes_log_reg.py, breast_cancer_3k_genes_dec_tree.py breast_cancer_3k_genes_random_forest.py for Logistic Regression, Decision Tree and Random Forest respectively.

To run the python file, run this on the command line: <br>
```python breast_cancer_3k_genes_log_reg.py```
<br>
If you get an error that a particular module could not be found, install the required package using:<br>
```pip install <package_name>```
<br>
E.g ```pip install imblearn```
<br>

The project uses ```scikit-learn```, ```imblearn``` and other packages which might need installation.
