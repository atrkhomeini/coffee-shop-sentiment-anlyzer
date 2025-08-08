# app/main.py
import io
import pickle
import pandas as pd
from pandas.errors import ParserError
import numpy as np
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from wordcloud import WordCloud # <-- ADD THIS IMPORT
import base64 # <-- ADD THIS IMPORT

# --- Project Imports ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import MODEL_PATH, TOKENIZER_PATH, MAX_LENGTH
from src.data_preprocessing import TextCleaner
from src.gemini_client import generate_insights

# --- App Initialization ---
app = FastAPI(title="SentimienKopi.com Sentiment Analysis API")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load ML Components on Startup ---
model = None
tokenizer = None
cleaner = None

@app.on_event("startup")
def load_ml_components():
    global model, tokenizer, cleaner
    try:
        model = load_model(MODEL_PATH)
        with open(TOKENIZER_PATH, 'rb') as handle:
            tokenizer = pickle.load(handle)
        cleaner = TextCleaner()
        print("✅ Model, tokenizer, and cleaner loaded successfully.")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not load ML components on startup: {e}")

# --- Helper Function for Word Cloud ---
def create_wordcloud(text_series):
    """Generates a word cloud image from a series of text."""
    full_text = ' '.join(text_series.dropna())
    if not full_text:
        return None
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(full_text)
    
    # Convert to image bytes
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    
    # Encode as Base64 string
    return base64.b64encode(img_bytes).decode('utf-8')

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_and_suggest")
async def process_and_suggest(
    file: UploadFile = File(...),
    text_column: str = Query(..., description="The name of the column with review text.")
):
    if not all([model, tokenizer, cleaner]):
        raise HTTPException(status_code=503, detail="ML components are not available.")

    try:
        contents = await file.read()
        decoded_contents = contents.decode('utf-8')
        
        try:
            df = pd.read_csv(io.StringIO(decoded_contents))
        except ParserError:
            df = pd.read_csv(io.StringIO(decoded_contents), delimiter=';')

        if text_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found.")

        # --- 1. Sentiment Analysis ---
        df_processed = df.copy()
        df_processed['cleaned_text'] = df_processed[text_column].apply(cleaner.clean)
        
        sequences = tokenizer.texts_to_sequences(df_processed['cleaned_text'])
        padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')
        
        predictions = model.predict(padded_sequences)
        sentiment_indices = np.argmax(predictions, axis=1)
        
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        df_processed['sentiment'] = [sentiment_map[idx] for idx in sentiment_indices]

        # --- 2. Gemini Insights ---
        positive_reviews = df_processed[df_processed['sentiment'] == 'positive'][text_column].dropna().tolist()
        negative_reviews = df_processed[df_processed['sentiment'] == 'negative'][text_column].dropna().tolist()
        summary, suggestions = generate_insights(positive_reviews, negative_reviews)
        
        # --- 3. Prepare Data for Frontend ---
        output_df = df_processed.drop(columns=['cleaned_text'])
        
        # Data for preview table (first 10 rows)
        preview_data = output_df.head(10).to_dict(orient='records')
        
        # Data for pie chart
        sentiment_counts = output_df['sentiment'].value_counts().to_dict()
        
        # Data for word cloud
        wordcloud_image_base64 = create_wordcloud(df_processed['cleaned_text'])
        
        # Full CSV data for download
        csv_data = output_df.to_csv(index=False)

        return JSONResponse(content={
            "summary": summary,
            "suggestions": suggestions,
            "csv_data": csv_data,
            "preview_data": preview_data,
            "sentiment_counts": sentiment_counts,
            "wordcloud_image": wordcloud_image_base64
        })

    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")
