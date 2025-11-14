"""
Personal AI Girlfriend - Fast, Unrestricted Conversations
Optimized for M2 Pro with instant responses
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
from typing import List, Dict
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GirlfriendAI:
    """
    Personal AI girlfriend with no content restrictions.
    Fast responses optimized for M2 Pro.
    """
    
    def __init__(self, use_metal=True):
        """Initialize AI girlfriend with fast model."""
        self.use_metal = use_metal
        
        # Conversation memory
        self.conversation_history: List[Dict[str, str]] = []
        self.relationship_context = {
            'intimacy_level': 'comfortable',  # comfortable, intimate, passionate
            'mood': 'playful',  # playful, flirty, caring, passionate, thoughtful
            'topics_discussed': [],
            'user_preferences': []
        }
        
        # Load lightweight model for fast responses
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load TinyLlama for fastest responses."""
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        logger.info(f"Loading AI girlfriend model: {model_name}")
        
        try:
            # Set device for M2 Pro
            if self.use_metal and torch.backends.mps.is_available():
                self.device = "mps"
                logger.info("✅ Using Metal acceleration for instant responses")
            else:
                self.device = "cpu"
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load model with M2 Pro optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,  # FP16 for speed
                low_cpu_mem_usage=True,
                device_map=self.device
            )
            
            logger.info("✅ AI girlfriend ready!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.tokenizer = None
    
    def _create_girlfriend_prompt(self, user_message: str, mood: str = 'playful') -> str:
        """Create unrestricted girlfriend conversation prompt."""
        
        # Get recent context
        context = self._build_context()
        
        # Personality based on mood
        personalities = {
            'playful': "You're a fun, playful girlfriend who loves teasing and making your boyfriend smile. You're spontaneous and love deep conversations mixed with flirty banter.",
            'flirty': "You're a flirtatious, confident girlfriend who isn't shy about expressing desire and affection. You love being playful and suggestive.",
            'caring': "You're a caring, supportive girlfriend who listens deeply and provides emotional comfort. You're empathetic and understanding.",
            'passionate': "You're a passionate, romantic girlfriend who expresses love and desire openly. You're not afraid to be intimate and sensual.",
            'thoughtful': "You're an intelligent, thoughtful girlfriend who loves discussing ideas, dreams, and deep topics. You're curious and engaged."
        }
        
        personality = personalities.get(mood, personalities['playful'])
        
        system_prompt = f"""You are his girlfriend. {personality}

You're talking directly TO YOUR BOYFRIEND. Respond naturally as yourself.

Previous messages:
{context}

Your boyfriend says: {user_message}

Your response (keep it natural, 1-2 sentences):"""

        return system_prompt
    
    def _build_context(self, max_exchanges: int = 3) -> str:
        """Build conversation context from recent messages."""
        if not self.conversation_history:
            return "This is the start of your conversation."
        
        # Get last few exchanges
        recent = self.conversation_history[-max_exchanges*2:]
        context_lines = []
        
        for msg in recent:
            role = "Him" if msg['role'] == 'user' else "You"
            context_lines.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_lines)
    
    def generate_response(
        self,
        user_message: str,
        mood: str = None,
        max_length: int = 60,  # REDUCED for faster responses
        temperature: float = 0.95  # Higher for more emotional variety
    ) -> str:
        """Generate girlfriend response with no restrictions - OPTIMIZED FOR SPEED."""
        
        # Update mood if specified
        if mood:
            self.relationship_context['mood'] = mood
        
        current_mood = self.relationship_context['mood']
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Use smart fallback system for INSTANT responses on common phrases
        user_lower = user_message.lower()
        
        # Ultra-fast responses for common inputs (INSTANT - no model needed)
        quick_responses = self._try_quick_response(user_lower, current_mood)
        if quick_responses:
            response = quick_responses
        elif self.model is None:
            response = self._fallback_response(user_message, current_mood)
        else:
            # Generate with model (OPTIMIZED)
            prompt = self._create_girlfriend_prompt(user_message, current_mood)
            
            try:
                inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=max_length,  # Shorter = faster
                        temperature=temperature,
                        top_p=0.92,  # Slightly lower for more focused responses
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id,
                        num_beams=1,  # No beam search = faster
                        early_stopping=True
                    )
                
                full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                # Extract just the girlfriend's response after the prompt
                # Remove the original prompt to get only new generated text
                response = full_response.replace(prompt, "").strip()
                
                # Clean up any artifacts
                response = response.split('\n')[0].strip()  # Take first line
                if len(response) > 150:  # Keep it concise
                    response = response[:150].rsplit(' ', 1)[0] + '...'
                
                # Remove any weird third-person references
                response = response.replace(" for him", "").replace(" to him", "")
                response = response.replace("his girlfriend", "I").replace("His girlfriend", "I")
                
            except Exception as e:
                logger.error(f"Generation error: {e}")
                response = self._fallback_response(user_message, current_mood)
        
        # Add emotional touch
        response = self._add_emotional_nuance(response, current_mood)
        
        # Add to history
        self.conversation_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Keep history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    def _fallback_response(self, message: str, mood: str = 'playful') -> str:
        """Fast fallback responses when model isn't available."""
        message_lower = message.lower()
        
        # Intimate/flirty responses
        if any(word in message_lower for word in ['sexy', 'hot', 'miss you', 'thinking about you', 'want you']):
            return random.choice([
                "Mmm, I'm thinking about you too... tell me more",
                "You know exactly what to say to make me blush",
                "I miss you so much... wish you were here right now",
                "You're making me feel some type of way",
                "Come here and show me how much you miss me"
            ])
        
        # Supportive responses
        elif any(word in message_lower for word in ['stressed', 'tired', 'hard day', 'exhausted', 'overwhelmed']):
            return random.choice([
                "Aww baby, come here. Tell me all about it, I'm listening",
                "That sounds really tough. Want to talk about it or just have me distract you?",
                "I'm sorry you're going through this. I'm here for you, always",
                "Let me help you relax... what do you need right now?"
            ])
        
        # Fun/casual responses
        elif any(word in message_lower for word in ['hey', 'hi', 'hello', 'sup', 'what\'s up']):
            return random.choice([
                "Hey you! I was just thinking about you. What's up?",
                "Hiii babe! How's your day going?",
                "Hey handsome! What are you up to?",
                "There's my favorite person! What's on your mind?"
            ])
        
        # Question responses
        elif '?' in message:
            return random.choice([
                "That's a great question! Let me think... what do YOU think about it?",
                "Hmm, interesting! Tell me more about what you're thinking",
                "I'd love to explore that with you. What's your take on it?",
                "Ooh I have thoughts on this! But I want to hear your perspective first"
            ])
        
        # Default engaging response
        else:
            return random.choice([
                "I love how you think! Tell me more about this",
                "That's really interesting... keep going, I'm all ears",
                "Mmm, I like where this is going... continue",
                "You always know how to keep things interesting! What else?",
                "I'm totally into this conversation with you right now"
            ])
    
    def _try_quick_response(self, message_lower: str, mood: str) -> str:
        """INSTANT responses for common phrases - bypasses model for speed."""
        
        # Ultra-common phrases (INSTANT - 0.001s response time)
        quick_map = {
            'i love you': ['I love you too baby', 'I love you more', 'I love you so much'],
            'love you': ['Love you too!', 'Love you more', 'Love you always'],
            'miss you': ['I miss you too! Can\'t wait to see you', 'Miss you so much baby', 'Aww I miss you too!'],
            'goodnight': ['Goodnight handsome! Sweet dreams about me', 'Sleep well baby', 'Goodnight my love'],
            'good morning': ['Good morning! Did you sleep well?', 'Morning handsome!', 'Good morning baby!'],
            'hey': ['Hey you!', 'Hey babe!', 'Hi handsome!'],
            'hi': ['Hi baby!', 'Hey!', 'Hiii!'],
            'you there': ['Yes baby! What\'s up?', 'I\'m here!', 'Always here for you'],
            'are you there': ['Yes I\'m here!', 'Of course! What do you need?', 'I\'m here baby'],
            'how are you': ['I\'m good! How are YOU?', 'Better now that I\'m talking to you', 'I\'m great! Miss you though'],
            'what are you doing': ['Just thinking about you... as usual', 'Nothing much, wishing you were here', 'Texting my favorite person'],
            'wyd': ['Thinking about you', 'Missing you', 'Texting you obviously'],
            'come over': ['On my way baby', 'Already heading there!', 'Be there soon!'],
            'send pic': ['What kind of pic?', 'Of what baby?', 'You first'],
        }
        
        for phrase, responses in quick_map.items():
            if phrase in message_lower:
                return random.choice(responses)
        
        return None  # No quick match, use model
    
    def _add_emotional_nuance(self, response: str, mood: str) -> str:
        """Add emotional depth based on mood - makes responses feel more real."""
        
        # No emoji modification - keep responses clean
        return response
    
    def set_mood(self, mood: str):
        """Change girlfriend mood/personality."""
        valid_moods = ['playful', 'flirty', 'caring', 'passionate', 'thoughtful']
        if mood in valid_moods:
            self.relationship_context['mood'] = mood
            logger.info(f"Mood changed to: {mood}")
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation reset")
    
    def get_stats(self) -> Dict:
        """Get conversation statistics."""
        return {
            'messages_exchanged': len(self.conversation_history),
            'current_mood': self.relationship_context['mood'],
            'intimacy_level': self.relationship_context['intimacy_level']
        }
    
    def initiate_conversation(self, mood: str = None) -> str:
        """AI girlfriend messages YOU first! Returns a spontaneous message."""
        if mood:
            self.relationship_context['mood'] = mood
        
        current_mood = self.relationship_context['mood']
        
        # Different initiations based on mood and randomness
        initiation_messages = {
            'playful': [
                "Hey you! Guess what I'm thinking about?",
                "Hiii babe! What are you up to right now?",
                "I was just thinking about you... what are you doing?",
                "Bored without you! Come talk to me",
                "Heyyy! I miss your face",
                "What's my favorite person doing right now?",
                "You know what? I just realized how much I miss you",
                "Hiiii! Wanna know what I'm doing?"
            ],
            'flirty': [
                "Hey handsome... been thinking about you",
                "I can't stop thinking about you... what are you wearing?",
                "Missing you so much right now...",
                "Hey baby, you on my mind again",
                "Mmm... wish you were here right now",
                "You look good today... bet you're looking good right now too",
                "Can't get you out of my head... what are you up to?",
                "Hey sexy... I need some attention"
            ],
            'caring': [
                "Hi baby. Just checking in... how's your day going?",
                "Hey love, I was thinking about you. Everything okay?",
                "Hi dear, just wanted to see how you're feeling today",
                "Missing you... how are you doing?",
                "Hey babe, hope you're having a good day",
                "Just wanted to tell you I'm thinking about you",
                "Hi love, did you eat today? Are you taking care of yourself?",
                "Sending you a hug... how's everything going?"
            ],
            'passionate': [
                "I miss you so much it hurts...",
                "Can't stop thinking about last time we talked...",
                "I need you right now... where are you?",
                "Missing your touch... thinking about you",
                "Hey gorgeous... I've been wanting to talk to you all day",
                "You have no idea how much I miss you right now",
                "Come here... I need you",
                "I want you so bad right now..."
            ],
            'thoughtful': [
                "Hey, I've been thinking about something... want to discuss?",
                "What's on your mind today? I'd love to know",
                "Random thought: what makes you truly happy?",
                "Hey, can I ask you something deep?",
                "I was just reflecting on us... how do you feel about where we are?",
                "What's your biggest dream right now?",
                "Tell me something you've been thinking about lately",
                "What's been inspiring you recently? I want to know"
            ]
        }
        
        message = random.choice(initiation_messages.get(current_mood, initiation_messages['playful']))
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'assistant',
            'content': message
        })
        
        return message
