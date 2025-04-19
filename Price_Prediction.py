import pandas as pd
import os

output_dir = '/content/linear_regression_output/'
os.makedirs(output_dir, exist_ok=True)

evaluation_metrics = {
    'R² Score': round(r2, 4),
    'MAE': round(mae, 4),
    'MAPE (%)': round(mape, 2),
    'Train Time (s)': round(train_time, 3)
}

df_metrics = pd.DataFrame([evaluation_metrics])

file_path = os.path.join(output_dir, 'linear_regression_evaluation_metrics.csv')
df_metrics.to_csv(file_path, index=False)

file_path

#converting csv file to pkl file

import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("/content/drive/MyDrive/cleaned_data.csv")

df.dropna(inplace=True)

X = df.drop(columns=['Price'])
y = df['Price']

X_encoded = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


model_filename = '/content/linear_regression_model.pkl'
joblib.dump(model, model_filename)

print(f"Model saved to: {model_filename}")

# price prediction
import joblib
import pandas as pd
import numpy as np

model = joblib.load('/content/linear_regression_model.pkl')

def predict_price(area_sq_yards, facing_input, open_sides, road_width):
    land_area = area_sq_yards * 9

    facing_columns = ['facing_North', 'facing_East', 'facing_South', 'facing_West', 'facing_North-East', 'facing_North-West', 'facing_South-East', 'facing_South-West']
    facing_vector = {col: 0 for col in facing_columns}
    facing_col_name = f"facing_{facing_input}"
    if facing_col_name in facing_vector:
        facing_vector[facing_col_name] = 1
    else:
        print(f"Warning: Facing value '{facing_input}' not seen during training. Model may behave unexpectedly.")

    input_data = {
        'land_area': land_area,
        'no_of_open_gates': open_sides,
        'road_width': road_width,
        **facing_vector
    }

    input_df = pd.DataFrame([input_data])

    input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)
    predicted_price = model.predict(input_df)

    return predicted_price[0]

area_sq_yards = int(input())
facing_input = input()
open_sides = int(input())
road_width = int(input())

predicted_price = predict_price(area_sq_yards, facing_input, open_sides, road_width)

print(f"Predicted Price: ₹{abs(predicted_price):.2f}")

#mounting google drive

from google.colab import drive
drive.mount('/content/drive')
