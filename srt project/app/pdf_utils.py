# pdf_utils.py
from fpdf import FPDF
import os

def save_recipe_as_pdf(dish_name, original_text, translated_text=None, lang_code="en"):
    pdf = FPDF()
    pdf.add_page()

    # --- Use a Unicode font that supports Hindi/Marathi ---
    font_path = os.path.join(os.path.dirname(__file__), "NotoSansDevanagari-Regular.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError(
            "NotoSansDevanagari-Regular.ttf not found in the app directory. "
            "Please download it from Google Fonts and place it here."
        )

    pdf.add_font("Noto", "", font_path, uni=True)
    pdf.set_font("Noto", "", 12)

    # --- Title ---
    pdf.cell(0, 10, f"{dish_name}", ln=True, align="C")
    pdf.ln(5)

    # --- Original Recipe ---
    pdf.multi_cell(0, 8, f"Original Recipe (English):\n\n{original_text}")
    pdf.ln(5)

    # --- Translated Recipe ---
    if translated_text:
        pdf.multi_cell(0, 8, f"Translated Recipe:\n\n{translated_text}")

    # --- Save PDF ---
    pdf_folder = os.path.join(os.path.dirname(__file__), "pdfs")
    os.makedirs(pdf_folder, exist_ok=True)
    safe_dish_name = "".join(c for c in dish_name if c.isalnum() or c in (" ", "_")).rstrip()
    pdf_path = os.path.join(pdf_folder, f"{safe_dish_name}.pdf")
    pdf.output(pdf_path)

    return pdf_path
