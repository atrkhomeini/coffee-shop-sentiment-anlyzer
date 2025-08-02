<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RasaKopi.ai - Project Documentation</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .section-title {
            @apply text-3xl font-bold text-gray-800 mb-6 border-b-2 border-gray-200 pb-2;
        }
        .card {
            @apply bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-700">

    <div class="container mx-auto max-w-4xl p-4 sm:p-8">

        <!-- Header -->
        <header class="text-center mb-12">
            <h1 class="text-5xl font-extrabold text-gray-900 mb-2">RasaKopi.ai ☕</h1>
            <div class="flex justify-center items-center space-x-2 mt-4">
                <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
                <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
                <img src="https://img.shields.io/badge/python-3.10-blueviolet" alt="Python Version">
            </div>
        </header>

        <!-- Overview -->
        <section class="mb-12">
            <h2 class="section-title">📖 Overview</h2>
            <p class="text-lg leading-relaxed">
                RasaKopi.ai is a full-stack web application designed to provide powerful sentiment analysis for Indonesian coffee shop reviews. In a competitive market, understanding customer feedback is crucial. This tool empowers coffee shop owners to move beyond manual review analysis by offering an automated MLOps pipeline. Users can upload a CSV file of raw customer reviews and receive not only a detailed sentiment breakdown (positive, negative, neutral) but also AI-generated summaries and actionable business suggestions to improve their service and offerings.
            </p>
        </section>

        <!-- Key Features -->
        <section class="mb-12">
            <h2 class="section-title">✨ Key Features</h2>
            <div class="grid md:grid-cols-2 gap-6">
                <div class="card">
                    <h3 class="text-xl font-bold mb-2">📊 Got a bunch of reviews?</h3>
                    <p>Just toss your CSV file in! It doesn't matter if you have a few or a few thousand, it'll handle it.</p>
                </div>
                <div class="card">
                    <h3 class="text-xl font-bold mb-2">🧹 It cleans up the messy text.</h3>
                    <p>This tool is pretty smart! It gets rid of weird characters, figures out Indonesian slang, and removes boring filler words.</p>
                </div>
                <div class="card">
                    <h3 class="text-xl font-bold mb-2">🤖 Figures out the vibe.</h3>
                    <p>We built our own little AI that reads everything and tells you if people are happy (Positive), unhappy (Negative), or just in-between (Neutral).</p>
                </div>
                <div class="card">
                    <h3 class="text-xl font-bold mb-2">💡 Get the inside scoop from an AI.</h3>
                    <p>We use Google's Gemini AI to give you the rundown on what everyone's saying and provide solid, helpful tips on how to improve.</p>
                </div>
                 <div class="card md:col-span-2">
                    <h3 class="text-xl font-bold mb-2">📥 Download your results.</h3>
                    <p>You can grab a new CSV file with all the answers! It has your original reviews plus the new sentiment labels, all neat and tidy.</p>
                </div>
            </div>
        </section>

        <!-- Technology Stack -->
        <section class="mb-12">
            <h2 class="section-title">🛠️ Technology Stack</h2>
            <div class="bg-white p-4 rounded-lg shadow-md overflow-x-auto">
                <table class="w-full text-left">
                    <thead>
                        <tr class="border-b">
                            <th class="p-4 font-semibold text-lg">Category</th>
                            <th class="p-4 font-semibold text-lg">Technology</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b">
                            <td class="p-4 font-medium">Backend</td>
                            <td class="p-4 flex items-center gap-2 flex-wrap"><img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI"></td>
                        </tr>
                        <tr class="border-b">
                            <td class="p-4 font-medium">Frontend</td>
                            <td class="p-4 flex items-center gap-2 flex-wrap"><img src="https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white" alt="HTML5"> <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?logo=tailwindcss&logoColor=white" alt="Tailwind CSS"> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black" alt="JavaScript"></td>
                        </tr>
                        <tr class="border-b">
                            <td class="p-4 font-medium">ML/AI</td>
                            <td class="p-4 flex items-center gap-2 flex-wrap"><img src="https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white" alt="TensorFlow"> <img src="https://img.shields.io/badge/Keras-D00000?logo=keras&logoColor=white" alt="Keras"> <img src="https://img.shields.io/badge/Google_Gemini-8E44AD?logo=google&logoColor=white" alt="Google Gemini"></td>
                        </tr>
                        <tr class="border-b">
                            <td class="p-4 font-medium">Database</td>
                            <td class="p-4"><img src="https://img.shields.io/badge/Google_BigQuery-669DF6?logo=googlebigquery&logoColor=white" alt="Google BigQuery"></td>
                        </tr>
                        <tr>
                            <td class="p-4 font-medium">Deployment</td>
                            <td class="p-4"><img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker"></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- MLOps Workflow -->
        <section class="mb-12">
            <h2 class="section-title">🔄 MLOps Workflow</h2>
            <ol class="list-decimal list-inside space-y-4 text-lg">
                <li><strong>Data Storage 🗄️:</strong> Labeled training data is stored and versioned in a dedicated Google BigQuery table, providing a single source of truth.</li>
                <li><strong>Model Training 🧠:</strong> The <code>src/train.py</code> script orchestrates the training pipeline, fetching data, preprocessing it, and training the model.</li>
                <li><strong>Artifact Versioning 📦:</strong> Upon successful training, the script saves the trained model (<code>sentiment_model.h5</code>) and the tokenizer (<code>tokenizer.pkl</code>).</li>
                <li><strong>Inference Service 🚀:</strong> The FastAPI web application loads these artifacts on startup to serve predictions and insights.</li>
            </ol>
        </section>

        <!-- Project Structure -->
        <section class="mb-12">
            <h2 class="section-title">📂 Project Structure</h2>
            <div class="bg-gray-800 text-white p-6 rounded-lg shadow-md font-mono text-sm">
                <pre><code>rasakopi-ai/
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
└── 📄 README.md</code></pre>
            </div>
        </section>

        <!-- Local Setup -->
        <section class="mb-12">
            <h2 class="section-title">💻 Local Setup and Installation</h2>
            <div class="space-y-6">
                <div>
                    <h3 class="text-xl font-semibold mb-2">1. Clone the Repository</h3>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code>git clone https://github.com/atrkhomeini/Sentiment-Analysis-of-4-Brand-Coffee-Shop-in-Indonesia-Using-CNN-BiLSTM.git
cd Sentiment-Analysis-of-4-Brand-Coffee-Shop-in-Indonesia-Using-CNN-BiLSTM</code></pre>
                </div>
                <div>
                    <h3 class="text-xl font-semibold mb-2">2. Create and Activate a Conda Environment</h3>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code>conda create --name rasakopi python=3.10
conda activate rasakopi</code></pre>
                </div>
                <div>
                    <h3 class="text-xl font-semibold mb-2">3. Install Dependencies</h3>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code>pip install -r requirements.txt</code></pre>
                </div>
                <div>
                    <h3 class="text-xl font-semibold mb-2">4. Set Up Authentication</h3>
                    <p class="mb-2">Authenticate the gcloud CLI for BigQuery access:</p>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code>gcloud auth application-default login</code></pre>
                    <p class="mt-4 mb-2">Set your Gemini API key as an environment variable:</p>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code># On Mac/Linux
export GEMINI_API_KEY="your_actual_api_key"

# On Windows
set GEMINI_API_KEY="your_actual_api_key"</code></pre>
                </div>
            </div>
        </section>

        <!-- Usage -->
        <section class="mb-12">
            <h2 class="section-title">▶️ Usage</h2>
            <div class="space-y-6">
                <div>
                    <h3 class="text-xl font-semibold mb-2">1. Training a New Model</h3>
                    <p class="mb-2">Run the training script to generate the model and tokenizer files.</p>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code>python src/train.py</code></pre>
                </div>
                <div>
                    <h3 class="text-xl font-semibold mb-2">2. Running the Web Application</h3>
                    <p class="mb-2">Start the FastAPI server.</p>
                    <pre class="bg-gray-800 text-white p-4 rounded-lg"><code>uvicorn app.main:app --reload</code></pre>
                    <p class="mt-2">Navigate to <a href="http://127.0.0.1:8000" class="text-blue-600 hover:underline">http://127.0.0.1:8000</a> in your browser.</p>
                </div>
            </div>
        </section>

        <!-- Future Improvements -->
        <section>
            <h2 class="section-title">🤔 Future Improvements</h2>
            <ul class="list-disc list-inside space-y-2 text-lg">
                <li>Real-time analytics dashboard to visualize sentiment trends.</li>
                <li>Direct database connection for users instead of CSV uploads.</li>
                <li>Automated CI/CD pipeline for model retraining and deployment.</li>
            </ul>
        </section>

    </div>
</body>
</html>
