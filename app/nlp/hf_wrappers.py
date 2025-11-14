"""
Wrappers for HuggingFace emotion and sentiment models.
Provides simple, cached interfaces for inference.
"""

from transformers import pipeline
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmotionDetector:
    """Detects emotions using HuggingFace model."""
    
    MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
    
    def __init__(self):
        """Initialize emotion detection model."""
        logger.info(f"Loading emotion model: {self.MODEL_NAME}")
        self.model = pipeline(
            "text-classification",
            model=self.MODEL_NAME,
            top_k=None,
            device=-1  # CPU
        )
        logger.info("Emotion model loaded successfully")
    
    def detect(self, text: str) -> Dict:
        """
        Detect emotion in text.
        
        Args:
            text: Input text
            
        Returns:
            {
                'emotion': str (top emotion label),
                'confidence': float,
                'all_scores': List[Dict] (all emotions with scores)
            }
        """
        if not text or len(text.strip()) == 0:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'all_scores': []
            }
        
        # Truncate to model's max length
        text = text[:512]
        
        results = self.model(text)[0]
        
        # Sort by score descending
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        top_emotion = sorted_results[0]
        
        return {
            'emotion': top_emotion['label'],
            'confidence': round(top_emotion['score'], 3),
            'all_scores': [
                {'label': r['label'], 'score': round(r['score'], 3)}
                for r in sorted_results
            ]
        }


class SentimentDetector:
    """Detects sentiment using HuggingFace model."""
    
    MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
    
    def __init__(self):
        """Initialize sentiment detection model."""
        logger.info(f"Loading sentiment model: {self.MODEL_NAME}")
        self.model = pipeline(
            "sentiment-analysis",
            model=self.MODEL_NAME,
            device=-1  # CPU
        )
        logger.info("Sentiment model loaded successfully")
    
    def detect(self, text: str) -> Dict:
        """
        Detect sentiment in text.
        
        Args:
            text: Input text
            
        Returns:
            {
                'sentiment': str ('POSITIVE' or 'NEGATIVE'),
                'confidence': float
            }
        """
        if not text or len(text.strip()) == 0:
            return {
                'sentiment': 'NEUTRAL',
                'confidence': 0.0
            }
        
        # Truncate to model's max length
        text = text[:512]
        
        result = self.model(text)[0]
        
        return {
            'sentiment': result['label'],
            'confidence': round(result['score'], 3)
        }


if __name__ == "__main__":
    # Test the models
    print("Testing Emotion Detector...")
    emotion_detector = EmotionDetector()
    
    test_texts = [
        "I'm so happy today! Everything is going great!",
        "I feel terrible and can't stop crying",
        "This makes me so angry, I can't believe it",
        "I'm terrified of what might happen"
    ]
    
    for text in test_texts:
        result = emotion_detector.detect(text)
        print(f"\nText: '{text}'")
        print(f"Emotion: {result['emotion']} (confidence: {result['confidence']})")
        print(f"All scores: {result['all_scores'][:3]}")
    
    print("\n" + "="*80)
    print("\nTesting Sentiment Detector...")
    sentiment_detector = SentimentDetector()
    
    for text in test_texts:
        result = sentiment_detector.detect(text)
        print(f"\nText: '{text}'")
        print(f"Sentiment: {result['sentiment']} (confidence: {result['confidence']})")
