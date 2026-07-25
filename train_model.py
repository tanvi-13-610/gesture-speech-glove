# =========================
# 1. IMPORTS
# =========================
import pandas as pd
import random
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

random.seed(42)

# =========================
# 2. CREATE DATASET
# =========================
data = []

def open_val():
    return random.randint(250, 420)

def closed_val():
    return random.randint(520, 750)

def noise():
    return random.randint(-130, 130)

for _ in range(40):
    data.append([open_val()+noise(), open_val()+noise(), open_val()+noise(), open_val()+noise(), "HELLO"])
    data.append([closed_val()+noise(), closed_val()+noise(), closed_val()+noise(), closed_val()+noise(), "FIST BUMP"])
    data.append([open_val()+noise(), closed_val()+noise(), closed_val()+noise(), closed_val()+noise(), "YES"])
    data.append([closed_val()+noise(), open_val()+noise(), open_val()+noise(), open_val()+noise(), "NO"])
    data.append([closed_val()+noise(), open_val()+noise(), closed_val()+noise(), closed_val()+noise(), "POINT"])
    data.append([open_val()+noise(), closed_val()+noise(), closed_val()+noise(), open_val()+noise(), "CALL"])
    data.append([closed_val()+noise(), open_val()+noise(), closed_val()+noise(), open_val()+noise(), "ROCK"])
    data.append([open_val()+noise(), open_val()+noise(), closed_val()+noise(), closed_val()+noise(), "GUN"])
    data.append([open_val()+noise(), open_val()+noise(), closed_val()+noise(), open_val()+noise(), "SPIDER"])
    data.append([closed_val()+noise(), open_val()+noise(), open_val()+noise(), closed_val()+noise(), "FOUR"])

df = pd.DataFrame(data, columns=["thumb", "index", "ring", "little", "gesture"])

# =========================
# 3. PREPROCESSING
# =========================
X = df[["thumb", "index", "ring", "little"]]

# Normalize (VERY IMPORTANT for Arduino)
X = X / 1023.0

y = df["gesture"]

le = LabelEncoder()
y_encoded = le.fit_transform(y)

print("Gesture Labels:", le.classes_)

# =========================
# 4. TRAIN MODEL
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(len(le.classes_), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=50, verbose=1)

loss, accuracy = model.evaluate(X_test, y_test)
print("✅ Accuracy:", accuracy)

# =========================
# 5. CONVERT TO TFLITE
# =========================
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optimization (IMPORTANT for TinyML)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()

with open("gesture_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TFLite model saved!")

# =========================
# 6. DOWNLOAD MODEL
# =========================
from google.colab import files
files.download("gesture_model.tflite")
