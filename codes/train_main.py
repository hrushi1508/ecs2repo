import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

# Dataset folder
dataset_path = r"C:\Users\DELL\OneDrive\Desktop\train\train"

# Image size
IMG_SIZE = (64, 64)

# Prepare data
X = []
y = []

for label in os.listdir(dataset_path):
    label_path = os.path.join(dataset_path, label)
    if not os.path.isdir(label_path):
        continue
    print("📂 Reading folder:", label)   # <---- ADD THIS LINE
    for img_name in os.listdir(label_path):
        ...



# Each folder name is the label (20, 30, 60, 80, 100)
for label in os.listdir(dataset_path):
    label_path = os.path.join(dataset_path, label)
    if not os.path.isdir(label_path):
        continue
    for img_name in os.listdir(label_path):
        img_path = os.path.join(label_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        img = cv2.resize(img, IMG_SIZE)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        X.append(img_gray.flatten())
        y.append(int(label))

X = np.array(X)
y = np.array(y)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"✅ Training complete! Accuracy: {accuracy*100:.2f}%")

# Save model
joblib.dump(model, "speed_sign_model.pkl")
print("💾 Model saved as speed_sign_model.pkl")



#pip install numpy==1.26.4
#pip install opencv-python==4.10.0.84
#pip install scikit-learn==1.4.2
#pip install joblib==1.4.2
#pip install pillow==10.3.0



