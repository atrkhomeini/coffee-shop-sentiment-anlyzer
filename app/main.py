# app/main.py
import io
import pickle
import pandas as pd
from pandas.errors import ParserError
import numpy as np
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from wordcloud import WordCloud
import base64
import markdown2

# --- Project Imports ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import MODEL_PATH, TOKENIZER_PATH, MAX_LENGTH
from src.data_preprocessing import TextCleaner
from src.gemini_client import generate_insights

# --- App Initialization ---
app = FastAPI(title="SentimenKopi.com Sentiment Analysis API")
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
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(full_text)
    
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    
    return base64.b64encode(img_bytes).decode('utf-8')

# --- API Endpoints ---
@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url="/home")

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/process_and_suggest", response_class=HTMLResponse)
async def process_and_suggest(
    request: Request,
    file: UploadFile = File(...),
    text_column: str = Form(...)
):
    if not all([model, tokenizer, cleaner]):
        raise HTTPException(status_code=503, detail="ML components are not available.")

    try:
        contents = await file.read()
        try:
            decoded_contents = contents.decode('utf-8')
        except UnicodeDecodeError:
            decoded_contents = contents.decode('latin-1')

        try:
            df = pd.read_csv(io.StringIO(decoded_contents))
        except ParserError:
            df = pd.read_csv(io.StringIO(decoded_contents), delimiter=';')

        if text_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found.")

        # --- Analysis Pipeline ---
        df_processed = df.copy()
        df_processed['cleaned_text'] = df_processed[text_column].apply(cleaner.clean)
        
        sequences = tokenizer.texts_to_sequences(df_processed['cleaned_text'])
        padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')
        
        predictions = model.predict(padded_sequences)
        sentiment_indices = np.argmax(predictions, axis=1)
        
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        df_processed['sentiment'] = [sentiment_map[idx] for idx in sentiment_indices]

        positive_reviews = df_processed[df_processed['sentiment'] == 'positive'][text_column].dropna().tolist()
        negative_reviews = df_processed[df_processed['sentiment'] == 'negative'][text_column].dropna().tolist()
        summary, suggestions = generate_insights(positive_reviews, negative_reviews)
        
        # --- Prepare Data for Frontend ---
        output_df = df_processed.drop(columns=['cleaned_text'])
        
        sentiment_counts = output_df['sentiment'].value_counts().to_dict()
        wordcloud_image_base64 = create_wordcloud(df_processed['cleaned_text'])
        csv_data = output_df.to_csv(index=False)

        # Convert Markdown to HTML
        summary_html = markdown2.markdown(summary)
        suggestions_html = markdown2.markdown(suggestions)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "summary": summary_html,
            "suggestions": suggestions_html,
            "csv_data": csv_data,
            "sentiment_counts": sentiment_counts,
            "wordcloud_image": wordcloud_image_base64,
            "filename": file.filename
        })

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "detail": str(e)}, status_code=500)

@app.get("/result")
async def result_page_not_accessible(request: Request):
    return RedirectResponse(url="/home")
