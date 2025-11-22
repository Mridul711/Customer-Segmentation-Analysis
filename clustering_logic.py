import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Load the clean data you just created
df = pd.read_csv('rfm_data.csv')

# 2. Data Cleaning for ML
# Remove missing CustomerIDs and outliers (negative money/quantity)
df = df.dropna()
df = df[df['Monetary'] > 0]

# 3. Prepare data for the Algorithm
# We only use the 3 columns: Recency, Frequency, Monetary
X = df[['Recency', 'Frequency', 'Monetary']]

# 4. Scaling (VERY IMPORTANT)
# K-Means gets confused if one number is 500 (Recency) and another is 10,000 (Money).
# Scaling makes them all comparable (like converting km and miles to meters).
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Apply K-Means Clustering (4 Groups)
print("Running K-Means Clustering...")
kmeans = KMeans(n_clusters=4, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# 6. Analyze the Results
# This shows the average behavior of each group
summary = df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
print("-" * 30)
print("CLUSTER SUMMARY (Average Values):")
print(summary)
print("-" * 30)

# 7. Save final file for Power BI
df.to_csv('rfm_final_with_clusters.csv', index=False)
print("SUCCESS! 'rfm_final_with_clusters.csv' saved.")
