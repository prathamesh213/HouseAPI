import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
import pickle

# Load dataset
df = pd.read_csv('house_data.csv')

# Select relevant columns
columns = ['bedrooms', 'bathrooms', 'floors', 'yr_built', 'price']
df = df[columns]

# Check for and handle missing values (simple example)
df = df.dropna()  # Or use df.fillna() for imputation

# Define features and target
X = df.iloc[:, 0:4]
y = df.iloc[:, 4]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Create a pipeline with scaling and polynomial features
pipeline = make_pipeline(
    StandardScaler(),
    PolynomialFeatures(degree=2),  # You can adjust the degree as needed
    LinearRegression()
)

# Fit the model
pipeline.fit(X_train, y_train)

# Evaluate model using cross-validation
scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2')
print(f"Cross-validated R-squared scores: {scores.mean()}")

# Save the model
pickle.dump(pipeline, open('model.pkl', 'wb'))
