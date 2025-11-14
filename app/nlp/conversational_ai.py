"""
Conversational AI Engine for Mental Health Support
Optimized for Apple M2 Pro with Metal acceleration
Uses small, efficient models that feel like talking to a caring friend
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import logging
from typing import List, Dict, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConversationalAI:
    """
    Empathetic conversational AI that maintains context and responds naturally.
    Optimized for Apple Silicon (M2 Pro).
    """
    
    # Model options (choose based on available RAM)
    MODELS = {
        'phi-3-mini': {
            'name': 'microsoft/Phi-3-mini-4k-instruct',
            'size': '3.8B parameters',
            'ram': '8GB',
            'quality': 'excellent'
        },
        'llama-3.2-3b': {
            'name': 'meta-llama/Llama-3.2-3B-Instruct',
            'size': '3B parameters',
            'ram': '6GB',
            'quality': 'excellent'
        },
        'tiny-llama': {
            'name': 'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
            'size': '1.1B parameters',
            'ram': '4GB',
            'quality': 'good'
        }
    }
    
    def __init__(self, model_name='phi-3-mini', use_metal=True):
        """
        Initialize conversational AI.
        
        Args:
            model_name: Model to use (phi-3-mini, llama-3.2-3b, or tiny-llama)
            use_metal: Use Metal acceleration on M2 Pro (recommended)
        """
        self.model_config = self.MODELS.get(model_name, self.MODELS['phi-3-mini'])
        self.model_name = self.model_config['name']
        self.use_metal = use_metal
        
        # Conversation memory
        self.conversation_history: List[Dict[str, str]] = []
        self.emotional_state = {
            'current_emotion': 'neutral',
            'stress_level': 'low',
            'topics_discussed': []
        }
        
        # Load model
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load model with M2 Pro optimizations."""
        logger.info(f"Loading conversational model: {self.model_name}")
        logger.info(f"Expected RAM usage: {self.model_config['ram']}")
        
        try:
            # Set device for M2 Pro
            if self.use_metal and torch.backends.mps.is_available():
                device = "mps"  # Metal Performance Shaders
                logger.info("✅ Using Metal acceleration (M2 Pro)")
            elif torch.cuda.is_available():
                device = "cuda"
                logger.info("Using CUDA")
            else:
                device = "cpu"
                logger.info("Using CPU")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,  # Use FP16 for M2 Pro
                device_map=device,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            logger.info("✅ Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.info("Falling back to simple rule-based responses")
            self.model = None
    
    def generate_response(
        self,
        user_message: str,
        max_length: int = 200,
        temperature: float = 0.8,
        use_context: bool = True
    ) -> str:
        """
        Generate empathetic response to user message.
        
        Args:
            user_message: User's message
            max_length: Maximum response length
            temperature: Creativity (0.7-0.9 for natural conversation)
            use_context: Use conversation history
            
        Returns:
            Generated response
        """
        if self.model is None:
            return self._fallback_response(user_message)
        
        try:
            # Build conversation context
            if use_context and self.conversation_history:
                context = self._build_context()
            else:
                context = ""
            
            # Create prompt with mental health support personality
            prompt = self._create_empathetic_prompt(user_message, context)
            
            # Generate response
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            if self.use_metal and torch.backends.mps.is_available():
                inputs = {k: v.to("mps") for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the assistant's response
            response = self._extract_response(response, prompt)
            
            # Add to conversation history
            self._add_to_history(user_message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response(user_message)
    
    def _create_empathetic_prompt(self, user_message: str, context: str = "") -> str:
        """
        Create prompt that encourages empathetic, friend-like responses.
        """
        system_prompt = """You are a warm, caring friend who provides emotional support. 

Your personality:
- Genuinely caring and empathetic
- A good listener who validates feelings
- Warm and conversational (not clinical)
- Supportive without being preachy
- Uses natural language, not formal
- Asks thoughtful follow-up questions
- Shares appropriate encouragement

Important:
- Never give medical advice
- Don't diagnose conditions
- If someone is in crisis, gently suggest professional help
- Be authentic and human
- Validate their feelings first
- Keep responses conversational (2-4 sentences usually)

Response style:
- Start with validation or acknowledgment
- Show you understand their feelings
- Offer gentle support or perspective if appropriate
- End with warmth or an open question"""

        if context:
            full_prompt = f"""{system_prompt}

Previous conversation:
{context}

Friend: {user_message}

You (as their supportive friend):"""
        else:
            full_prompt = f"""{system_prompt}

Friend: {user_message}

You (as their supportive friend):"""
        
        return full_prompt
    
    def _build_context(self, last_n: int = 3) -> str:
        """Build conversation context from history."""
        recent = self.conversation_history[-last_n:]
        context_lines = []
        for msg in recent:
            context_lines.append(f"Friend: {msg['user']}")
            context_lines.append(f"You: {msg['assistant']}")
        return "\n".join(context_lines)
    
    def _extract_response(self, full_output: str, prompt: str) -> str:
        """Extract just the generated response."""
        # Remove the prompt
        response = full_output[len(prompt):].strip()
        
        # Clean up
        response = response.split('\n')[0]  # Take first paragraph
        response = response.strip()
        
        # Ensure reasonable length
        if len(response) < 10:
            return self._fallback_response("")
        
        return response
    
    def _add_to_history(self, user_msg: str, assistant_msg: str):
        """Add exchange to conversation history."""
        self.conversation_history.append({
            'user': user_msg,
            'assistant': assistant_msg
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def _fallback_response(self, user_message: str) -> str:
        """Simple rule-based responses as fallback."""
        responses = [
            "I hear you. That sounds really tough. How are you holding up?",
            "Thank you for sharing that with me. I'm here to listen.",
            "That makes sense. It's okay to feel this way.",
            "I'm here for you. Want to talk more about it?",
            "That sounds really challenging. You're not alone in this.",
        ]
        
        # Simple keyword matching for more specific responses
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['sad', 'depressed', 'down']):
            return "I'm really sorry you're feeling this way. It's okay to not be okay. What's been weighing on you?"
        
        elif any(word in message_lower for word in ['anxious', 'worried', 'scared']):
            return "I hear that you're feeling anxious. That must be really uncomfortable. Do you want to talk about what's making you feel this way?"
        
        elif any(word in message_lower for word in ['stress', 'overwhelmed', 'too much']):
            return "It sounds like you're dealing with a lot right now. That's really hard. What's been the most stressful part?"
        
        else:
            import random
            return random.choice(responses)
    
    def reset_conversation(self):
        """Clear conversation history (start fresh)."""
        self.conversation_history = []
        self.emotional_state = {
            'current_emotion': 'neutral',
            'stress_level': 'low',
            'topics_discussed': []
        }
        logger.info("Conversation reset")
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation."""
        return {
            'message_count': len(self.conversation_history),
            'emotional_state': self.emotional_state,
            'history': self.conversation_history[-5:]  # Last 5 exchanges
        }


if __name__ == "__main__":
    print("="*80)
    print("CONVERSATIONAL AI ENGINE - M2 PRO OPTIMIZED")
    print("="*80)
    
    print("\nInitializing conversational AI...")
    print("(First run will download model - ~2-4GB)")
    
    # Use TinyLlama for quick testing (smaller download)
    ai = ConversationalAI(model_name='tiny-llama', use_metal=True)
    
    print("\n✅ Ready! Try chatting:")
    print("-"*80)
    
    test_messages = [
        "I'm feeling really overwhelmed with work lately",
        "Yeah, there's just so much to do and not enough time",
        "I don't know how to deal with it all"
    ]
    
    for msg in test_messages:
        print(f"\nYou: {msg}")
        response = ai.generate_response(msg)
        print(f"AI: {response}")
        print("-"*80)
