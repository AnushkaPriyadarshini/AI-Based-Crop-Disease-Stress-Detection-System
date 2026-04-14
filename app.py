# Load the trained model
from flask import Flask, render_template, request , redirect, url_for 
import requests
import os
import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow import keras

image = keras.preprocessing.image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"

# Ensure upload folder exists

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)



# Load the trained model
model = tf.keras.models.load_model('plant_disease_model1.h5')

crop_mapping= [
    'Apple','Apple', 'Apple','Apple',
    'Corn','Corn','Corn','Corn',
    'Grape','Grape','Grape','Grape',
    'Orange',
    'Peach','Peach',
    'Bell Pepper', 'Bell pepper',
    'Potato','Potato','Potato',
    'Strawberry','Strawberry',
    'Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Tomato',
]

# Mapping of disease labels to their respective crops
disease_labels = [
    'Apple scab','Black rot', 'Cedar apple rust','Apple healthy',
    'Cercospora leaf spot Gray leaf spot','Common rust', 'Northern Leaf Blight','healthy',
    'Black rot','Esca (Black Measles)', 'Leaf blight (Isariopsis Leaf Spot)','healthy',
    'Huanglongbing (Citrus greening)',
    'Bacterial spot','healthy',
    'Bacterial spot' , 'healthy',
    'Early blight','Late blight','healthy',
    'healthy' , 'Leaf scorch',
    'Bacterial spot','Early blight','healthy','Late blight','Leaf Mold','Septoria leaf spot',
    'Spider mites (Two-spotted spider mite)','Target Spot','Tomato mosaic virus', 'Tomato Yellow Leaf Curl Virus'
    
]

# Load genetic modification data
genetic_modifications = {
    'Late blight': [
        '1. CRISPR-Cas9 to target genes for resistance to Phytophthora infestans     2. Genetic engineering to overexpress the Rpi-blb2 gene for late blight resistance      3. Introduction of resistance from wild Solanum species'
    ],
    'Early blight': [
        ' 1. Transgenic potato expressing Bacillus thuringiensis (Bt) toxin '

        '   2. Engineering for resistance to Alternaria solani using synthetic biology '

        '  3. Expression of antifungal peptides (e.g., Chitinases) for controlling Alternaria'
    ],
    'Common rust': [
        '1. RNA interference (RNAi) to silence the gene expression of the rust pathogen'

        '  2. Overexpression of Co1 resistance gene from wild maize species'

        '  3. Use of genetically modified maize with high resistance to Puccinia sorghi'
    ],
    'Northern Leaf Blight': [
        '1. Introduction of resistance genes such as Htn1 using CRISPR-Cas9'

        '  2. Expression of ToxA resistance genes through transgenic approaches'

        '  3. Use of maize lines with enhanced immunity from natural sources'
    ],
    'Tomato mosaic virus': [
        '1. Genetic modification for resistance to Tomato mosaic virus using RNAi'

        '  2. Transgenic tomatoes expressing a protein that blocks virus replication'

        '  3. CRISPR-based resistance targeting viral replication machinery'
    ],
    'Tomato Yellow Leaf Curl Virus': [
        '1. Use of viral RNA silencing through transgenic tomatoes'

        '  2. Incorporation of TYLCV resistance genes into tomato genome using gene editing'

        '  3. Genetic modifications that boost the tomato plant’s immune response against TYLCV'
    ],
    'Bacterial spot': [
        '1. Overexpression of antimicrobial peptides to combat Xanthomonas'

        '  2. Expression of resistance proteins (e.g., R genes) for improved immunity'

        '  3. Genetic modification to activate systemic acquired resistance pathways'
    ],
    'Apple scab': [
        '1. Engineering of apples to express Vf gene for scab resistance'

        '  2. CRISPR-edited apple varieties with improved resistance to Venturia inaequalis'

        '  3. Genetic modifications to increase phenolic compounds that inhibit fungal growth'
    ],
    'Cedar apple rust': [
        '1. Expression of Cr1 resistance gene in apple trees to combat rust'

        '  2. Development of apple varieties resistant to Gymnosporangium via gene editing'

        '  3. Genetic engineering for enhanced resistance to rust pathogens using pathogen-derived resistance'
    ]
}
API_KEY = "bfc1a21674f2fe9623f21598d0f5398b"

