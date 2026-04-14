📌 Overview

This project is an AI-powered web application that detects crop diseases and environmental stress conditions using image processing and machine learning. It helps in early identification of plant issues and provides actionable insights for better crop management.

🚀 Features

🌿 Crop disease detection using image input
📊 Environmental stress detection (drought, water stress)
🌦️ Weather-based severity analysis
🧬 Genetic modification suggestions based on crop and disease
🤖 Intelligent recommendations using Random Forest
⚡ Real-time prediction via web interface


🧠 Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
ML/DL: TensorFlow (CNN), OpenCV, Scikit-learn

⚙️ How It Works

1. User uploads a crop image

2. Image is processed using OpenCV

3. CNN model predicts disease/stress

4. Weather data is fetched for severity analysis

5. Random Forest provides suggestions & genetic insights

6. Results displayed on web UI

📁 Model & Dataset Note

The dataset is organized into train and validation (valid) directories for model training and evaluation.
Due to large file size constraints, the training dataset and trained model file is not included in this repository.
You can download the dataset from Kaggle: New Plant Diseases Dataset (Augmented) and place it in the appropriate folders before training.
