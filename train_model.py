import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# Load the updated CSV
# -----------------------------
data = pd.read_csv("pet_disease.csv")

# Encode Pet_Type column
le_pet = LabelEncoder()
data['Pet_Type'] = le_pet.fit_transform(data['Pet_Type'])

# Separate features and target
X = data.drop("Disease", axis=1)
y = data["Disease"]

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save trained model and encoders
joblib.dump(model, "pet_model.pkl")
joblib.dump(le_pet, "le_pet.pkl")

# Save feature columns for correct order in app
feature_columns = X.columns.tolist()
joblib.dump(feature_columns, "feature_columns.pkl")

print("✅ Model retrained successfully with new symptoms!")
