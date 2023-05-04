import os
import io
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, f1_score, classification_report, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE, RandomOverSampler

# Change this number if you want top 50/100 genes for feature importance
feat_impo_size = 100

if __name__ == "__main__":
    sur_training_data = pd.read_csv('./survivors/filtered-collated-data-training.csv')
    sur_validation_data = pd.read_csv('./survivors/filtered-collated-data-validation.csv')
    sur_test_data = pd.read_csv('./survivors/filtered-collated-data-testing.csv')

    dec_training_data = pd.read_csv('./deceased/filtered-collated-data-training_dec.csv')
    dec_validation_data = pd.read_csv('./deceased/filtered-collated-data-validation_dec.csv')
    dec_test_data = pd.read_csv('./deceased/filtered-collated-data-testing_dec.csv')

    combined_data = pd.concat([sur_training_data, sur_validation_data, sur_test_data, dec_training_data, dec_validation_data, dec_test_data], ignore_index=True)

    # Performing SMOTE since negative class is in minority (9:2 ratio)
    print("Value counts before resampling: ")
    print(combined_data['Result'].value_counts())

    target = combined_data['Result']
    combined_data = combined_data.drop(columns=['sample_id', 'Result', 'ZZZ3\n'])
    
    gene_expression_sum = combined_data.sum(axis=0)
    
    sorted_gene_expr = gene_expression_sum.argsort()[::-1]

    X_train, X_test, y_train, y_test = train_test_split(combined_data, target, test_size=0.3, random_state=42)
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    
    print("Value counts after resampling: ")
    print(y_train_smote.value_counts())

    #  Initialize and train logistic regression model
    model = LogisticRegression()
    model.fit(X_train_smote, y_train_smote)

    # # Make predictions on testing set
    y_pred = model.predict(X_test)

    # # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy:', accuracy)
    print("F1 Score: ", f1_score(y_test, y_pred, pos_label="Survived"))
    print("AUC score: ", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))

    # # Get feature importance
    feature_importance = abs(model.coef_[0])
    sorted_idx = feature_importance.argsort()[::-1]
    genes = combined_data.columns

    # Plot top 100 important genes
    
    plt.figure(figsize=(20, 15))
    plt.barh(range(feat_impo_size), feature_importance[sorted_idx][:feat_impo_size], align='center')
    plt.yticks(range(feat_impo_size), genes[sorted_idx][:feat_impo_size])
    plt.xlabel('Feature Importance')
    plt.ylabel('Genes')
    plt.title('Top 100 Important Genes')
    plt.gca().invert_yaxis()
    plt.savefig('3k_log_reg_top100_without_smote.png') 
    
    # print("Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)  
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Deceased", "Survived"])
    disp.plot()
    plt.show()
    
    # Generate classification report
    report = classification_report(y_test, y_pred)
    print('\n\nClassification report:')
    print(report)

    cm = confusion_matrix(y_test, y_pred)
    print('Confusion matrix:')
    print(cm)




