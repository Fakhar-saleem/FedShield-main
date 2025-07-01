import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
import pytesseract  # Tesseract OCR
from tensorflow.keras.preprocessing.sequence import pad_sequences
# Load Text Classifier components
# ------------------------------------------------------------------
# Load the saved text classification model
text_model = tf.keras.models.load_model('./models/text_model.h5')

# Load word index for text preprocessing
with open('./word_index.json', 'r') as f:
    word_index = json.load(f)

# Text preprocessing parameters (match your training configuration)
vocab_size = 3000
max_length = 120
padding_type = 'post'
truncation_type = 'post'
oov_tok = '<OOV>'

# Text preprocessing function
def preprocess_text(text):
    # Remove stopwords (use your original stopwords list)
    stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]  # Your stopwords list from Text_Classifier1.ipynb
    words = text.split()
    filtered_words = [w for w in words if w.lower() not in stopwords]
    processed_text = ' '.join(filtered_words)

    # Convert text to sequence and pad
    sequence = [min(word_index.get(word, 1), vocab_size - 1) for word in processed_text.split()]  # 1 = OOV index
    padded = pad_sequences([sequence], maxlen=max_length,
                          padding=padding_type, truncating=truncation_type)
    return padded

# Load Image Classifier
# ------------------------------------------------------------------
image_model = tf.keras.models.load_model('./models/image_model.h5')

# Image preprocessing function
def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((150, 150))  # Match your model's input size
    img_array = np.array(img) / 255.0  # Normalization
    return np.expand_dims(img_array, axis=0)

# Combined Prediction Function
# ------------------------------------------------------------------
def combined_prediction(image_path, threshold=0.5):
    # 1. Image Classification
    print("imagetest")
    processed_image = preprocess_image(image_path)
    image_pred = image_model.predict(processed_image)[0][0]
    print("imagetestdone")

    # 2. Text Extraction and Classification
    print("texttest")

    extracted_text = pytesseract.image_to_string(Image.open(image_path))
    text_pred = 0.0  # Default non-sensitive
    
    if extracted_text.strip():
        processed_text = preprocess_text(extracted_text)
        text_pred = text_model.predict(processed_text)[0][0]
    print("texttestdone")
    print("image_pred:", image_pred)
    print("text_pred:", text_pred)
    # 3. Combine predictions (OR logic)
    combined_pred = 1 if (image_pred > threshold) or (text_pred > threshold) else 0
    print("combined_pred:", combined_pred)
    return combined_pred

# Accuracy Calculation Function
# ------------------------------------------------------------------
# def calculate_combined_accuracy(test_images_dir, true_labels):
#     correct = 0
#     total = len(true_labels)

#     for idx, (img_path, label) in enumerate(test_images_dir.items()):
#         pred, true = combined_prediction(img_path, label)
#         if pred == true:
#             correct += 1

#         print(f"Processed {idx+1}/{total} - Current Accuracy: {correct/(idx+1):.2%}", end='\r')

#     final_accuracy = correct / total
#     print(f"\nFinal Combined Accuracy: {final_accuracy:.2%}")
#     return final_accuracy

# # Usage Example
# # ------------------------------------------------------------------
# # Create a dictionary of {image_path: true_label}
# def load_test_data(test_dir):
#     test_data = {}

#     # Define class subdirectories (adjust based on your folder structure)
#     sensitive_dir = os.path.join(test_dir, "sensitive")
#     nonsensitive_dir = os.path.join(test_dir, "nonsensitive")

#     # Load sensitive images (label 1)
#     for filename in os.listdir(sensitive_dir):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             img_path = os.path.join(sensitive_dir, filename)
#             test_data[img_path] = 1

#     # Load non-sensitive images (label 0)
#     for filename in os.listdir(nonsensitive_dir):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             img_path = os.path.join(nonsensitive_dir, filename)
#             test_data[img_path] = 0

#     return test_data

# # Usage
# test_dir = "./validation"
# test_data = load_test_data(test_dir)

# # Calculate combined accuracy
# calculate_combined_accuracy(test_data, test_data.values())