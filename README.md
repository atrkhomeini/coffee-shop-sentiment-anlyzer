# SentimenKopi.com

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python Version](https://img.shields.io/badge/python-3.9-blueviolet)

## Overview

SentimenKopi.com is a full-stack web application designed to help coffee shop owners in Indonesia unlock valuable insights from customer reviews. By simply uploading a CSV file of raw feedback, users can leverage a sophisticated MLOps pipeline that performs sentiment analysis, generates concise summaries, and provides actionable business suggestions. This tool transforms qualitative customer feedback into a quantitative asset, enabling data-driven decisions to improve service, products, and overall customer experience.

## Key Features

*   **CSV File Upload**: Easily upload and process customer reviews in batch via a user-friendly web interface.
*   **Advanced Text Preprocessing**: Includes normalization of Indonesian slang and removal of stopwords to ensure high-quality analysis.
*   **3-Class Sentiment Analysis**: Classifies reviews into "Positive," "Negative," or "Neutral" categories using a powerful CNN-BiLSTM model built with TensorFlow/Keras.
*   **AI-Powered Insights**: Generates insightful summaries and actionable business suggestions from the reviews using the Google Gemini API.
*   **Downloadable Results**: Export the enriched data, including sentiment labels and AI-generated insights, as a CSV file for further analysis.

## Technology Stack

*   **Backend**: Python, FastAPI
*   **Frontend**: HTML, Tailwind CSS, JavaScript
*   **Machine Learning**: TensorFlow (Keras)
*   **Generative AI**: Google Gemini API
*   **Data Source**: Google BigQuery
*   **Deployment**: Docker

## MLOps Workflow

The project follows a complete MLOps pipeline to ensure a seamless flow from data to insights:

1.  **Data Storage and Versioning**: The training data, consisting of labeled Indonesian coffee shop reviews, is stored and versioned in Google BigQuery.
2.  **Model Training**: The `src/train.py` script fetches the data from BigQuery, preprocesses it, and trains the CNN-BiLSTM sentiment analysis model.
3.  **Artifacts Generation**: After training, the script saves the trained model (`.h5` file) and the tokenizer (`.pkl` file) as artifacts in the `models/` directory.
4.  **Application Loading**: The FastAPI web application loads these trained artifacts on startup, making them ready for inference.
5.  **Inference and Insights**: When a user uploads a CSV file, the application uses the loaded model and tokenizer to perform sentiment prediction on the reviews. It then calls the Gemini API to generate summaries and suggestions based on the analysis.

## Project Structure

```
coffee-shop-sentiment-analyzer/
├── app/                # Contains the FastAPI web application
│   ├── __init__.py
│   ├── main.py         # FastAPI server logic
│   └── templates/
│       └── index.html  # User-facing HTML file
│
├── src/                # Core machine learning and data processing scripts
│   ├── __init__.py
│   ├── config.py
│   ├── data_preprocessing.py
│   ├── model.py
│   ├── train.py        # Script for offline model training
│   └── gemini_client.py # Module for all Gemini API calls
│
├── models/             # Stored outputs from the training script
│   ├── sentiment_model.h5
│   └── tokenizer.pkl
│
├── data/               # Labeled data for training
│   └── raw/
│
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Local Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/SentimenKopi.com.git
    cd SentimenKopi.com
    ```

2.  **Create and activate a Conda virtual environment:**
    ```bash
    conda create --name rasakopi-env python=3.9
    conda activate rasakopi-env
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up authentication:**
    *   **For Google BigQuery:**
        ```bash
        gcloud auth application-default login
        ```
    *   **For Google Gemini API:**
        Set your Gemini API key as an environment variable.
        ```bash
        export GEMINI_API_KEY="your-api-key"
        ```

## Usage

### Training a New Model

To train the sentiment analysis model on the latest data from Google BigQuery, run the training script:

```bash
python src/train.py
```

### Running the Web Application

To start the FastAPI server, run the following command:

```bash
uvicorn app.main:app --reload
```

Navigate to `http://127.0.0.1:8000` in your web browser to access the application.

## Future Improvements

*   **Real-time Analytics Dashboard**: A dashboard to visualize sentiment trends and key themes from the reviews in real-time.
*   **Support for More Data Sources**: Integration with social media platforms and other review sites to gather more customer feedback.
*   **Automated Model Retraining**: A CI/CD pipeline to automatically retrain and deploy the model when new data is available.
