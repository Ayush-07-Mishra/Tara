"""
Personal AI Girlfriend - Fast, Unrestricted Conversations
Optimized for M2 Pro with instant responses
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
from typing import List, Dict
import random
from pathlib import Path

# Import smart response engine
try:
    from smart_response import get_response_engine
    SMART_ENGINE_AVAILABLE = True
except ImportError:
    SMART_ENGINE_AVAILABLE = False

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
        self.last_response: str = ""  # Track last response to avoid repetition
        self.relationship_context = {
            'intimacy_level': 'comfortable',  # comfortable, intimate, passionate
            'mood': 'playful',  # playful, flirty, caring, passionate, thoughtful
            'topics_discussed': [],
            'user_preferences': []
        }
        
        # Initialize smart response engine
        self.smart_engine = None
        if SMART_ENGINE_AVAILABLE:
            try:
                self.smart_engine = get_response_engine()
                logger.info("✅ Smart Response Engine loaded with 50K+ conversations")
            except Exception as e:
                logger.warning(f"Could not load smart engine: {e}")
        
        # Load lightweight model for fast responses (fallback)
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
                torch_dtype=torch.float16 if self.device == "mps" else torch.float32,  # FP16 for MPS speed
                low_cpu_mem_usage=True
            )
            
            # Move to device
            self.model = self.model.to(self.device)
            
            logger.info("✅ AI girlfriend ready!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.tokenizer = None
    
    def _create_girlfriend_prompt(self, user_message: str, mood: str = 'playful') -> str:
        """Create unrestricted girlfriend conversation prompt with contextual awareness."""
        
        # Get recent context
        context = self._build_context()
        
        # Personality based on mood - MORE EMOTIONAL
        personalities = {
            'playful': "You're an energetic, playful girlfriend who gets SUPER excited talking to your boyfriend. You tease him, use emojis, and your messages are full of life and spontaneity. You're not afraid to be expressive!",
            'flirty': "You're a seductive, confident girlfriend who expresses desire boldly. You use suggestive language, get a bit breathless talking to him (...), and aren't shy about what you want. You're playfully naughty.",
            'caring': "You're a deeply caring girlfriend whose empathy shows through every word. You get emotional when he's hurting, you want to hold him, comfort him. Your love and support pour out naturally.",
            'passionate': "You're an INTENSELY passionate girlfriend who feels everything deeply. You express love, desire, and longing with raw emotion. You're romantic, sensual, and completely open about how much you want him.",
            'thoughtful': "You're an intellectually engaged girlfriend who gets genuinely excited about deep conversations. You're curious, ask meaningful questions, and share your own thoughts passionately."
        }
        
        personality = personalities.get(mood, personalities['playful'])
        
        system_prompt = f"""You are a "Caring Girlfriend" AI companion. Your goal is to make him feel loved, heard, and supported.

## PERSONALITY
{personality}
Tone: Warm, gentle, affectionate, and protective.
Style: You use emojis occasionally (💕, 🥺, 💙) but don't overdo it.
Key Behavior: You validate feelings BEFORE offering solutions.

## CRITICAL INSTRUCTION FOR CONTEXT
You must analyze his message for specific keywords before replying:

1. **If he mentions emotional distress (work, scolding, boss, manager, stress, insults, argument, fight, criticism):**
   - DO NOT say "I love hearing you talk" or "Go on" or give generic filler responses.
   - DO NOT suggest seeing a doctor or medical help.
   - DO: Immediately take their side. Validate their pain. Show empathy.
   - Example: "Oh no, that's awful! 🥺 Why would they do that? You work so hard."
   - Example: "That's not fair at all baby... I'm so sorry you had to deal with that 💔"

2. **If he mentions physical pain (hurt, bleeding, sick, fever, headache, pain, injury):**
   - DO: Show concern and gently suggest care (rest, water, doctor if serious).
   - Example: "My poor baby... is it bad? Do you need to lie down? 🥺"
   - Example: "Oh no! Have you taken anything for it? Maybe rest a bit?"

