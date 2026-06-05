# app/model_utils.py
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import json

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', 'dish_classifier.h5')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, '..', 'model', 'class_names.json')

# --- Load Model ---
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# --- Load Class Names ---
try:
    with open(CLASS_NAMES_PATH, 'r') as f:
        CLASS_NAMES = json.load(f)
    print("✅ Loaded class names:", CLASS_NAMES)
except Exception as e:
    print(f"❌ Error loading class names: {e}")
    CLASS_NAMES = []


def predict_dish_from_image(img_file):
    """
    Predict the dish name from an uploaded image file (Streamlit UploadedFile or path).
    Returns: (dish_name, confidence)
    """
    if model is None or not CLASS_NAMES:
        return "Model or class names not loaded", 0.0

    try:
        # Open and resize image
        if not isinstance(img_file, str):
            img = Image.open(img_file).convert("RGB")
        else:
            img = tf.keras.utils.load_img(img_file, target_size=(224, 224))

        img = img.resize((224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

        # Predict
        preds = model.predict(img_array)
        class_idx = np.argmax(preds[0])
        confidence = float(np.max(preds[0]))
        predicted_class = CLASS_NAMES[class_idx]

        print(f"Predicted: {predicted_class} ({confidence:.2f})")
        return predicted_class, confidence

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return "Prediction Error", 0.0
