# streamlit_app.py
import streamlit as st
from PIL import Image
from pdf_utils import save_recipe_as_pdf
from recipe_utils import fetch_themealdb_recipe  # using TheMealDB instead of Spoonacular
from translation_utils import translate_recipe, translate_ui_text
from model_utils import predict_dish_from_image
import os
from googletrans import LANGUAGES

# --- Page Config ---
st.set_page_config(page_title="Smart Recipe Translator", page_icon="🍴", layout="wide")

# --- Session State ---
if "preferred_lang" not in st.session_state:
    st.session_state.preferred_lang = "en"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "last_recipe_en" not in st.session_state:
    st.session_state.last_recipe_en = {"ingredients": [], "instructions": ""}
if "translated_recipe" not in st.session_state:
    st.session_state.translated_recipe = {"ingredients": [], "instructions": ""}
if "option_selected" not in st.session_state:
    st.session_state.option_selected = None
if "dish_name" not in st.session_state:
    st.session_state.dish_name = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "translated_recipes_cache" not in st.session_state:
    st.session_state.translated_recipes_cache = {}

# --- Theme Functions ---
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

def get_theme_colors():
    if st.session_state.theme == "light":
        return {
            "primary_bg": "#f9fafc",
            "input_bg": "#ffffff",
            "box_bg": "#ffffff",
            "text_color": "#2c3e50",
            "subtitle_color": "#7f8c8d",
            "button_bg": "#2563eb",
            "button_hover": "#1e40af",
            "option_color": "#2c3e50",
        }
    else:
        return {
            "primary_bg": "#111827",
            "input_bg": "#1f2937",
            "box_bg": "#1f2937",
            "text_color": "#f3f4f6",
            "subtitle_color": "#9ca3af",
            "button_bg": "#3b82f6",
            "button_hover": "#2563eb",
            "option_color": "#f3f4f6",
        }

