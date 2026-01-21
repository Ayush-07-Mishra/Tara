"""
Smart Response Engine - Optimized for 297K dataset
Fast category-based matching with semantic understanding
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
import random
import re
from collections import defaultdict


class SmartResponseEngine:
    """Intelligent response system with optimized category-based matching."""
    
    def __init__(self, dataset_path: str):
        """Initialize with conversation dataset."""
        print(f"Loading dataset from: {dataset_path}")
        self.dataset = self._load_dataset(dataset_path)
        print(f"✓ Loaded {len(self.dataset):,} conversations")
        
        # Build multiple indexes for fast lookup
        self.exact_index = {}  # Exact matches
        self.category_index = defaultdict(list)  # By category
        self.keyword_index = defaultdict(list)  # By keywords
        
        self._build_optimized_indexes()
        print(f"✓ Built optimized indexes: {len(self.exact_index):,} exact, {len(self.category_index)} categories")
        
    def _load_dataset(self, path: str) -> List[Dict]:
        """Load conversation dataset."""
        dataset_file = Path(path)
        if dataset_file.exists():
            with open(dataset_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _build_optimized_indexes(self):
        """Build multiple indexes for ultra-fast lookups."""
        print("Building optimized indexes...")
        
        for item in self.dataset:
            input_text = item['input'].lower().strip()
            output = item['output']
            category = item.get('category', 'unknown')
            
            # 1. Exact match index
            normalized = self._normalize_text(input_text)
            if normalized not in self.exact_index:
                self.exact_index[normalized] = []
            self.exact_index[normalized].append(output)
            
            # 2. Category index
            self.category_index[category].append({
                'input': input_text,
                'output': output
            })
            
            # 3. Keyword index - extract important words
            keywords = self._extract_keywords(input_text)
            for keyword in keywords:
                self.keyword_index[keyword].append({
                    'input': input_text,
                    'output': output,
                    'category': category
                })
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better matching."""
        text = ' '.join(text.split())
        text = text.rstrip('?!.,;:')
        # Remove extra punctuation inside
        text = re.sub(r'[!?]{2,}', '', text)
        return text.lower().strip()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Common words to ignore
        stopwords = {'i', 'you', 'the', 'a', 'an', 'to', 'is', 'are', 'was', 'were', 
                     'what', 'how', 'when', 'where', 'why', 'my', 'your', 'his', 'her',
                     'it', 'this', 'that', 'in', 'on', 'at', 'for', 'with', 'from',
                     'of', 'and', 'or', 'but', 'if', 'so', 'do', 'does', 'did'}
        
        words = re.findall(r'\w+', text.lower())
        keywords = [w for w in words if len(w) > 2 and w not in stopwords]
        return keywords[:5]  # Keep top 5 keywords
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def find_best_response(
        self,
        user_input: str,
        context: List[Dict[str, str]] = None,
        threshold: float = 0.5
    ) -> Optional[str]:
        """Find best response using optimized multi-stage matching with strict filtering."""
        
        user_lower = user_input.lower()
        normalized_input = self._normalize_text(user_input)
        
        # CRITICAL: Physical health keywords - DO NOT match from dataset
        # Let the fallback system in girlfriend_ai.py handle these properly
        physical_health_keywords = [
            'headache', 'stomach', 'fever', 'sick', 'hurt', 'pain', 'ache',
            'bleeding', 'nauseous', 'dizzy', 'injury', 'injured', 'broken',
            'sprain', 'cut', 'wound', 'tooth', 'migraine', 'allerg', 'cold',
            'flu', 'virus', 'infection', 'sore', 'cough', 'sneeze', 'ankle',
            'back pain', 'my back', 'killing me'
        ]
        
        # Check if this is a physical health issue
        if any(keyword in user_lower for keyword in physical_health_keywords):
            # Exception: If it's about emotional hurt, not physical
            emotional_indicators = ['feelings', 'emotionally', 'heart', 'inside']
            is_emotional = any(indicator in user_lower for indicator in emotional_indicators)
            
            if not is_emotional:
                return None  # Let fallback handle physical health
        
        # Stage 1: Exact match (fastest)
        if normalized_input in self.exact_index:
            responses = self.exact_index[normalized_input]
            return random.choice(responses[:10] if len(responses) > 10 else responses)
        
        # Stage 2: Keyword-based matching (fast and contextual)
        user_keywords = self._extract_keywords(user_input)
        if user_keywords:
            keyword_matches = []
            for keyword in user_keywords:
                if keyword in self.keyword_index:
                    keyword_matches.extend(self.keyword_index[keyword])
            
            if keyword_matches:
                # Score matches based on keyword overlap
                scored_matches = []
                for match in keyword_matches:
                    match_keywords = self._extract_keywords(match['input'])
                    overlap = len(set(user_keywords) & set(match_keywords))
                    
                    # Only consider if significant overlap (at least 40% of keywords)
                    if overlap >= max(2, len(user_keywords) * 0.4):
                        scored_matches.append((overlap, match['output']))
                
                if scored_matches:
                    # Sort by score and return best
                    scored_matches.sort(reverse=True, key=lambda x: x[0])
                    
                    # Only return if top score is strong enough
                    if scored_matches[0][0] >= 3 or scored_matches[0][0] >= len(user_keywords) * 0.6:
                        top_matches = [m[1] for m in scored_matches[:20]]
                        return random.choice(top_matches)
        
        # Stage 3: Fuzzy similarity search (slower, broader) - MORE CONSERVATIVE
        best_match = None
        best_score = 0.0
        
        # Only search a sample for speed
        sample_size = min(5000, len(self.exact_index))
        sampled_inputs = list(self.exact_index.keys())[:sample_size]
        
        for stored_input in sampled_inputs:
            similarity = self._calculate_similarity(normalized_input, stored_input)
            
            # Much higher threshold - only match if very similar (80%+)
            if similarity > best_score and similarity >= max(0.8, threshold):
                best_score = similarity
                best_match = self.exact_index[stored_input]
        
        # Only return if confidence is very high
        if best_match and best_score >= 0.8:
            return random.choice(best_match[:10] if len(best_match) > 10 else best_match)
        
        return None
    
    def get_contextual_response(
        self,
        user_input: str,
        conversation_history: List[Dict],
        mood: str = 'playful'
    ) -> Optional[str]:
        """Get response considering full conversation context."""
        
        # Try to find pattern match in dataset
        response = self.find_best_response(user_input, conversation_history)
        
        return response


# Global engine instance
_engine = None

def get_response_engine(dataset_path: str = None) -> SmartResponseEngine:
    """Get or create response engine singleton."""
    global _engine
    if _engine is None:
        if dataset_path is None:
            # Use the new 297K dataset
            dataset_path = str(Path(__file__).parent.parent / "data" / "final_training_dataset_100k.json")
        _engine = SmartResponseEngine(dataset_path)
    return _engine
