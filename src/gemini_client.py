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

    # --- UPDATED: New, more sophisticated "Expert Analyst" prompt ---
    prompt = f"""
    You are an expert market analyst and business consultant specializing in the Food & Beverage industry in Indonesia, with a focus on coffee shops. Your goal is to provide the coffee shop owner with deep, actionable insights that can directly improve their business.

    Analyze the following customer reviews provided.

    **Positive Reviews:**
    - {"- ".join(positive_reviews[:20]) if positive_reviews else "N/A"} 

    **Negative Reviews:**
    - {"- ".join(negative_reviews[:20]) if negative_reviews else "N/A"}

    Based on this data, generate a concise business report in Bahasa Indonesia with two distinct sections:

    ---

    **Section 1: Ringkasan Ulasan & Analisis Tema**
    1.  **Analisis Tema Positif:** Identify the top 2-3 specific things customers love. Categorize each theme (e.g., Produk, Pelayanan, Suasana, Harga). For example: "Produk - Kopi Gula Aren sangat disukai karena rasanya yang konsisten."
    2.  **Analisis Tema Negatif:** Identify the top 2-3 specific things customers complain about. Categorize each theme clearly. For example: "Pelayanan - Waktu tunggu pesanan yang lama menjadi keluhan utama."

    ---

    **Section 2: Saran Perbaikan Prioritas**
    Based ONLY on the negative themes, provide the top 3 most impactful and actionable recommendations for the business owner. For each recommendation, provide a brief "Rationale" (Mengapa ini penting) explaining the business benefit. Present this as a numbered list.

    Example Format for Recommendations:
    1.  **Tingkatkan Kecepatan Pelayanan:** Latih barista untuk meracik pesanan populer dengan lebih efisien.
        * **Mengapa ini penting:** Mengurangi waktu tunggu akan meningkatkan kepuasan pelanggan dan mempercepat perputaran meja, yang berpotensi meningkatkan pendapatan.
    2.  **[Rekomendasi Berikutnya]**
        * **Mengapa ini penting:** [Penjelasan]

    ---
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
