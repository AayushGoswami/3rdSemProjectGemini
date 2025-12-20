import unittest
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.encoder import get_face_embedding
from app.face_matcher import find_match

class TestFaceRecognition(unittest.TestCase):
    
    def test_embedding_generation(self):
        # NOTE: You need a real image at this path for the test to pass
        test_img = "data/images/test_subject.jpg" 
        if os.path.exists(test_img):
            emb = get_face_embedding(test_img)
            self.assertIsNotNone(emb)
            self.assertEqual(len(emb), 128)
        else:
            print("Skipping image test (file not found)")

if __name__ == '__main__':
    unittest.main()