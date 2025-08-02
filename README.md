# RasaKopi.ai ☕

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python Version](https://img.shields.io/badge/python-3.10-blueviolet)

## 📖 Overview

RasaKopi.ai is a full-stack web application designed to provide powerful sentiment analysis for Indonesian coffee shop reviews. In a competitive market, understanding customer feedback is crucial. This tool empowers coffee shop owners to move beyond manual review analysis by offering an automated MLOps pipeline. Users can upload a CSV file of raw customer reviews and receive not only a detailed sentiment breakdown (positive, negative, neutral) but also AI-generated summaries and actionable business suggestions to improve their service and offerings.

## ✨ Key Features

### 📊 Got a bunch of reviews?
Just toss your CSV file in! It doesn't matter if you have a few or a few thousand, it'll handle it.

### 🧹 It cleans up the messy text
This tool is pretty smart! It gets rid of weird characters, figures out Indonesian slang, and removes boring filler words.

### 🤖 Figures out the vibe
We built our own little AI that reads everything and tells you if people are happy (Positive), unhappy (Negative), or just in-between (Neutral).

### 💡 Get the inside scoop from an AI
We use Google's Gemini AI to give you the rundown on what everyone's saying and provide solid, helpful tips on how to improve.

### 📥 Download your results
You can grab a new CSV file with all the answers! It has your original reviews plus the new sentiment labels, all neat and tidy.

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Backend | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) |
| Frontend | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?logo=tailwindcss&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black) |
| ML/AI | ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-D00000?logo=keras&logoColor=white) ![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E44AD?logo=google&logoColor=white) |
| Database | ![Google BigQuery](https://img.shields.io/badge/Google_BigQuery-669DF6?logo=googlebigquery&logoColor=white) |
| Deployment | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) |

## 🔄 MLOps Workflow

1. **Data Storage 🗄️:** Labeled training data is stored and versioned in a dedicated Google BigQuery table, providing a single source of truth.

2. **Model Training 🧠:** The `src/train.py` script orchestrates the training pipeline, fetching data, preprocessing it, and training the model.

3. **Artifact Versioning 📦:** Upon successful training, the script saves the trained model (`sentiment_model.h5`) and the tokenizer (`tokenizer.pkl`).

4. **Inference Service 🚀:** The FastAPI web application loads these artifacts on startup to serve predictions and insights.

## 📂 Project Structure

```
rasakopi-ai/
├── 📁 app/
│   ├── 📄 main.py
│   └── 📁 templates/
│       └── 📄 index.html
│
├── 📁 src/
│   ├── 📄 config.py
│   ├── 📄 data_preprocessing.py
│   ├── 📄 gemini_client.py
│   ├── 📄 model.py
│   └── 📄 train.py
│
├── 📁 models/
│   ├── 📄 sentiment_model.h5
│   └── 📄 tokenizer.pkl
│
├── 📄 requirements.txt
└── 📄 README.md
```

## 💻 Local Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/atrkhomeini/Sentiment-Analysis-of-4-Brand-Coffee-Shop-in-Indonesia-Using-CNN-BiLSTM.git
cd Sentiment-Analysis-of-4-Brand-Coffee-Shop-in-Indonesia-Using-CNN-BiLSTM
```

### 2. Create and Activate a Conda Environment

```bash
conda create --name rasakopi python=3.10
conda activate rasakopi
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Authentication

Authenticate the gcloud CLI for BigQuery access:

```bash
gcloud auth application-default login
```

Set your Gemini API key as an environment variable:

```bash
# On Mac/Linux
export GEMINI_API_KEY="your_actual_api_key"

# On Windows
set GEMINI_API_KEY="your_actual_api_key"
```

## ▶️ Usage

### 1. Training a New Model

Run the training script to generate the model and tokenizer files.

```bash
python src/train.py
```

### 2. Running the Web Application

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## 🤔 Future Improvements

- Real-time analytics dashboard to visualize sentiment trends.
- Direct database connection for users instead of CSV uploads.
- Automated CI/CD pipeline for model retraining and deployment.
- Preview 10 data result in web