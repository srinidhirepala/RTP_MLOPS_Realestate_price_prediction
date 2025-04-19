import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

sheet_id = "15OfQ_JmxKTcRhN12CfN2ivsSFhizkQztKf3Rl-m2t1s"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

print(f"\n Reading Google Sheet from: {sheet_url}")
df = pd.read_csv(sheet_url)

print("\n Basic Info:")
print(df.info())

print("\n First 5 rows:")
print(df.head())

print("\n Shape:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n Summary Statistics (Numeric):")
print(df.describe())

print("\n Summary Statistics (Object / Categorical):")
print(df.describe(include='object'))

print("\n Column Types:")
print(df.dtypes)

print("\n Missing Values Per Column:")
print(df.isnull().sum())

print("\n Missing Values Per Row:")
print(df.isnull().sum(axis=1))

df = df.dropna()
print("\n Shape after removing missing values:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n Number of Duplicate Rows:")
print(df.duplicated().sum())

df['group_id'] = df.groupby(df.columns.tolist(), dropna=True).ngroup()
duplicate_rows = df[df.duplicated(keep=False)].sort_values(by='group_id')
group_counts = duplicate_rows['group_id'].value_counts().sort_index()

print("\n Duplicate Rows:")
print(duplicate_rows)
print("\n Group Counts:")
print(group_counts)

df = df.drop_duplicates(keep='first')
df = df.drop(columns=['group_id'])

print("\n Shape after removing duplicates:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n Unique Values Per Column:")
for col in df.columns:
    print(f"{col}: {df[col].unique()}")
    print("-" * 20)

def clean_price(value):
    if isinstance(value, str):
        value = value.strip().lower()
        if "crore" in value:
            return float(value.replace("crore", "").replace("c", "").strip()) * 1e7
        elif "lac" in value:
            return float(value.replace("lac", "").replace("l", "").strip()) * 1e5
        elif "ac" in value:
            return float(value.replace("ac", "").replace("a", "").strip()) * 1e4
        else:
            return pd.to_numeric(value, errors='coerce')
    return value

df["Price"] = df["Price"].apply(clean_price)

df["open_sides"] = pd.to_numeric(df["open_sides"], errors="coerce")
df["Width_road"] = pd.to_numeric(df["Width_road"].str.replace(r"[^0-9.]", "", regex=True), errors="coerce")

print("\n Generating Histograms for Numeric Columns...")
df.hist(figsize=(12, 8), bins=20)
plt.suptitle('Histograms of Numeric Columns')
plt.tight_layout()
plt.show()

#BAR CHARTS (CATEGORICAL)
for col in df.select_dtypes(include=['object', 'string']):
    category_counts = df[col].value_counts()
    category_counts.plot(kind='bar', figsize=(10, 6))
    plt.title(f'{col} Distribution')
    plt.xlabel('Category')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#CORRELATION MATRIX
print("\n🔹 Correlation Matrix (Numeric Columns):")
corr = df.corr(numeric_only=True)
print(corr)

if not corr.empty:
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

#ENCODING CATEGORICAL VALUES
df_encoded = df.copy()

for col in df_encoded.select_dtypes(include=['object', 'string']):
    if df_encoded[col].nunique() < 20:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        print(f"\n Encoded {col}: {df_encoded[col].unique()}")
    else:
        print(f" Skipping {col} (too many categories)")
        df_encoded.drop(columns=[col], inplace=True)

#ENCODED CORRELATION HEATMAP
corr_encoded = df_encoded.corr(numeric_only=True)

plt.figure(figsize=(12, 8))
sns.heatmap(corr_encoded, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Correlation Heatmap (Encoded)")
plt.tight_layout()
plt.show()

df.to_csv('/content/drive/MyDrive/cleaned_data.csv', index=False)

print("\n EDA complete.")
