import face_recognition
import pickle
import os
import numpy as np

def get_face_embedding(image_path):
    """
    Loads an image and returns the 128-dimension face encoding.
    Returns None if no face is found or if multiple faces are found (to avoid ambiguity).
    """
    try:
        # Load the image into a numpy array
        image = face_recognition.load_image_file(image_path)
        
        # specific_model="hog" is faster, "cnn" is more accurate (but requires GPU/CUDA for speed)
        # We stick to default (hog) for CPU compatibility.
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            print(f"⚠️ No face detected in {image_path}")
            return None
        
        if len(face_locations) > 1:
            print(f"⚠️ Multiple faces detected in {image_path}. Please use an image with a single subject.")
            return None

        # Generate the encoding (embedding)
        # known_face_encodings returns a list, we take the first one
        encoding = face_recognition.face_encodings(image, face_locations)[0]
        return encoding

    except Exception as e:
        print(f"❌ Error processing image {image_path}: {e}")
        return None

def save_embedding(embedding, output_path):
    """
    Serializes the embedding (numpy array) and saves it to a pickle file.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump(embedding, f)
        # print(f"💾 Embedding saved to {output_path}") # Uncomment for verbose
        return True
    except Exception as e:
        print(f"❌ Error saving embedding: {e}")
        return False

def load_embedding(input_path):
    """
    Loads a serialized embedding from a pickle file.
    """
    try:
        with open(input_path, 'rb') as f:
            embedding = pickle.load(f)
        return embedding
    except Exception as e:
        print(f"❌ Error loading embedding {input_path}: {e}")
        return None

# --- Test Block (Run this file directly to test) ---
if __name__ == "__main__":
    # Create a dummy image file for testing if one doesn't exist
    # (In a real scenario, put a real jpg in data/images/ to test)
    print("--- Testing Encoder ---")
    print("Note: To test this properly, ensure you have a valid image at 'data/images/test.jpg'")
    
    # Example usage:
    # test_img = "data/images/test.jpg"
    # emb = get_face_embedding(test_img)
    # if emb is not None:
    #     save_embedding(emb, "data/embeddings/test.pkl")
    #     print("Test complete: Embedding generated and saved.")