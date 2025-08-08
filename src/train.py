# src/train.py
import pandas as pd
import pickle
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- Project Imports ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import (
    GCP_PROJECT_ID,
    BIGQUERY_DATASET,
    BIGQUERY_TRAINING_TABLE,
    MODEL_PATH, # This will now be 'models/sentiment_model.keras'
    TOKENIZER_PATH,
    MAX_LENGTH,
)
from src.data_preprocessing import TextCleaner
from src.model import build_model

# --- Model Parameters ---
EMBEDDING_DIM = 300 

# --- Main Training Function ---
def train_model():
    print("--- Starting Model Training Pipeline ---")
    cleaner = TextCleaner()

    print(f"Fetching data from BigQuery table: {GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TRAINING_TABLE}...")
    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
        query = f"""
            SELECT string_field_1, string_field_4
            FROM `{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TRAINING_TABLE}`
            WHERE string_field_1 != 'Text' AND string_field_4 IS NOT NULL AND string_field_4 IN ('positive', 'negative', 'neutral')
        """
        df = client.query(query).to_dataframe()
        df.rename(columns={'string_field_1': 'Text', 'string_field_4': 'Sentimen'}, inplace=True)
        print(f"✅ Successfully fetched {len(df)} rows.")
    except Exception as e:
        print(f"❌ Failed to fetch data from BigQuery: {e}")
        return

    print("Cleaning and preprocessing text data...")
    df['cleaned_review'] = df['Text'].apply(cleaner.clean)
    
    def map_sentiment(sentiment):
        s = sentiment.lower()
        if s == 'positive': return 2
        elif s == 'neutral': return 1
        else: return 0
    df['sentiment_label'] = df['Sentimen'].apply(map_sentiment)
    
    reviews = df['cleaned_review'].values
    labels = df['sentiment_label'].values

    print("Tokenizing and padding sequences...")
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(reviews)
    sequences = tokenizer.texts_to_sequences(reviews)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')

    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    vocab_size = len(tokenizer.word_index) + 1
    model = build_model(vocab_size=vocab_size, embedding_dim=EMBEDDING_DIM, max_length=MAX_LENGTH)

    print("Training the model...")
    model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=2
    )

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n✅ Training Complete! Test Accuracy: {accuracy:.4f}")

    # The save command is the same, but because MODEL_PATH now ends in .keras,
    # it will use the new, more reliable format.
    print(f"Saving model to: {MODEL_PATH}")
    model.save(MODEL_PATH)

    print(f"Saving tokenizer to: {TOKENIZER_PATH}")
    with open(TOKENIZER_PATH, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    print("\n--- Model training pipeline finished successfully! ---")

if __name__ == '__main__':
    train_model()
