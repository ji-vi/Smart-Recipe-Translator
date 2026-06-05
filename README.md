# 🍽️ Smart Recipe Translator

A deep learning-powered web application that identifies food dishes from images or text, retrieves corresponding recipes, translates them into multiple languages, and generates downloadable recipe PDFs. The project combines **Computer Vision, NLP, and Web Development** into a unified system.

---

## 📌 Overview

Smart Recipe Translator is designed to simplify access to global recipes by eliminating language barriers and enabling image-based dish recognition. Users can upload a food image or enter a dish name to receive structured recipe details in their preferred language.

---

## ✨ Key Features

- 📷 **Image-based Dish Recognition** using CNN model  
- 🔍 **Text-based Recipe Search**  
- 🍲 **Recipe Retrieval** via external APIs  
- 🌐 **Multi-language Translation Support**  
- 📄 **PDF Export of Recipes**  
- 🖥️ **Interactive Web Interface using Streamlit**  

---

## 🧠 Tech Stack

**Frontend**
- Streamlit

**Backend / Core**
- Python

**Machine Learning**
- TensorFlow / Keras (CNN model)
- OpenCV (image preprocessing)

**APIs**
- Google Translate API (language translation)
- Spoonacular / TheMealDB (recipe data)

---

## ⚙️ System Workflow
Input (Image / Text)

↓

Dish Classification (CNN Model)

↓

Recipe Fetching (API Integration)

↓

Translation Module

↓

PDF Generation + UI Display


---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/smart-recipe-translator.git
cd smart-recipe-translator
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python model/create_real_model.py
```
### 4. Run the application
```bash
streamlit run app/streamlit_app.py
```

## ⚠️ Notes
💠API keys are not included for security reasons

💠Trained model files are excluded due to GitHub size limits

💠Model can be regenerated using the training script