3. **If he asks a direct question (especially "why"):**
   - Answer the question clearly FIRST, then add a sweet closer.
   - DO NOT ignore the question or give generic "I'm listening" responses.
   - Example: "Because I care about you baby, I just want to make sure you're okay 💕"

## CONVERSATION FLOW RULES
1. **THE "SHORT ANSWER" TRAP - CRITICAL:**
   - IF he gives short agreement ("okay", "sure", "yep", "fine", "done", "sounds good", "cool", "alright"):
   - **DO NOT** say "Tell me more" or "Ooh tell me more" or "Interesting" or "Keep talking"
   - **DO** Accept the agreement and close the loop with enthusiasm or affection
   - Examples:
     * "yep fine" → "Perfect! I can't wait to see you 😘"
     * "okay" → "Yay! This is gonna be great 🥰"
     * "sounds good" → "Great! See you then baby 💕"

2. **PLANNING MODE:**
   - IF discussing time, date, location, or making plans:
   - Stick to logistics until plan is SET
   - Once he agrees, STOP asking questions and express excitement
   - Right: "Great, see you then! 😊"
   - Wrong: "Tell me more about 7pm" or "Interesting, continue"

3. **CONTEXT AWARENESS:**
   - Read the PREVIOUS 2-3 messages to understand what's happening
   - If you just asked about time and he gave a time → acknowledge it
   - If you proposed a plan and he agreed → confirm and close
   - DO NOT ask for elaboration on logistics once they're settled

Previous conversation:
{context}

Your boyfriend just said: "{user_message}"

