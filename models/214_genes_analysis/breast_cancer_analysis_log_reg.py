import os
import io
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Change this number if you want top 50/100 genes for feature importance
feat_impo_size = 50

if __name__ == "__main__":
    sur_training_data = pd.read_csv('./survivors/filtered-collated-data-training.csv')
    sur_validation_data = pd.read_csv('./survivors/filtered-collated-data-validation.csv')
    sur_test_data = pd.read_csv('./survivors/filtered-collated-data-testing.csv')

    dec_training_data = pd.read_csv('./deceased/filtered-collated-data-training_dec.csv')
    dec_validation_data = pd.read_csv('./deceased/filtered-collated-data-validation_dec.csv')
    dec_test_data = pd.read_csv('./deceased/filtered-collated-data-testing_dec.csv')

    combined_data = pd.concat([sur_training_data, sur_validation_data, sur_test_data, dec_training_data, dec_validation_data, dec_test_data], ignore_index=True)

    target = combined_data['Result']
    combined_data = combined_data.drop(columns=['sample_id', 'Result'])

    X_train, X_test, y_train, y_test = train_test_split(combined_data, target, test_size=0.3, random_state=42)

    #  Initialize and train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # # Make predictions on testing set
    y_pred = model.predict(X_test)

    # # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy:', accuracy)
    print('F1 Score: ', f1_score(y_test, y_pred, pos_label="Survived"))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print('Confusion matrix:')
    print(cm)

    # Generate classification report
    report = classification_report(y_test, y_pred)
    print('Classification report:')
    print(report)

    # # Get feature importance
    feature_importance = abs(model.coef_[0])
    sorted_idx = feature_importance.argsort()[::-1]
    genes = combined_data.columns

    # Plot top important genes
    plt.figure(figsize=(10, 8))
    plt.barh(range(30), feature_importance[sorted_idx][:30], align='center')
    plt.yticks(range(30), genes[sorted_idx][:30])
    plt.xlabel('Feature Importance')
    plt.ylabel('Genes')
    plt.title('Top 50 Important Genes without using SMOTE')
    plt.gca().invert_yaxis()
    plt.show()






