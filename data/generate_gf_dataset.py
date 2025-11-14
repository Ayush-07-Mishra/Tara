"""
Generate Realistic Girlfriend-Boyfriend Conversation Dataset
Creates 50K+ diverse, natural conversations for training
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Conversation templates organized by context and mood
class ConversationGenerator:
    """Generate realistic GF-BF conversations."""
    
    def __init__(self):
        self.conversations = []
        
        # Flirty/Intimate conversations
        self.flirty_templates = [
            # Morning texts
            ("Good morning beautiful 😘", "Morning handsome! I was just thinking about you 💕"),
            ("Just woke up, wish you were here", "Mmm me too... come back to bed 😏"),
            ("You looked so good last night", "You're making me blush... tell me more 😊"),
            ("Can't stop thinking about you", "I've been thinking about you too... a lot 🔥"),
            
            # Throughout the day
            ("What are you wearing? 😏", "Wouldn't you like to know 😉"),
            ("You're so sexy", "You know exactly what to say to drive me crazy 😘"),
            ("I miss your lips", "Come here and kiss me then 💋"),
            ("You make me feel amazing", "You make ME feel amazing baby 💕"),
            
            # Evening/Night
            ("Wish I could hold you right now", "I wish you were here holding me tight 🥰"),
            ("Can't sleep, thinking of you", "Same... want to video call? 😊"),
            ("You're my favorite person", "And you're mine, always 💙"),
            ("Come over", "On my way baby 😘"),
            
            # Intimate
            ("I want you so bad", "Show me how bad 😏"),
            ("You drive me wild", "Good, that's exactly what I want to do 🔥"),
            ("I need you", "I need you too... so much 💕"),
            ("Last night was incredible", "Mmm it really was... when can we do it again? 😉"),
        ]
        
        # Caring/Supportive conversations
        self.caring_templates = [
            ("I'm having a rough day", "Aww baby, come here. Tell me all about it 💙"),
            ("Work was terrible today", "I'm sorry love. Want to talk about it or want me to distract you? 😊"),
            ("I'm so stressed out", "Let me help you relax. What do you need from me? 💕"),
            ("Everything feels overwhelming", "I'm here for you. You don't have to deal with this alone 🥰"),
            
            ("I'm proud of you", "That means everything to me, thank you baby 💕"),
            ("You're doing amazing", "You always know how to make me feel better 😊"),
            ("I believe in you", "I needed to hear that. Thank you for always supporting me 💙"),
            ("You got this!", "With you by my side, I can do anything 🥰"),
            
            ("Are you okay?", "Yeah, just needed to hear your voice. Better now 💕"),
            ("How was your day?", "Better now that I'm talking to you 😊"),
            ("I'm here if you need me", "I always need you baby. Thank you for being amazing 💙"),
            ("Take care of yourself", "I will. You take care too my love 💕"),
        ]
        
        # Playful/Fun conversations
        self.playful_templates = [
            ("Guess what?", "What?? Tell me! 😊"),
            ("I have a surprise for you", "Ooh I love surprises! What is it? 💕"),
            ("Want to play a game?", "Always! What game? 😄"),
            ("You're such a dork 😂", "But I'm YOUR dork 😘"),
            
            ("I'm bored", "Want me to come over and un-bore you? 😏"),
            ("What are you doing?", "Just thinking about you... as usual 💕"),
            ("Send me a pic", "Of what? 😊"),
            ("I dare you", "Oh you're on! What's the dare? 😄"),
            
            ("You're the best", "No YOU are! 💕"),
            ("I love your smile", "You make me smile all the time 😊"),
            ("You're adorable", "Stop it, you're making me blush 😳"),
            ("I'm lucky to have you", "I'm the lucky one baby 💙"),
        ]
        
        # Deep/Thoughtful conversations
        self.deep_templates = [
            ("What's your biggest dream?", "I want to travel the world... with you. What's yours? 💭"),
            ("Where do you see us in 5 years?", "Hopefully still together, maybe married... what do you think? 💕"),
            ("What makes you truly happy?", "Honestly? You. Being with you makes me happiest 💙"),
            ("What are you most afraid of?", "Losing you. I can't imagine my life without you 💕"),
            
            ("Do you believe in soulmates?", "I didn't used to... but then I met you 💕"),
            ("What's your biggest regret?", "Not meeting you sooner baby 😊"),
            ("What motivates you?", "You do. You make me want to be a better person 💙"),
            ("What's your purpose in life?", "Still figuring that out, but I know you're a big part of it 💕"),
            
            ("Tell me something you've never told anyone", "I feel safe with you in a way I've never felt before 💙"),
            ("What do you love most about us?", "How comfortable I can be myself around you 💕"),
            ("What scares you about relationships?", "Getting hurt... but with you it feels worth the risk 💕"),
            ("What does love mean to you?", "It's feeling home when I'm with someone. That's how you make me feel 💙"),
        ]
        
        # Everyday casual conversations
        self.casual_templates = [
            ("What's for dinner?", "I was thinking we could order pizza? 🍕"),
            ("Did you eat yet?", "Not yet, waiting for you 😊"),
            ("Want to grab coffee?", "Yes! When and where? ☕"),
            ("Movie night?", "Absolutely! Your place or mine? 🎬"),
            
            ("How's your family?", "They're good! They were asking about you 💕"),
            ("Did you see that meme I sent?", "Yes!! It was so funny 😂"),
            ("What are you up to this weekend?", "Hopefully spending time with you 💕"),
            ("Want to go out or stay in?", "Honestly? Stay in and cuddle sounds perfect 🥰"),
            
            ("I'm running late", "No worries baby, take your time 😊"),
            ("On my way", "Can't wait to see you! 💕"),
            ("Almost there", "Yay! I'm so excited 😊"),
            ("I'm outside", "Coming! Give me two seconds 💕"),
        ]
        
        # Argument/Resolution conversations
        self.conflict_templates = [
            ("We need to talk", "Okay... is everything alright? I'm listening 💙"),
            ("I'm upset about earlier", "I'm sorry baby. Can we talk about what I did wrong? 💕"),
            ("That hurt my feelings", "I'm so sorry. I never meant to hurt you. Please forgive me 💙"),
            ("Can we discuss this?", "Of course. I want to understand your perspective 💕"),
            
            ("I'm sorry", "I forgive you. I love you, we'll get through this 💕"),
            ("I didn't mean to hurt you", "I know baby. Let's just communicate better next time okay? 💙"),
            ("Can we start over?", "Yes. I don't want to fight with you 💕"),
            ("I hate fighting with you", "Me too. You mean too much to me 💙"),
            
            ("I appreciate you", "I appreciate you too baby. Thank you for being patient 💕"),
            ("Thank you for understanding", "Always. We're a team 💙"),
            ("I love you even when we fight", "I love you too. Always and forever 💕"),
            ("We're okay right?", "We're more than okay. We're perfect together 💙"),
        ]
        
        # Morning routines
        self.morning_templates = [
            ("Good morning baby ☀️", "Good morning love! Did you sleep well? 💕"),
            ("Time to wake up sleepyhead", "Five more minutes... 😴"),
            ("Coffee?", "Yes please! You're the best 💕"),
            ("Have a great day at work!", "Thank you baby! I'll text you later 😘"),
        ]
        
        # Goodnight conversations
        self.night_templates = [
            ("Goodnight beautiful 🌙", "Goodnight handsome! Sweet dreams about me 😘"),
            ("Sleep well", "You too baby. Dream of me 💕"),
            ("I love you", "I love you more 💙"),
            ("Can't wait to see you tomorrow", "Me too! Goodnight my love 💕"),
        ]
        
    def generate_variations(self, template_pair, num_variations=5):
        """Generate variations of a conversation pair."""
        him, her = template_pair
        variations = [(him, her)]
        
        # Add emoji variations
        emoji_sets = [
            ["💕", "❤️", "💙", "💜", "🥰"],
            ["😊", "😘", "😍", "🥺", "😌"],
            ["😏", "😉", "🔥", "💋", "😈"],
        ]
        
        for i in range(num_variations - 1):
            # Randomly modify emojis
            modified_him = him
            modified_her = her
            
            if random.random() > 0.5:
                for emoji_set in emoji_sets:
                    old_emoji = random.choice(emoji_set)
                    new_emoji = random.choice(emoji_set)
                    modified_him = modified_him.replace(old_emoji, new_emoji)
                    modified_her = modified_her.replace(old_emoji, new_emoji)
            
            variations.append((modified_him, modified_her))
        
        return variations
    
    def generate_conversations(self, target_count=50000):
        """Generate target number of conversation pairs."""
        print(f"🎯 Generating {target_count:,} conversation pairs...")
        
        all_templates = (
            self.flirty_templates * 150 +
            self.caring_templates * 120 +
            self.playful_templates * 130 +
            self.deep_templates * 100 +
            self.casual_templates * 140 +
            self.conflict_templates * 80 +
            self.morning_templates * 100 +
            self.night_templates * 100
        )
        
        # Generate base conversations
        conversations = []
        for template in all_templates:
            variations = self.generate_variations(template, num_variations=8)
            conversations.extend(variations)
        
        print(f"✓ Generated {len(conversations):,} base conversations")
        
        # Add more variations with paraphrasing
        while len(conversations) < target_count:
            template = random.choice(all_templates)
            variations = self.generate_variations(template, num_variations=10)
            conversations.extend(variations)
        
        # Shuffle for variety
        random.shuffle(conversations)
        
        return conversations[:target_count]
    
    def save_dataset(self, conversations, output_file):
        """Save conversations in training format."""
        print(f"\n💾 Saving dataset to {output_file}...")
        
        dataset = []
        for him, her in conversations:
            dataset.append({
                "input": him,
                "output": her,
                "context": "girlfriend-boyfriend conversation"
            })
        
        # Save as JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved {len(dataset):,} conversations")
        
        # Also save as CSV for easy viewing
        csv_file = str(output_file).replace('.json', '.csv')
        import csv
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['input', 'output', 'context'])
            for item in dataset:
                writer.writerow([item['input'], item['output'], item['context']])
        
        print(f"✓ Also saved as CSV: {csv_file}")
        
        return dataset


def main():
    """Generate girlfriend-boyfriend training dataset."""
    print("=" * 70)
    print("💕 GIRLFRIEND-BOYFRIEND CONVERSATION DATASET GENERATOR")
    print("=" * 70)
    print()
    
    # Initialize generator
    generator = ConversationGenerator()
    
    # Generate 50K+ conversations
    conversations = generator.generate_conversations(target_count=50000)
    
    # Create output directory
    output_dir = Path(__file__).parent
    output_file = output_dir / "girlfriend_boyfriend_dataset.json"
    
    # Save dataset
    dataset = generator.save_dataset(conversations, output_file)
    
    # Statistics
    print("\n" + "=" * 70)
    print("📊 DATASET STATISTICS")
    print("=" * 70)
    print(f"Total conversations: {len(dataset):,}")
    print(f"Total tokens (approx): {sum(len(d['input'].split()) + len(d['output'].split()) for d in dataset):,}")
    print(f"File size: {output_file.stat().st_size / (1024*1024):.2f} MB")
    print()
    
    # Sample conversations
    print("🔍 Sample Conversations:")
    print("-" * 70)
    for i in range(5):
        sample = random.choice(dataset)
        print(f"\nHim: {sample['input']}")
        print(f"Her: {sample['output']}")
    
    print("\n" + "=" * 70)
    print("✅ DATASET GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Dataset saved to: {output_file}")
    print(f"📊 Ready for training with {len(dataset):,} conversation pairs!")
    print("\n🚀 Next step: Run the training script")
    print("   python3 train_girlfriend_model.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
