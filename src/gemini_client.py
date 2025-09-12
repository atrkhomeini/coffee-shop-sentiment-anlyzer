# src/gemini_client.py
import google.generativeai as genai
from src.config import GEMINI_API_KEY
import time
import re

# --- Configure the Gemini API ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    model = None

def generate_insights(positive_reviews, negative_reviews):
    """
    Generates both a summary and actionable suggestions using the Gemini API.
    """
    if not model:
        error_msg = "Gemini API key not configured. Cannot generate insights."
        return error_msg, error_msg

    if not positive_reviews and not negative_reviews:
        return "Tidak ada ulasan untuk dianalisis.", "Tidak ada ulasan negatif untuk memberikan saran."

    prompt = f"""
    You are an expert market analyst and business consultant specializing in the Food & Beverage industry in Indonesia, with a focus on coffee shops.
    Your goal is to provide the coffee shop owner with deep, actionable insights that can directly improve their business.

    **Format your entire response using Markdown in Bahasa Indonesia.** Use headings, bold text, and bullet points to create a clear and easy-to-read report.

    Analyze the following customer reviews:

    **Positive Reviews:**
    - {"- ".join(positive_reviews[:20]) if positive_reviews else "N/A"} 

    **Negative Reviews:**
    - {"- ".join(negative_reviews[:20]) if negative_reviews else "N/A"}

    Based on this data, generate a concise business report with two distinct sections:

    ---

    ### Ringkasan Ulasan & Analisis Tema
    - **Tema Positif:** Identify the top 2-3 specific things customers love. Use bold for the theme category (e.g., **Produk**, **Pelayanan**).
    - **Tema Negatif:** Identify the top 2-3 specific things customers complain about. Use bold for the theme category.

    ---

    ### Saran Perbaikan Prioritas
    Based ONLY on the negative themes, provide the top 3 most impactful and actionable recommendations. For each recommendation, provide a brief rationale explaining the business benefit.

    Example Format for Recommendations:
    - **Tingkatkan Kecepatan Pelayanan:** Latih barista untuk meracik pesanan populer dengan lebih efisien.
        - **Alasan:** Mengurangi waktu tunggu akan meningkatkan kepuasan pelanggan dan mempercepat perputaran meja.
    - **[Rekomendasi Berikutnya]**
        - **Alasan:** [Penjelasan]

    ---
    """

    for n in range(5):
        try:
            response = model.generate_content(prompt)
            
            full_text = response.text
            summary_part, suggestions_part = "Gagal mem-parsing respons.", "Gagal mem-parsing respons."

            # Use regex for more robust splitting, ignoring case and handling variations in markdown headings
            splitter = re.compile(r'#*\s*Saran Perbaikan Prioritas', re.IGNORECASE)
            parts = splitter.split(full_text)

            if len(parts) > 1:
                summary_raw = parts[0]
                suggestions_part = parts[1].strip()

                # Clean up the summary part by removing its heading
                summary_cleaner = re.compile(r'#*\s*Ringkasan Ulasan & Analisis Tema', re.IGNORECASE)
                summary_part = summary_cleaner.sub('', summary_raw).strip()
            else:
                # Fallback if splitting fails
                summary_cleaner = re.compile(r'#*\s*Ringkasan Ulasan & Analisis Tema', re.IGNORECASE)
                if summary_cleaner.search(full_text):
                    summary_part = summary_cleaner.sub('', full_text).strip()

            # Ensure parts are not empty after stripping
            if not summary_part:
                 summary_part = "Ringkasan tidak tersedia."
            if not suggestions_part:
                 suggestions_part = "Saran tidak tersedia."


            return summary_part, suggestions_part
        except Exception as e:
            print(f"Gemini API attempt {n+1} failed with error: {e}")
            time.sleep(2 ** n)
    
    return "Gagal menghasilkan ringkasan setelah beberapa kali percobaan.", "Gagal menghasilkan saran setelah beberapa kali percobaan."
