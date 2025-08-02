# src/gemini_client.py
import google.generativeai as genai
from src.config import GEMINI_API_KEY
import time

# --- Configure the Gemini API ---
# This explicitly checks for the API key from your environment variable.
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running the app.")
    
genai.configure(api_key=GEMINI_API_KEY)

# --- Initialize the Generative Model ---
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_insights(positive_reviews, negative_reviews):
    """
    Generates both a summary and actionable suggestions using the Gemini API.
    """
    # Handle cases where there might be no reviews of a certain type
    if not positive_reviews and not negative_reviews:
        return "Tidak ada ulasan untuk dianalisis.", "Tidak ada ulasan negatif untuk memberikan saran."

    # Create the prompt, ensuring we don't send empty lists
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
    Format this as a short paragraph for positives and a short paragraph for negatives.

    **Section 2: Saran Perbaikan (Actionable Suggestions)**
    Based ONLY on the negative reviews, provide 3-4 concrete, actionable suggestions for the business owner to improve.
    If there are no negative reviews, state that.
    Present these as a bulleted list in Bahasa Indonesia.
    """

     # Using exponential backoff for retries
    for n in range(5): # Retry up to 5 times
        try:
            response = model.generate_content(prompt)
            
            full_text = response.text
            summary_part = "Ringkasan tidak dapat dibuat."
            suggestions_part = "Saran tidak dapat dibuat."

            if "Saran Perbaikan" in full_text:
                parts = full_text.split("Saran Perbaikan")
                summary_part = parts[0].replace("Ringkasan Ulasan", "").strip()
                suggestions_part = parts[1].strip()
            elif "Ringkasan Ulasan" in full_text:
                 summary_part = full_text.replace("Ringkasan Ulasan", "").strip()

            return summary_part, suggestions_part

        except Exception as e:
            print(f"Gemini API attempt {n+1} failed with error: {e}")
            time.sleep(2 ** n) # Exponential backoff: 1s, 2s, 4s, 8s
    
    # If all retries fail
    return "Gagal menghasilkan ringkasan setelah beberapa kali percobaan.", "Gagal menghasilkan saran setelah beberapa kali percobaan."

