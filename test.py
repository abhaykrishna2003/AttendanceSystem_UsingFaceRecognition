# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

# load the face embeddings for testing
print("[INFO] loading testing face embeddings...")
test_data = pickle.loads(open("output/embeddings_test.pickle", "rb").read())

# load the testing labels
print("[INFO] loading testing labels...")
test_labels = pickle.loads(open("output/le.pickle", "rb").read())

# load the trained label encoder
print("[INFO] loading label encoder...")
le = pickle.loads(open("output/le.pickle", "rb").read())

# load the trained face recognizer model
print("[INFO] loading face recognizer model...")
recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())

# predict labels for the testing set
print("[INFO] predicting labels for the testing set...")
test_predictions = recognizer.predict(test_data["embeddings"])

# calculate testing accuracy
test_accuracy = accuracy_score(test_labels, test_predictions)
print(f"[INFO] Testing Accuracy: {test_accuracy * 100:.2f}%")

# calculate and display other performance metrics for testing
print("[INFO] Testing Classification Report:")
print(classification_report(test_labels, test_predictions, target_names=le.classes_))

print("[INFO] Testing Confusion Matrix:")
print(confusion_matrix(test_labels, test_predictions))

print("done..")