sensitivity_thresholds = {
    'Potato': {'Late blight': 2, 'Early blight': 1},
    'Corn': {'Common rust': 1, 'Northern Leaf Blight': 2},
    'Tomato': {'Tomato mosaic virus': 3, 'Tomato Yellow Leaf Curl Virus': 2, 'Bacterial spot': 1},
    'Apple': {'Apple scab': 2, 'Cedar apple rust': 1},
    'Grape': {'Black rot': 2, 'Esca (Black Measles)': 3},
    'Orange': {'Haunglongbing (Citrus greening)': 3},
    'Strawberry': {'Leaf scorch': 2},
    'Peach': {'Bacterial spot': 1},
    'Cherry': {'Leaf blight (Isariopsis Leaf Spot)': 1},
    'Bell Pepper': {'Bacterial spot': 1}
}

# Get location from IP
def get_ip_location():
    try:
        ip_response = requests.get("https://ipinfo.io").json()
        loc = ip_response.get('loc', '0,0').split(',')
        lat, lon = map(float, loc)
        return lat, lon
    except Exception as e:
        print(f"⚠️ Error fetching IP location: {e}")
        return None, None

# Fetch weather data
def get_weather(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        temperature = response.get('main', {}).get('temp', None)
        humidity = response.get('main', {}).get('humidity', None)
        weather_desc = response.get('weather', [{}])[0].get('description', 'N/A')

        if temperature is None or humidity is None:
            print("⚠️ Incomplete weather data received.")
            return None, None, weather_desc

        return temperature, humidity, weather_desc

    except Exception as e:
        print(f"⚠️ Error fetching weather: {e}")
        return None, None, 'N/A'

# Calculate severity score based on weather
def calculate_severity_score(temperature, humidity, weather_desc):
    if temperature is None or humidity is None:
        return 0

    severity_score = 0

    # Temperature-based scoring
    if temperature < 10 or temperature > 35:
        severity_score += 3
    elif 10 <= temperature < 20 or 30 <= temperature <= 35:
        severity_score += 2
    else:
        severity_score += 1
    
    # Humidity-based scoring
    if humidity > 80:
        severity_score += 3
    elif 50 <= humidity <= 80:
        severity_score += 2
    else:
        severity_score += 1

    # Weather condition scoring
    weather_conditions = ['rain', 'storm', 'snow', 'drizzle', 'thunderstorm', 'hail', 'fog']
    if any(condition in weather_desc.lower() for condition in weather_conditions):
        severity_score += 3

    return severity_score

# Get severity risk for each crop-disease pair
def get_severity_score(crop, disease, severity_score):
    if crop in sensitivity_thresholds and disease in sensitivity_thresholds[crop]:
        threshold = sensitivity_thresholds[crop][disease]

        if severity_score >= threshold + 1:
            return "🔴 High Risk"
        elif severity_score == threshold:
            return "🟠 Moderate Risk"
        else:
            return "🟢 Low Risk"
    else:
        return "❓ No Disease"


@app.route('/')
def home():
    return render_template('body.html')

@app.route('/predict', methods=['POST'])
def predict():

    file = request.files['image']  
    
    
    
    if request.method == "POST":
        if "image" not in request.files or request.files["image"].filename == "":
            # No file uploaded, return empty results
            return render_template("body.html", name="", disease="", severity="", genetic_suggestions="")

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]


    predicted_disease = disease_labels[predicted_class]
    genetic_suggestions = genetic_modifications.get(predicted_disease, ['No genetic modification available'])
    crop_name = crop_mapping[predicted_class]


    # Get IP location and weather data
    lat, lon = get_ip_location()
    if lat and lon:
        temp, humidity, weather_desc = get_weather(lat, lon)

        if temp is not None and humidity is not None:
            # Calculate severity score
            severity_score = calculate_severity_score(temp, humidity, weather_desc)

            severity_label = get_severity_score(crop_name, predicted_disease, severity_score)


    
    print(f"Predicted class index: {predicted_class}")
    print(f"Predicted disease: {disease_labels[predicted_class]}")
    print(f"Predicted Crop :{crop_name}")
    print(f"Severity of the Crop :{severity_label}")
    print(f"Predicted genetic modification: {genetic_suggestions}")
    print(f"Temperature of your location :{temp}")





    return render_template('body.html',
                           name = crop_name,
                           disease = predicted_disease,
                           severity = severity_label,
                           genetic_suggestions = "<br>".join(genetic_suggestions))

    
 
   


if __name__ == '__main__':
    app.run(debug=True)

