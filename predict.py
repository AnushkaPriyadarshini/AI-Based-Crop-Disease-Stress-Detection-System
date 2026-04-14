import numpy as np
import cv2
import sys
from tensorflow import keras

# Load the trained model
model = keras.models.load_model("plant_disease_model.h5")

# Class labels (Update these based on your dataset)
class_labels = [
    "Apple Scab", "Apple Black Rot", "Apple Cedar Rust", "Apple Healthy",
    "Blueberry Healthy", "Cherry Powdery Mildew", "Cherry Healthy",
    "Corn Cercospora Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight",
    "Corn Healthy", "Grape Black Rot", "Grape Esca", "Grape Leaf Blight", "Grape Healthy",
    "Orange Haunglongbing", "Peach Bacterial Spot", "Peach Healthy",
    "Pepper Bacterial Spot", "Pepper Healthy", "Potato Early Blight",
    "Potato Late Blight", "Potato Healthy", "Raspberry Healthy", "Soybean Healthy",
    "Squash Powdery Mildew", "Strawberry Leaf Scorch", "Strawberry Healthy",
    "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Late Blight",
    "Tomato Leaf Mold", "Tomato Septoria Leaf Spot", "Tomato Spider Mites",
    "Tomato Target Spot", "Tomato Yellow Leaf Curl Virus", "Tomato Mosaic Virus",
    "Tomato Healthy"
]

# Function to preprocess image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found or cannot be read!")
        sys.exit(1)
    
    img = cv2.resize(img, (224, 224))  # Resize to model input size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to make a prediction
def predict_disease(image_path):
    img = preprocess_image(image_path)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions) * 100

    print(f"Predicted Disease: {class_labels[predicted_class]}")
    print(f"Confidence: {confidence:.2f}%")

# Run the script with an image path argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    predict_disease(image_path)
