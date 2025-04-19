import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression

df = pd.read_csv("/content/drive/MyDrive/cleaned_data.csv")

df.dropna(inplace=True)

X = df.drop(columns=['Price'])
y = df['Price']

X_encoded = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

model = LinearRegression()

start_time = time.time()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
end_time = time.time()

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
non_zero = y_test != 0
mape = np.mean(np.abs((y_test[non_zero] - y_pred[non_zero]) / y_test[non_zero])) * 100
train_time = end_time - start_time

print("\n Linear Regression Model Evaluation:")
print(f"R² Score       : {round(r2, 4)}")
print(f"MAE            : {round(mae, 4)}")
print(f"MAPE (%)       : {round(mape, 2)}")
print(f"Train Time (s) : {round(train_time, 3)}")
