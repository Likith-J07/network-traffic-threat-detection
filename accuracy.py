import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import pickle

# =======================
# Load Dataset
# =======================
df = pd.read_csv("synthetic_network_traffic.csv")

# Encode categorical features
le_protocol = LabelEncoder()
le_flags = LabelEncoder()
le_label = LabelEncoder()

df['Protocol'] = le_protocol.fit_transform(df['Protocol'])
df['Flags'] = le_flags.fit_transform(df['Flags'])
df['Label'] = le_label.fit_transform(df['Label'])

# Features and Target
X = df[['Protocol', 'Packet_Size', 'Flow_Duration', 'Flags']]
y = df['Label']

# Balance dataset with SMOTE
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
)

# =======================
# Random Forest with GridSearchCV
# =======================
param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "bootstrap": [True, False],
}

rf = RandomForestClassifier(random_state=42)

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1,
    scoring="accuracy",
    verbose=2
)

grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# =======================
# Evaluate
# =======================
y_pred = best_model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("✅ Best Parameters:", grid_search.best_params_)
print("✅ Accuracy:", acc)
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le_label.classes_))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# =======================
# Save Model
# =======================
pickle.dump((best_model, le_protocol, le_flags, le_label), open("model.pkl", "wb"))
print("🎉 Model retrained and saved as model.pkl")
