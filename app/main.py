# app/main.py
import io
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- Project Imports ---
import sys
import os
# Add the project root to the Python path to allow imports from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import MODEL_PATH, TOKENIZER_PATH, MAX_LENGTH
from src.data_preprocessing import TextCleaner # <-- UPDATED: Import the class
from src.gemini_client import generate_insights

# --- App Initialization ---
app = FastAPI(title="SentimenKopi.ai Sentiment Analysis API")
templates = Jinja2Templates(directory="templates")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load ML Components on Startup ---
# These components will be loaded once when the app starts for efficiency.
model = None
tokenizer = None
cleaner = None # <-- ADDED: Cleaner instance

@app.on_event("startup")
def load_ml_components():
    """Load all necessary ML components when the application starts."""
    global model, tokenizer, cleaner
    try:
        model = load_model(MODEL_PATH)
        with open(TOKENIZER_PATH, 'rb') as handle:
            tokenizer = pickle.load(handle)
        cleaner = TextCleaner() # <-- UPDATED: Initialize the TextCleaner
        print("✅ Model, tokenizer, and cleaner loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading ML components: {e}")
        # The app will run, but endpoints will fail until this is fixed.

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_and_suggest")
async def process_and_suggest(
    file: UploadFile = File(...),
    text_column: str = Query(..., description="The name of the column with review text.")
):
    """
    Analyzes sentiment, generates insights with Gemini, and returns all results.
    """
    if not all([model, tokenizer, cleaner]):
        raise HTTPException(status_code=503, detail="ML components are not available. Please check server logs.")

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        if text_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found.")

        # --- 1. Sentiment Analysis (CNN-BiLSTM Model) ---
        df_processed = df.copy()
        # UPDATED: Use the cleaner instance for consistent preprocessing
        df_processed['cleaned_text'] = df_processed[text_column].apply(cleaner.clean)
        
        sequences = tokenizer.texts_to_sequences(df_processed['cleaned_text'])
        padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')
        
        predictions = model.predict(padded_sequences)
        sentiment_indices = np.argmax(predictions, axis=1)
        
        # UPDATED: Map the 3-class output indices to labels
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        df_processed['sentiment'] = [sentiment_map[idx] for idx in sentiment_indices]

        # --- 2. Insight Generation (Gemini API) ---
        positive_reviews = df_processed[df_processed['sentiment'] == 'positive'][text_column].dropna().tolist()
        negative_reviews = df_processed[df_processed['sentiment'] == 'negative'][text_column].dropna().tolist()

        # Call the Gemini client
        summary, suggestions = generate_insights(positive_reviews, negative_reviews)
        
        # --- 3. Prepare Response ---
        # Don't include the intermediate cleaned text in the final CSV
        output_df = df_processed.drop(columns=['cleaned_text'])
        csv_data = output_df.to_csv(index=False)

        return JSONResponse(content={
            "summary": summary,
            "suggestions": suggestions,
            "csv_data": csv_data
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")

