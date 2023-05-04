import os
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from imblearn.over_sampling import RandomOverSampler, SMOTE

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

    print("Value counts before resampling: ")
    print(combined_data['Result'].value_counts())

    target = combined_data['Result']
    combined_data = combined_data.drop(columns=['sample_id', 'Result', 'ZZZ3\n'])

    X_train, X_test, y_train, y_test = train_test_split(combined_data, target, test_size=0.3, random_state=42)


    ros = RandomOverSampler(random_state=42)
    X_train_oversample, y_train_oversample = ros.fit_resample(X_train, y_train)

    #  Initialize and train logistic regression model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_oversample, y_train_oversample)
    
    print("Value counts after resampling: ")
    print(y_train_oversample.value_counts())

    # # Make predictions on testing set
    y_pred = model.predict(X_test)

    f1_score = f1_score(y_test, y_pred, pos_label="Survived")
    accuracy_score = accuracy_score(y_test, y_pred)
    # # Evaluate model performance
    print("\n\nAccuracy: ", accuracy_score)
    print("F1 Score: ", f1_score)
    

    cm = confusion_matrix(y_test, y_pred)
    print('Confusion matrix:')
    print(cm)

    # Generate classification report
    report = classification_report(y_test, y_pred)
    print('Classification report:')
    print(report)

    # Get feature importance
    feature_importance = model.feature_importances_
    print(feature_importance)
    sorted_idx = feature_importance.argsort()[::-1]
    genes = combined_data.columns

    # Plot top important genes
    plt.figure(figsize=(20, 20))
    plt.barh(range(feat_impo_size), feature_importance[sorted_idx][:feat_impo_size], align='center')
    plt.yticks(range(feat_impo_size), genes[sorted_idx][:feat_impo_size])
    plt.xlabel('Feature Importance')
    plt.ylabel('Genes')
    plt.title('Top 100 Important Genes')
    plt.gca().invert_yaxis()
    plt.savefig('6k_log_reg_top100_wit_smote.png') 

    cm = confusion_matrix(y_test, y_pred)  
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Deceased", "Survived"])

    disp.plot()
    
    plt.show()

    