def apply_theme():
    colors = get_theme_colors()
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background-color: {colors['primary_bg']} !important;
        color: {colors['text_color']} !important;
    }}
    div.block-container {{
        background-color: {colors['primary_bg']} !important;
        color: {colors['text_color']} !important;
        padding: 1rem 2rem;
    }}
    .stButton>button {{
        background-color:{colors['button_bg']} !important;
        color:white !important;
        height:40px; width:auto; padding:0 10px;
        margin-top:0.5rem;
    }}
    .stButton>button:hover {{
        background-color:{colors['button_hover']} !important;
    }}
    input, textarea, .stTextInput>div>div>input {{
        background-color:{colors['input_bg']} !important;
        color:{colors['text_color']} !important;
    }}
    .recipe-box {{
        background-color:{colors['box_bg']} !important;
        color:{colors['text_color']} !important;
        padding:1rem; border-radius:12px; box-shadow:0px 2px 6px rgba(0,0,0,0.15);
        margin-top:1rem; font-size:1rem; max-height:400px; overflow-y:auto; border:1px solid rgba(0,0,0,0.1);
        white-space: pre-line; -webkit-overflow-scrolling: touch;
    }}
    .option-box {{
        padding: 0.5rem 1rem; border-radius:8px; cursor:pointer;
        border:1px solid rgba(0,0,0,0.2); margin-right:0.5rem;
        display:inline-block; margin-top:0.5rem;
        background-color:{colors['box_bg']}; color:{colors['option_color']};
        text-align:center;
        min-width:120px; max-width:200px;
    }}
    .option-box:hover {{
        border-color:{colors['button_bg']};
    }}
    img {{
        border-radius:10px; margin-bottom:1rem; width:100%; max-width:400px; height:auto;
    }}
    /* Navbar fix */
    .navbar-container {{
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: {colors['primary_bg']};
        padding: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# --- UI Texts ---
UI_TEXT = {
    "title": "Smart Recipe Translator",
    "upload_image": "🍴 Upload Image",
    "enter_dish": "✏️ Enter Dish Name",
    "original_recipe": "Original Recipe",
    "translated_recipe": "Translated Recipe",
    "translate_button": "🌍 Translate Recipe",
    "pdf_button": "💾 Generate PDF",
    "download_pdf": "⬇️ Download Recipe PDF",
    "placeholder": "Please upload an image or enter a dish name to get started.",
}

# --- Navbar ---
with st.container():
    st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown(f"<h2>{UI_TEXT['title']}</h2>", unsafe_allow_html=True)
    with col2:
        st.button("🌙" if st.session_state.theme=="light" else "🌞", on_click=toggle_theme)
        lang_list = list(LANGUAGES.values())
        selected_lang = st.selectbox("Language", options=lang_list, index=lang_list.index("english"), label_visibility="collapsed")
        lang_code = [k for k,v in LANGUAGES.items() if v==selected_lang][0]
        st.session_state.preferred_lang = lang_code
        # Auto-translate UI text
        UI_TEXT = translate_ui_text(UI_TEXT, dest_lang=lang_code)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Input Options (Blue Buttons) ---
st.markdown("<div class='input-option-container' style='display:flex; gap:10px; justify-content:flex-start;'>", unsafe_allow_html=True)
option_col1, option_col2 = st.columns([1,1])
with option_col1:
    if st.button(UI_TEXT["upload_image"]):
        st.session_state.option_selected = "Upload Image"
with option_col2:
    if st.button(UI_TEXT["enter_dish"]):
        st.session_state.option_selected = "Enter Dish Name"
st.markdown("</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg","png","jpeg"], label_visibility="collapsed") if st.session_state.option_selected=="Upload Image" else None
dish_name_input = st.text_input("", label_visibility="collapsed") if st.session_state.option_selected=="Enter Dish Name" else None

# --- Handle Inputs ---
if st.session_state.option_selected == "Upload Image" and uploaded_file:
    st.session_state.uploaded_image = uploaded_file
    img = Image.open(st.session_state.uploaded_image)
    # Resize dynamically
    max_width = 400
    aspect_ratio = img.height / img.width
    display_width = min(img.width, max_width)
    display_height = int(display_width * aspect_ratio)
    st.image(img, width=display_width)

    predicted = predict_dish_from_image(st.session_state.uploaded_image)
    st.session_state.dish_name = predicted[0] if isinstance(predicted, tuple) else predicted
    st.success(f"🍴 Predicted Dish: {st.session_state.dish_name}")

elif st.session_state.option_selected == "Enter Dish Name" and dish_name_input:
    st.session_state.dish_name = dish_name_input
    st.success(f"✏️ Dish Selected: {st.session_state.dish_name}")

# --- Fetch Recipe ---
if st.session_state.dish_name:
    recipe_data = fetch_themealdb_recipe(st.session_state.dish_name)  # returns dict with 'ingredients' and 'instructions'
    ingredients = recipe_data.get("ingredients", [])
    instructions = recipe_data.get("instructions", "")

    if not ingredients and not instructions:
        st.warning("⚠️ No recipe found for this dish. Please try another dish name or image.")
    else:
        st.session_state.last_recipe_en = {"ingredients": ingredients, "instructions": instructions}

        # --- Original Recipe ---
        st.markdown(f"### {UI_TEXT['original_recipe']}")
        full_recipe = "\n".join(ingredients) + ("\n\nInstructions:\n" + instructions if instructions else "")
        st.markdown(f"<div class='recipe-box'>{full_recipe}</div>", unsafe_allow_html=True)

        # --- Translate & PDF Buttons ---
        col_translate, col_pdf = st.columns(2)
        with col_translate:
            if st.button(UI_TEXT["translate_button"]):
                lang = st.session_state.preferred_lang
                # Use cached translation if available
                if lang in st.session_state.translated_recipes_cache:
                    translated_text = st.session_state.translated_recipes_cache[lang]
                else:
                    translated_text = translate_recipe(full_recipe, lang)
                    st.session_state.translated_recipes_cache[lang] = translated_text

                st.session_state.translated_recipe = {
                    "ingredients": translated_text.splitlines(),
                    "instructions": translated_text.splitlines()
                }

        if st.session_state.translated_recipe.get("ingredients") or st.session_state.translated_recipe.get("instructions"):
            st.markdown(f"### {UI_TEXT['translated_recipe']}")
            translated_text = "\n".join(st.session_state.translated_recipe["ingredients"]) + \
                              "\n\nInstructions:\n" + \
                              "\n".join(st.session_state.translated_recipe["instructions"])
            st.markdown(f"<div class='recipe-box'>{translated_text}</div>", unsafe_allow_html=True)

            with col_pdf:
                if st.button(UI_TEXT["pdf_button"]):
                    pdf_path = save_recipe_as_pdf(
                        st.session_state.dish_name,
                        full_recipe,
                        translated_text,
                        lang_code=st.session_state.preferred_lang
                    )
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label=UI_TEXT["download_pdf"],
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
else:
    st.markdown(f"<div class='recipe-box' style='text-align:center; font-style:italic;'>{UI_TEXT['placeholder']}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<br><br><hr><p style='text-align:center; font-size:0.9rem;'>Developed by Jivi</p>", unsafe_allow_html=True)
st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
