import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pickle

# Load your CSV data
df = pd.read_csv("final_dataset.csv")

y = df['label'].map({'not_spam': 0, 'spam': 1})

print("Columns in dataset:", df.columns)

# Replace 'message' and 'label' with your real column names
X = df['text']
#y = df['label']

# Split your dataset for training/testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a Pipeline that vectorizes and then trains classifier
model = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words='english')),
    ('classifier', LogisticRegression())
])

# Train the model
model.fit(X_train, y_train)

# Evaluate on test set
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the trained model pipeline to disk
with open("spam_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as spam_classifier.pkl")