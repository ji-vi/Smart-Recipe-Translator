# translation_utils.py
from googletrans import Translator

translator = Translator()

def translate_text(text, dest_lang="hi"):
    """
    Translate a text string into the target language.
    """
    if dest_lang == "en" or not text.strip():
        return text
    try:
        return translator.translate(text, dest=dest_lang).text
    except Exception as e:
        print("Translation error:", e)
        return text

def translate_recipe(recipe_text, dest_lang="hi"):
    """
    Translate a full recipe string (ingredients + instructions) line by line.
    Preserves the separation between ingredients and instructions.
    """
    if dest_lang == "en" or not recipe_text.strip():
        return recipe_text

    # Split into lines
    lines = recipe_text.splitlines()
    translated_lines = []
    for line in lines:
        line = line.strip()
        if line:
            translated_lines.append(translate_text(line, dest_lang))
        else:
            translated_lines.append("")

    return "\n".join(translated_lines)

def translate_ui_text(ui_dict, dest_lang="hi"):
    """
    Translate UI text dictionary dynamically.
    """
    if dest_lang == "en":
        return ui_dict
    translated = {}
    for key, value in ui_dict.items():
        try:
            translated[key] = translator.translate(value, src="en", dest=dest_lang).text
        except Exception as e:
            print(f"UI translation error for '{key}': {e}")
            translated[key] = value  # fallback to English
    return translated