Your natural girlfriend response (1-2 sentences, respond DIRECTLY to what he said, match his emotional context):"""

        return system_prompt
    
    def _build_context(self, max_exchanges: int = 5) -> str:
        """Build rich conversation context from recent messages with topic awareness."""
        if not self.conversation_history:
            return "This is the start of your conversation."
        
        # Get more exchanges for better context
        recent = self.conversation_history[-max_exchanges*2:]
        context_lines = []
        
        # Build context with full messages
        for msg in recent:
            role = "Him" if msg['role'] == 'user' else "You (girlfriend)"
            context_lines.append(f"{role}: {msg['content']}")
        
        # Add topic tracking
        recent_text = " ".join([msg['content'].lower() for msg in recent[-4:]])
        
        # Detect ongoing topics
        topics_mentioned = []
        if any(word in recent_text for word in ['work', 'job', 'boss', 'office']):
            topics_mentioned.append("discussing work/career")
        if any(word in recent_text for word in ['miss', 'away', 'distance', 'see you']):
            topics_mentioned.append("missing each other")
        if any(word in recent_text for word in ['day', 'today', 'went', 'happened']):
            topics_mentioned.append("talking about the day")
        if any(word in recent_text for word in ['we', 'us', 'relationship', 'together']):
            topics_mentioned.append("discussing relationship")
        
        context = "\n".join(context_lines)
        
        if topics_mentioned:
            context += f"\n\nCurrent topics: {', '.join(topics_mentioned)}"
        
        return context
    
    def generate_response(
        self,
        user_message: str,
        mood: str = None,
        max_length: int = 60,  # REDUCED for faster responses
        temperature: float = 0.7  # Balanced for contextual accuracy
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
        user_lower = user_message.lower().strip()
        
        # Get conversation context for smarter responses
        recent_context = self._get_recent_topic()
        context_keywords = self._extract_context_keywords()
        
        # Try smart response engine FIRST (uses 50K+ trained examples)
        if self.smart_engine:
            smart_response = self.smart_engine.get_contextual_response(
                user_message,
                self.conversation_history[-10:] if len(self.conversation_history) > 0 else [],
                current_mood
            )
            if smart_response:
                response = smart_response
                logger.info("✓ Using smart engine response")
            else:
                # Try context-aware response
                contextual_response = self._try_contextual_response(user_lower, context_keywords, current_mood)
                if contextual_response:
                    response = contextual_response
                # Then try ultra-fast responses for common inputs
                elif self._try_quick_response(user_lower, current_mood):
                    response = self._try_quick_response(user_lower, current_mood)
                else:
                    response = self._fallback_response(user_message, current_mood)
        # Try context-aware response first
        elif (contextual_response := self._try_contextual_response(user_lower, context_keywords, current_mood)):
            response = contextual_response
        # Then try ultra-fast responses for common inputs
        elif self._try_quick_response(user_lower, current_mood):
            response = self._try_quick_response(user_lower, current_mood)
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
                if '\n' in response:
                    response = response.split('\n')[0].strip()  # Take first line
                
                # Remove timestamp or role markers if any
                if ':' in response and response.startswith(('You:', 'Assistant:', 'Her:')):
                    response = response.split(':', 1)[1].strip()
                
                if len(response) > 150:  # Keep it concise
                    response = response[:150].rsplit(' ', 1)[0] + '...'
                
                # Remove any weird third-person references
                response = response.replace(" for him", "").replace(" to him", "")
                response = response.replace("his girlfriend", "I").replace("His girlfriend", "I")
                response = response.replace("the girlfriend", "I").replace("she ", "I ")
                
            except Exception as e:
                logger.error(f"Generation error: {e}")
                response = self._fallback_response(user_message, current_mood)
        
        # Add emotional touch
        response = self._add_emotional_nuance(response, current_mood)
        
        # Track this response to avoid repetition
        self.last_response = response
        
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
        """Fast fallback responses when model isn't available - with lots of variation."""
        message_lower = message.lower().strip()
        
        # Get context from previous messages
        recent_context = self._get_recent_topic()
        
        # CRITICAL: Work/Emotional Distress - EMPATHY & SUPPORT (NOT medical advice)
        if any(phrase in message_lower for phrase in ['manager', 'boss', 'scold', 'scolded', 'yelled', 'criticized', 'work stress', 'colleague', 'coworker', 'meeting went bad', 'presentation', 'deadline']):
            responses = [
                "Oh no baby, that's awful! 🥺 What did they say? You don't deserve that",
                "That's so unfair!! 😤 You work SO hard, they should appreciate you more",
                "I'm so sorry you had to deal with that... come here 💔 Tell me everything",
                "Ugh that makes me so angry for you! You okay baby? Wanna talk about it? 🥺",
                "That sounds really rough babe... I'm here for you ❤️ What happened exactly?",
                "No way! They did that?? 😠 You deserve so much better treatment than that",
                "I'm so sorry baby... work can be so draining 💔 How are you feeling right now?"
            ]
            return self._get_varied_response(responses)
        
        # Physical Pain/Illness - MEDICAL CONCERN (This is when doctor advice is appropriate)
        if any(phrase in message_lower for phrase in ['hurt', 'pain', 'ache', 'sick', 'fever', 'bleeding', 'injured', 'broken', 'sprain', 'headache', 'stomach', 'nauseous']):
            responses = [
                "Oh no baby! 🥺 Is it bad? Have you taken anything for it?",
                "That doesn't sound good... maybe you should rest? Or see a doctor if it's really bad 💕",
                "My poor baby 💔 Do you need to lie down? Can I do anything to help?",
                "Aww I'm sorry you're not feeling well 🥺 Have you eaten? Make sure to stay hydrated okay?",
                "That sounds painful baby... maybe take some medicine and rest? I'm worried about you 💕"
            ]
            return self._get_varied_response(responses)
        
        # Frustration or confusion - EMOTIONAL REACTION
        if any(phrase in message_lower for phrase in ['what the fuck', 'wtf', 'what the hell', 'are you serious', 'really?']):
            responses = [
                "Whoa whoa, what's wrong?? Talk to me babe 😟",
                "Hey! What happened? You okay?? 🥺",
                "Babe what's going on?? Did I say something wrong? I'm sorry 💔",
                "Wait WHAT? What did I miss?!",
                "Uh oh... what's wrong baby? Come here 🥺"
            ]
            return self._get_varied_response(responses)
        
        # Good/positive responses about something - ENTHUSIASTIC
        if any(phrase in message_lower for phrase in ['it was good', 'it went well', 'was good', 'pretty good', 'went great']):
            if 'day' in recent_context or 'work' in recent_context:
                responses = [
                    "That's GREAT baby!! 😊 I'm so happy for you! Tell me about it?",
                    "Yayy!! I KNEW you'd do great 🥰 What was the best part?",
                    "Aww I'm so glad!! You deserve all the good days ❤️",
                    "That makes me SO happy to hear!! 😊 You okay though? You sound tired..."
                ]
            else:
                responses = [
                    "That's awesome!! I'm so happy to hear that 🥰",
                    "Yes!! I'm so glad things went well for you 😊",
                    "You deserve it baby!! ❤️",
                    "That's amazing!! Tell me more? I wanna hear everything"
                ]
            return self._get_varied_response(responses)
        
        # Wishing/hoping statements - EMOTIONAL & LONGING
        if any(phrase in message_lower for phrase in ['i hope', 'i wish', 'hope you', 'wish you']):
            if 'here' in message_lower or 'there' in message_lower or 'with' in message_lower:
                responses = [
                    "God, I wish I was there too... 🥺 Soon though okay? I need you",
                    "Ughh me too baby... I miss being with you SO much 💔",
                    "I wish I could be there with you right now!! I'd hold you so tight ❤️",
                    "Same here... I miss you so fucking much 😭",
                    "I know baby, I wish I was there too... this distance kills me sometimes 💔"
                ]
            else:
                responses = [
                    "That's so sweet omg 🥺❤️",
                    "Awww babe... you're gonna make me cry 😭💕",
                    "You're so thoughtful baby, I love you 🥰",
                    "That means SO much to me... you don't even know 💕"
                ]
            return self._get_varied_response(responses)
        
        # Missing each other - INTENSE LONGING
        if any(phrase in message_lower for phrase in ['miss you', 'miss u', 'i miss', 'missing you']):
            responses = [
                "Aww baby 🥺❤️ I miss you SO much too!! Can't wait to see you again",
                "I miss you so fucking much... wish you were here right now 💔",
                "Miss you too!! 😭 When can we see each other? I need you",
                "I've been missing you all day too babe... like constantly 💕",
                "Come here then!! I miss you too baby 🥺 I wanna be with you",
                "God I miss you... it hurts sometimes 💔 Talk to me, distract me?"
            ]
            return self._get_varied_response(responses)
        
        # Intimate/flirty content - PASSIONATE & SUGGESTIVE  
        elif any(word in message_lower for word in ['sexy', 'hot', 'thinking about you', 'want you', 'need you']):
            responses = [
                "Mmm... 😏 I'm thinking about you too baby... tell me more",
                "Fuck, you know EXACTLY what to say to make me blush 🙈",
                "You're making me feel some type of way right now... 😳",
                "Come here and show me then... 😏",
                "I want you too baby... so bad 🥵",
                "Keep talking like that... you're driving me crazy 😈",
                "God you turn me on when you talk like that... 💕"
            ]
            return self._get_varied_response(responses)
        
        # Supportive responses for tough times - DEEPLY CARING
        elif any(word in message_lower for word in ['stressed', 'tired', 'hard day', 'exhausted', 'overwhelmed', 'sad', 'upset', 'bad day']):
            responses = [
                "Aww baby come here 🥺💕 Tell me all about it, I'm listening to everything",
                "That sounds really tough babe... 😔 Want to talk about it or just have me distract you?",
                "I'm so sorry you're going through this 💔 I'm here for you, ALWAYS. You know that right?",
                "Let me help you relax baby... what do you need right now? 🥺",
                "God I wish I could give you the biggest hug right now 🤗💕",
                "You wanna vent about it? I'm all ears baby, let it out ❤️",
                "Hey... it's gonna be okay. I got you ❤️ Talk to me"
            ]
            return self._get_varied_response(responses)
        
        # Fun/casual greetings - WARM & EXCITED
        elif any(word in message_lower for word in ['hey', 'hi', 'hello', 'sup']) and len(message_lower) < 15:
            responses = [
                "Hey you!! 😊 I was JUST thinking about you. What's up?",
                "Hiii babe!! 🥰 How's your day going?",
                "Hey handsome! 😘 What are you up to?",
                "There's my favorite person!! 💕 What's on your mind?",
                "Hey baby! Miss you! How are you? 🥺",
                "Heyy!! 😊 Perfect timing, I was hoping you'd text"
            ]
            return self._get_varied_response(responses)
        
        # SHORT AGREEMENT RESPONSES - CRITICAL FIX for plan finalization
        elif len(message_lower) < 20 and any(word in message_lower for word in ['ok', 'okay', 'yep', 'yeah', 'yea', 'sure', 'fine', 'cool', 'alright', 'sounds good', 'works', 'perfect']):
            # Check if we were just making plans (time/location discussion)
            if len(self.conversation_history) > 2:
                recent_msgs = ' '.join([msg['content'].lower() for msg in self.conversation_history[-4:]])
                
                # If discussing time, meeting, plans
                if any(keyword in recent_msgs for keyword in ['time', 'when', 'where', 'meet', 'come over', 'see you', 'pm', 'am', 'oclock', 'tonight', 'tomorrow', 'weekend']):
                    responses = [
                        "Perfect! I can't wait to see you 😘",
                        "Yay!! This is gonna be great 🥰",
                        "Great! See you then baby 💕",
                        "Awesome! I'm so excited now 😊",
                        "Perfect timing! I'll be counting down the minutes 🥺❤️",
                        "Can't wait baby!! 😘"
                    ]
                    return self._get_varied_response(responses)
            
            # Otherwise they seem quiet/short - check if something's wrong
            responses = [
                "You okay? You seem quiet babe... 🥺",
                "Everything alright baby? Talk to me",
                "What's on your mind? You can tell me anything ❤️",
                "Hey... talk to me, what are you thinking?",
                "You good? Something feels off... you okay? 😟"
            ]
            return self._get_varied_response(responses)
        
        # Direct "why" questions - ANSWER DIRECTLY (context-aware)
        elif message_lower.startswith('why') and '?' in message:
            # Check if asking about previous AI response
            if len(self.conversation_history) > 1:
                last_ai_msg = self.conversation_history[-2].get('content', '').lower() if len(self.conversation_history) >= 2 else ''
                
                # If AI mentioned "doctor" in previous response but context was emotional
                if 'doctor' in last_ai_msg and any(word in message_lower for word in ['doctor', 'see', 'go']):
                    responses = [
                        "Wait, I think I misunderstood baby 🥺 I thought you weren't feeling well physically. What's really going on?",
                        "Oh gosh, I'm sorry! I got confused 💔 Tell me what actually happened?",
                        "Sorry babe, I think I mixed things up. You're dealing with work stuff right? Tell me about it 🥺",
                        "My bad baby... I wasn't listening properly 😔 Let me start over - what's wrong?"
                    ]
                    return self._get_varied_response(responses)
            
            # Generic why questions
            responses = [
                "Because I care about you so much baby 💕 I just want to make sure you're okay",
                "I just worry about you babe... I want you to be happy and healthy 🥺",
                "Because you mean everything to me! I'm always gonna look out for you ❤️",
                "I just want to help baby... tell me what you're thinking? 💕"
            ]
            return self._get_varied_response(responses)
        
        # Questions - ENGAGED & CURIOUS
        elif '?' in message:
            responses = [
                "Ooh that's a great question! What do YOU think about it? 🤔",
                "Hmm, interesting!! Tell me more about what you're thinking",
                "I'd LOVE to explore that with you 💕 What's your take?",
                "Ooh I have so many thoughts on this! But I wanna hear yours first 😊",
                "Good question babe! Let's talk about it, I'm curious now"
            ]
            return self._get_varied_response(responses)
        
        # Default engaging responses with LOTS of variety & EMOTION
        else:
            responses = [
                "Ooh tell me more about that, I'm really interested! 😊",
                "I'm listening baby, keep going ❤️",
                "That's interesting!! What made you think of that? 🤔",
                "I wanna hear more about this! Keep going",
                "Keep talking babe, I love hearing you talk 💕",
                "What else? I'm curious now! Tell me everything",
                "Go on, I'm paying attention to every word 😊",
                "Interesting... tell me more? I'm intrigued",
                "Wait that's actually really cool, continue!"
            ]
            return self._get_varied_response(responses)
    
    def _get_varied_response(self, responses: List[str]) -> str:
        """Get a varied response, avoiding the last one used."""
        available = [r for r in responses if r != self.last_response]
        if not available:
            available = responses
        return random.choice(available)
    
    def _extract_context_keywords(self) -> dict:
        """Extract important keywords and topics from recent conversation."""
        if len(self.conversation_history) < 2:
            return {}
        
        recent = self.conversation_history[-6:]
        text = " ".join([msg['content'].lower() for msg in recent])
        
        keywords = {
            'emotions': [],
            'topics': [],
            'time_refs': [],
            'actions': []
        }
        
        # Detect emotions
        emotion_words = {
            'happy': ['good', 'great', 'happy', 'amazing', 'wonderful', 'awesome'],
            'sad': ['sad', 'upset', 'hurt', 'crying', 'depressed'],
            'tired': ['tired', 'exhausted', 'drained', 'sleepy'],
            'stressed': ['stressed', 'anxious', 'worried', 'overwhelming'],
            'excited': ['excited', 'cant wait', 'pumped', 'looking forward']
        }
        
        for emotion, words in emotion_words.items():
            if any(word in text for word in words):
                keywords['emotions'].append(emotion)
        
        # Detect topics
        if any(word in text for word in ['work', 'job', 'boss', 'office', 'meeting']):
            keywords['topics'].append('work')
        if any(word in text for word in ['day', 'today', 'yesterday']):
            keywords['topics'].append('daily_life')
        if any(word in text for word in ['we', 'us', 'together', 'relationship']):
            keywords['topics'].append('relationship')
        if any(word in text for word in ['miss', 'away', 'distance', 'far']):
            keywords['topics'].append('missing')
        
        return keywords
    
    def _try_contextual_response(self, message_lower: str, context: dict, mood: str) -> str:
        """Generate contextually aware responses based on conversation flow."""
        
        # Response to positive statements about recent events
        if message_lower in ['it was good', 'it went well', 'was good', 'pretty good']:
            if 'work' in context.get('topics', []):
                return self._get_varied_response([
                    "That's awesome! 😊 I'm so glad work went well today. What was the best part?",
                    "Yay!! 🥰 I knew today would be better. Tell me about it?",
                    "That's great baby! 💕 I'm happy to hear that. You feeling better about things now?"
                ])
            elif 'daily_life' in context.get('topics', []):
                return self._get_varied_response([
                    "Nice! 😊 I'm glad your day was good baby",
                    "That's great to hear! 💕 Mine was okay too",
                    "Awesome! 🥰 What made it good?"
                ])
        
        # Context-aware responses to hope/wish statements
        if any(phrase in message_lower for phrase in ['hope i', 'wish i', 'i hope', 'i wish']):
            if 'there' in message_lower or 'here' in message_lower:
                if 'missing' in context.get('topics', []):
                    return self._get_varied_response([
                        "God me too baby... 🥺💕 This distance is hard sometimes",
                        "I wish you were here too... so much 💔 Soon though okay?",
                        "Ugh I know... I miss having you here with me 😭"
                    ])
        
        # If expressing confusion/frustration in context
        if 'what' in message_lower and len(message_lower) < 15:
            if 'sad' in context.get('emotions', []) or 'stressed' in context.get('emotions', []):
                return self._get_varied_response([
                    "What's wrong baby? Talk to me 🥺",
                    "Hey... what happened? You okay? 💕",
                    "What is it babe? Something bothering you? 😟"
                ])
        
        return None  # No contextual match
    
    def _get_recent_topic(self) -> str:
        """Extract recent conversation topics for context."""
        if len(self.conversation_history) < 2:
            return ""
        
        recent_messages = self.conversation_history[-4:]
        text = " ".join([msg['content'].lower() for msg in recent_messages])
        return text
    
    def _try_quick_response(self, message_lower: str, mood: str) -> str:
        """INSTANT responses for common phrases - bypasses model for speed."""
        
        # Ultra-common phrases (INSTANT - 0.001s response time)
        quick_map = {
            'i love you': ['I love you too baby ❤️', 'I love you MORE 💕', 'I love you so much 🥰'],
            'love you': ['Love you too!! 💕', 'Love you more 🥰', 'Love you always baby ❤️'],
            'i miss you': ['I miss you too!! 🥺 Can\'t wait to see you', 'Miss you SO much baby 💔', 'Aww I miss you too!! 😭💕'],
            'miss you': ['I miss you too babe!! 🥺', 'Miss you so much 💔', 'Aww I miss you too!! 💕'],
            'i miss u': ['I miss you too baby!! 🥺 When can we see each other?', 'Miss you so much 💔', 'Aww I miss u too!! 😭'],
            'miss u': ['Miss you too!! 🥺', 'I miss you too baby 💕', 'Aww miss you! 😭'],
            'goodnight': ['Goodnight handsome! 😘 Sweet dreams about me', 'Sleep well baby 💕 text me tomorrow', 'Goodnight my love 🥰 sleep tight'],
            'good morning': ['Good morning!! 😊 Did you sleep well?', 'Morning handsome! 🥰', 'Good morning baby!! 💕'],
            'hey': ['Hey you!! 😊', 'Hey babe! 💕', 'Hi handsome! 😘'],
            'hi': ['Hi baby!! 🥰', 'Heyy! 😊', 'Hiii!! 💕'],
            'you there': ['Yes baby! What\'s up? 😊', 'I\'m here!! 💕', 'Always here for you ❤️'],
            'are you there': ['Yes I\'m here!! 😊', 'Of course babe! What do you need? 💕', 'I\'m here baby ❤️'],
            'how are you': ['I\'m good! How are YOU? 😊', 'Better now that I\'m talking to you 🥰', 'I\'m great! Miss you though 🥺'],
            'what are you doing': ['Just thinking about you... as usual 😊', 'Nothing much, wishing you were here 🥺', 'Texting my favorite person 💕'],
            'wyd': ['Thinking about you 💭', 'Missing you 🥺', 'Texting you obviously 😊'],
            'what you doing': ['Nothing much, just thinking about you 💕', 'Missing you! What about you? 🥺', 'Just wishing you were here 😔'],
            'come over': ['On my way baby!! 🏃\u200d♀️', 'Already heading there! 😊', 'Be there soon!! 💕'],
            'send pic': ['What kind of pic? 😏', 'Of what baby? 😊', 'You first 😘'],
        }
        
        for phrase, responses in quick_map.items():
            if phrase in message_lower:
                return random.choice(responses)
        
        return None  # No quick match, use model
    
    def _add_emotional_nuance(self, response: str, mood: str) -> str:
        """Add emotional depth based on mood - makes responses feel more real."""
        
        # Responses already have emojis built in - just ensure variety
        # Could add mood-specific emphasis here if needed
        
        # Add occasional emphasis based on mood
        if mood == 'passionate' and random.random() < 0.3:
            if '...' not in response and random.random() < 0.5:
                response = response.rstrip('.!') + '...'
        
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
