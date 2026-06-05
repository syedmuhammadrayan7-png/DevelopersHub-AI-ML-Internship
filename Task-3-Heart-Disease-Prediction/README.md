# Task 3: Heart Disease Prediction

## Objective
The objective of this task is to build a machine learning model that predicts whether a person is at risk of heart disease based on medical features.

## Dataset
The Heart Disease dataset was downloaded from Kaggle using the `kagglehub` library.

## Model Used
Logistic Regression was used for binary classification.

## Features
The dataset contains medical features such as:
- Age
- Sex
- Chest pain type
- Resting blood pressure
- Cholesterol
- Fasting blood sugar
- Maximum heart rate
- Exercise induced angina
- ST depression
- Slope
- Number of major vessels
- Thalassemia

## Target Variable
The target variable is `target`.

- `target = 1` means the person has heart disease
- `target = 0` means the person does not have heart disease

## Steps Performed
- Imported required libraries
- Downloaded the dataset using kagglehub
- Loaded the dataset using pandas
- Inspected the dataset using shape, columns, head, info, and describe
- Checked for missing values
- Removed duplicate rows
- Performed Exploratory Data Analysis
- Visualized target distribution
- Visualized age distribution
- Visualized heart disease by chest pain type
- Created a correlation heatmap
- Split the data into training and testing sets
- Applied feature scaling using StandardScaler
- Trained a Logistic Regression model
- Made predictions on test data
- Evaluated the model using accuracy, confusion matrix, classification report, ROC curve, and ROC-AUC score
- Analyzed important features using model coefficients

## Evaluation Metrics
The model was evaluated using:
- Accuracy
- Confusion Matrix
- Classification Report
- ROC Curve
- ROC-AUC Score

## Key Insights
The Logistic Regression model was able to classify whether a person is at risk of heart disease based on medical features.

The ROC curve and ROC-AUC score helped evaluate how well the model separates the two classes.

The feature importance analysis showed which medical features had stronger influence on the prediction.

## Conclusion
This task helped in understanding binary classification, medical dataset analysis, model evaluation, and feature importance.

This project is for learning purposes only and should not be used as a replacement for professional medical diagnosis.
