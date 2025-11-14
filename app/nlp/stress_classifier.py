"""
Custom stress level classifier using TF-IDF + SVM.
This will be trained on a custom dataset and loaded for inference.
"""

import joblib
import os
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StressClassifier:
    """Custom stress level classifier."""
    
    STRESS_LEVELS = ['low', 'medium', 'high']
    
    def __init__(self, model_path: str = None):
        """
        Initialize stress classifier.
        
        Args:
            model_path: Path to trained model directory containing vectorizer.joblib and model.joblib
        """
        self.model = None
        self.vectorizer = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            logger.warning("No trained model found. Using rule-based fallback.")
    
    def load_model(self, model_path: str):
        """Load trained model and vectorizer."""
        try:
            vectorizer_path = os.path.join(model_path, 'vectorizer.joblib')
            model_file_path = os.path.join(model_path, 'model.joblib')
            
            if os.path.exists(vectorizer_path) and os.path.exists(model_file_path):
                self.vectorizer = joblib.load(vectorizer_path)
                self.model = joblib.load(model_file_path)
                logger.info(f"Loaded stress model from {model_path}")
            else:
                logger.warning(f"Model files not found in {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.vectorizer = None
    
    def detect(self, text: str) -> Dict:
        """
        Detect stress level in text.
        
        Args:
            text: Input text
            
        Returns:
            {
                'stress_level': str ('low', 'medium', 'high'),
                'confidence': float,
                'all_scores': Dict[str, float]
            }
        """
        if not text or len(text.strip()) == 0:
            return {
                'stress_level': 'low',
                'confidence': 0.0,
                'all_scores': {'low': 0.0, 'medium': 0.0, 'high': 0.0}
            }
        
        # If model is loaded, use it
        if self.model and self.vectorizer:
            try:
                # Vectorize input
                features = self.vectorizer.transform([text])
                
                # Get prediction and probabilities
                prediction = self.model.predict(features)[0]
                probabilities = self.model.predict_proba(features)[0]
                
                # Map to stress levels
                stress_level = self.STRESS_LEVELS[prediction]
                confidence = float(probabilities[prediction])
                
                all_scores = {
                    self.STRESS_LEVELS[i]: float(probabilities[i])
                    for i in range(len(self.STRESS_LEVELS))
                }
                
                return {
                    'stress_level': stress_level,
                    'confidence': round(confidence, 3),
                    'all_scores': {k: round(v, 3) for k, v in all_scores.items()}
                }
            except Exception as e:
                logger.error(f"Error in model prediction: {e}")
                # Fall back to rule-based
        
        # Fallback: simple rule-based classifier
        return self._rule_based_detection(text)
    
    def _rule_based_detection(self, text: str) -> Dict:
        """
        Simple rule-based stress detection as fallback.
        
        Uses keyword matching and intensity markers.
        """
        text_lower = text.lower()
        
        # High stress indicators
        high_stress_keywords = [
            'overwhelmed', 'can\'t handle', 'breaking down', 'falling apart',
            'panic', 'crisis', 'desperate', 'unbearable', 'too much',
            'can\'t cope', 'drowning', 'crushing', 'suffocating'
        ]
        
        # Medium stress indicators
        medium_stress_keywords = [
            'stressed', 'anxious', 'worried', 'pressure', 'struggling',
            'exhausted', 'tired', 'burned out', 'tense', 'difficult',
            'challenging', 'overwhelming', 'busy'
        ]
        
        # Low stress indicators
        low_stress_keywords = [
            'okay', 'fine', 'managing', 'coping', 'handling', 'alright',
            'good', 'calm', 'relaxed', 'peaceful'
        ]
        
        # Count matches
        high_count = sum(1 for keyword in high_stress_keywords if keyword in text_lower)
        medium_count = sum(1 for keyword in medium_stress_keywords if keyword in text_lower)
        low_count = sum(1 for keyword in low_stress_keywords if keyword in text_lower)
        
        # Intensity markers (exclamation, caps, etc.)
        exclamation_count = text.count('!')
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        # Determine stress level
        if high_count > 0 or exclamation_count > 2 or caps_ratio > 0.3:
            stress_level = 'high'
            confidence = min(0.7 + (high_count * 0.1), 0.95)
        elif medium_count > 0 or exclamation_count > 0:
            stress_level = 'medium'
            confidence = min(0.6 + (medium_count * 0.1), 0.85)
        else:
            stress_level = 'low'
            confidence = 0.5 + (low_count * 0.1)
        
        return {
            'stress_level': stress_level,
            'confidence': round(min(confidence, 1.0), 3),
            'all_scores': {
                'high': round(high_count / max(high_count + medium_count + low_count, 1), 3),
                'medium': round(medium_count / max(high_count + medium_count + low_count, 1), 3),
                'low': round(low_count / max(high_count + medium_count + low_count, 1), 3)
            }
        }


if __name__ == "__main__":
    # Test the stress classifier
    classifier = StressClassifier()
    
    test_cases = [
        "I'm feeling okay, just a bit tired",
        "I'm so stressed with all this work, it's overwhelming",
        "I CAN'T HANDLE THIS ANYMORE! Everything is falling apart!",
        "Things are challenging but I'm managing",
        "I'm drowning in deadlines and can't cope"
    ]
    
    print("Stress Classification Test Cases:\n")
    for text in test_cases:
        result = classifier.detect(text)
        print(f"Text: '{text}'")
        print(f"Stress Level: {result['stress_level']} (confidence: {result['confidence']})")
        print(f"All scores: {result['all_scores']}")
        print("-" * 80)
