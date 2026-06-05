# Task 2: Predict Future Stock Prices

## Objective
The objective of this task is to use historical stock market data to predict the next day's closing price of a selected stock.

## Dataset
The dataset was collected from Yahoo Finance using the `yfinance` Python library.

## Stock Selected
Apple Inc. stock was selected using the ticker symbol `AAPL`.

## Features Used
The following features were used to predict the next day's closing price:

- Open
- High
- Low
- Volume

## Target Variable
The target variable was the next day's closing price, created using the `Close` column shifted by one day.

## Model Used
Linear Regression was used for prediction.

## Steps Performed
- Imported required libraries
- Downloaded historical stock data using yfinance
- Inspected the dataset using shape, columns, head, info, and describe
- Created a new column for next day's closing price
- Selected input features and target variable
- Split the dataset into training and testing sets
- Trained a Linear Regression model
- Made predictions on test data
- Evaluated the model using MAE, MSE, RMSE, and R2 Score
- Plotted actual vs predicted closing prices

## Key Results
The model was able to learn the general relationship between stock market features and the next day's closing price.

## Conclusion
This task helped in understanding basic time-series style prediction using machine learning. However, stock prices are affected by many external factors such as news, market sentiment, company performance, and economic conditions. Therefore, this model is mainly for learning purposes and should not be used for real investment decisions.
