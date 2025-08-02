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

# --- Project Imports ---
# This allows the script to find and import from the 'src' directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import MODEL_PATH, TOKENIZER_PATH, MAX_LENGTH
from src.data_preprocessing import TextCleaner
from src.gemini_client import generate_insights

# --- App Initialization ---
app = FastAPI(title="RasaKopi.ai Sentiment Analysis API")

# This creates a robust path to the 'templates' directory, ensuring it can always be found.
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

# --- CORS Middleware ---
# This allows your frontend HTML to communicate with this backend server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods
    allow_headers=["*"], # Allows all headers
)

# --- Global variables to hold the loaded ML components ---
model = None
tokenizer = None
cleaner = None

@app.on_event("startup")
def load_ml_components():
    """
    Load all necessary ML components once when the application starts up.
    This is efficient as it avoids reloading for every user request.
    """
    global model, tokenizer, cleaner
    try:
        model = load_model(MODEL_PATH)
        with open(TOKENIZER_PATH, 'rb') as handle:
            tokenizer = pickle.load(handle)
        cleaner = TextCleaner()
        print("✅ Model, tokenizer, and cleaner loaded successfully.")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not load ML components on startup: {e}")
        # In a real production app, you might want to handle this more gracefully.

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main index.html page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_and_suggest")
async def process_and_suggest(
    file: UploadFile = File(...),
    text_column: str = Query(..., description="The name of the column containing the review text.")
):
    """
    The main endpoint that processes an uploaded CSV file, analyzes sentiment,
    generates insights with Gemini, and returns all results as JSON.
    """
    if not all([model, tokenizer, cleaner]):
        raise HTTPException(status_code=503, detail="ML components are not available. Please check server logs.")

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        contents = await file.read()
        decoded_contents = contents.decode('utf-8')
        
        # Robust CSV Parsing: Try comma delimiter first, then fall back to semicolon.
        try:
            df = pd.read_csv(io.StringIO(decoded_contents))
        except ParserError:
            print("Comma delimiter failed. Trying semicolon...")
            df = pd.read_csv(io.StringIO(decoded_contents), delimiter=';')

        if text_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found. Please check spelling and case.")

        # --- 1. Sentiment Analysis (CNN-BiLSTM Model) ---
        df_processed = df.copy()
        df_processed['cleaned_text'] = df_processed[text_column].apply(cleaner.clean)
        
        sequences = tokenizer.texts_to_sequences(df_processed['cleaned_text'])
        padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')
        
        predictions = model.predict(padded_sequences)
        sentiment_indices = np.argmax(predictions, axis=1)
        
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        df_processed['sentiment'] = [sentiment_map[idx] for idx in sentiment_indices]

        # --- 2. Insight Generation (Gemini API) ---
        positive_reviews = df_processed[df_processed['sentiment'] == 'positive'][text_column].dropna().tolist()
        negative_reviews = df_processed[df_processed['sentiment'] == 'negative'][text_column].dropna().tolist()

        summary, suggestions = generate_insights(positive_reviews, negative_reviews)
        
        # --- 3. Prepare Response ---
        output_df = df_processed.drop(columns=['cleaned_text'])
        csv_data = output_df.to_csv(index=False)

        return JSONResponse(content={
            "summary": summary,
            "suggestions": suggestions,
            "csv_data": csv_data
        })

    except ParserError:
        raise HTTPException(status_code=400, detail="Could not parse the CSV file. Please ensure it is a valid CSV with either comma (,) or semicolon (;) delimiters.")
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")

