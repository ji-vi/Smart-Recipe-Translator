# create_demo_model.py
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Flatten, Dense
import os

# --- Create a simple 3-class model ---
model = Sequential([
    Flatten(input_shape=(224, 224, 3)),
    Dense(3, activation='softmax')  # 3 classes: Pasta, Dosa, Burger
])

# --- Ensure 'model' folder exists ---
os.makedirs("model", exist_ok=True)

# --- Save model to model/ folder ---
model_path = os.path.join("model", "dish_classifier.h5")
model.save(model_path)
print(f"Demo model saved at: {model_path}")
