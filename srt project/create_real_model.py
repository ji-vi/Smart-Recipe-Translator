# create_real_model.py
import tensorflow as tf
from keras import layers, models
import os
import json

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, "data", "train")
VAL_DIR = os.path.join(BASE_DIR, "data", "val")
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "dish_classifier.h5")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")

# --- Hyperparameters ---
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10  # can increase for better accuracy

# --- Load datasets ---
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

# ✅ Save class names **before** mapping normalization
CLASS_NAMES = train_ds.class_names
print("Detected classes:", CLASS_NAMES)

# Save class names to JSON for later use
with open(CLASS_NAMES_PATH, "w") as f:
    json.dump(CLASS_NAMES, f)
print(f"Class names saved to {CLASS_NAMES_PATH}")

# --- Normalize pixel values ---
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# --- Model ---
num_classes = len(CLASS_NAMES)
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=IMG_SIZE+(3,)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# --- Train ---
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# --- Save model ---
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
