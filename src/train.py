# src/train.py
import pandas as pd
import os
import sys

# Add the project root to the Python path to allow imports from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_preprocessing import TextCleaner
from src.model import build_model
import pickle
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- Project Imports ---
# Note: You might need to update MAX_LENGTH and add EMBEDDING_DIM to your config
from src.config import (
    GCP_PROJECT_ID,
    BIGQUERY_DATASET,
    BIGQUERY_TRAINING_TABLE,
    MODEL_PATH,
    TOKENIZER_PATH,
    MAX_LENGTH,
)

# --- Model Parameters from your Notebook ---
# Using a trainable embedding layer instead of GloVe for a self-contained pipeline
EMBEDDING_DIM = 300 
# MAX_LENGTH is imported from config, ensure it's set to 50

# --- Main Training Function ---
def train_model():
    """
    Fetches labeled data from BigQuery, trains the sentiment model,
    and saves the model and tokenizer artifacts.
    """
    print("--- Starting Model Training ---")

    # 1. Fetch Data from BigQuery
    print(f"Fetching data from BigQuery table: {GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TRAINING_TABLE}...")
    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
        # UPDATED: Query generic field names and filter out the header row.
        query = f"""
            SELECT string_field_1, string_field_4
            FROM `{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TRAINING_TABLE}`
            WHERE string_field_1 != 'Text' 
              AND string_field_4 IS NOT NULL 
              AND string_field_4 IN ('positive', 'negative', 'neutral')
        """
        df = client.query(query).to_dataframe()
        
        # UPDATED: Rename the generic columns to the expected names.
        df.rename(columns={'string_field_1': 'Text', 'string_field_4': 'Sentimen'}, inplace=True)
        
        print(f"✅ Successfully fetched {len(df)} rows.")
    except Exception as e:
        print(f"❌ Failed to fetch data from BigQuery: {e}")
        return

    # 2. Preprocess Data
    print("Cleaning and preprocessing text data...")
    cleaner = TextCleaner()  # Initialize the text cleaner
    df['cleaned_review'] = df['Text'].apply(cleaner.clean)
    
    # Map string labels to integers for 3 classes
    def map_sentiment(sentiment):
        sentiment = sentiment.lower()
        if sentiment == 'positive':
            return 2
        elif sentiment == 'neutral':
            return 1
        else: # 'negative'
            return 0
            
    df['sentiment_label'] = df['Sentimen'].apply(map_sentiment)
    
    reviews = df['cleaned_review'].values
    labels = df['sentiment_label'].values

    # 3. Tokenize and Pad Text
    print("Tokenizing and padding sequences...")
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(reviews)
    
    sequences = tokenizer.texts_to_sequences(reviews)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')

    # 4. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, labels, test_size=0.2, random_state=42, stratify=labels
    )
    print(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

    # 5. Build the CNN-BiLSTM Model
    # This call imports the architecture from src/model.py
    vocab_size = len(tokenizer.word_index) + 1
    model = build_model(vocab_size=vocab_size, embedding_dim=EMBEDDING_DIM, max_length=MAX_LENGTH)

    # 6. Train the Model
    print("Training the model...")
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=32, # From your notebook
        validation_data=(X_test, y_test),
        verbose=2
    )

    # 7. Evaluate the Model
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n✅ Training Complete!")
    print(f"   Test Accuracy: {accuracy:.4f}")
    print(f"   Test Loss: {loss:.4f}")

    # 8. Save Artifacts
    print(f"Saving model to: {MODEL_PATH}")
    model.save(MODEL_PATH)

    print(f"Saving tokenizer to: {TOKENIZER_PATH}")
    with open(TOKENIZER_PATH, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    print("\n--- Model training script finished successfully! ---")


if __name__ == '__main__':
    train_model()
