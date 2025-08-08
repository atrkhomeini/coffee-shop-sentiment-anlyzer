# src/gemini_client.py
import google.generativeai as genai
from src.config import GEMINI_API_KEY # This will be None if not found
import time

# --- Configure the Gemini API ---
# This configuration now only happens if the key was successfully loaded.
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    model = None # Set model to None if no key is found

def generate_insights(positive_reviews, negative_reviews):
    """
    Generates both a summary and actionable suggestions using the Gemini API.
    """
    # --- ADDED: Check if the model was initialized ---
    if not model:
        error_msg = "Gemini API key not configured. Cannot generate insights."
        return error_msg, error_msg

    if not positive_reviews and not negative_reviews:
        return "Tidak ada ulasan untuk dianalisis.", "Tidak ada ulasan negatif untuk memberikan saran."

    prompt = f"""
    You are a business consultant for a coffee shop in Indonesia.
    Analyze the following customer reviews.

    **Positive Reviews:**
    - {"- ".join(positive_reviews[:15]) if positive_reviews else "N/A"} 

    **Negative Reviews:**
    - {"- ".join(negative_reviews[:15]) if negative_reviews else "N/A"}

    Based on the reviews, provide the following in two distinct sections:

    **Section 1: Ringkasan Ulasan (Review Summary)**
    Summarize the main positive themes and the main negative themes in Bahasa Indonesia.

    **Section 2: Saran Perbaikan (Actionable Suggestions)**
    Based ONLY on the negative reviews, provide 3-4 concrete, actionable suggestions.
    """

    # Using exponential backoff for retries
    for n in range(5):
        try:
            response = model.generate_content(prompt)
            
            full_text = response.text
            summary_part, suggestions_part = "Gagal mem-parsing respons.", "Gagal mem-parsing respons."

            if "Saran Perbaikan" in full_text:
                parts = full_text.split("Saran Perbaikan")
                summary_part = parts[0].replace("Ringkasan Ulasan", "").strip()
                suggestions_part = parts[1].strip()
            elif "Ringkasan Ulasan" in full_text:
                 summary_part = full_text.replace("Ringkasan Ulasan", "").strip()

            return summary_part, suggestions_part
        except Exception as e:
            print(f"Gemini API attempt {n+1} failed with error: {e}")
            time.sleep(2 ** n)
    
    return "Gagal menghasilkan ringkasan setelah beberapa kali percobaan.", "Gagal menghasilkan saran setelah beberapa kali percobaan."
