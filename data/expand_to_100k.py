"""
Expand the dataset to 100K+ by creating realistic variations
Takes the existing dataset and multiplies it with realistic patterns
"""

import json
import random
from pathlib import Path

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def expand_dataset():
    """Expand dataset to 100k+ conversations."""
    
    data_dir = Path(__file__).parent
    input_file = data_dir / "final_training_dataset.json"
    
    print("Loading existing dataset...")
    conversations = load_json(input_file)
    print(f"Loaded {len(conversations):,} conversations")
    
    expanded = list(conversations)  # Start with original
    
    # Add time variations
    print("\nAdding time-based variations...")
    time_additions = {
        "morning": [" this morning", " in the morning"],
        "night": [" tonight", " at night"],
        "day": [" today", " this afternoon"],
        "evening": [" this evening"],
    }
    
    for convo in list(conversations):
        for time_word, additions in time_additions.items():
            if time_word in convo["input"] or random.random() < 0.1:
                for addition in additions:
                    if addition not in convo["input"]:
                        expanded.append({
                            "input": convo["input"] + addition,
                            "output": convo["output"],
                            "category": convo.get("category", "unknown") + "_time_var"
                        })
    
    print(f"After time variations: {len(expanded):,}")
    
    # Add prefix variations
    print("Adding prefix variations...")
    prefixes = ["hey ", "so ", "um ", "like ", "babe ", "baby "]
    
    sample = random.sample(conversations, min(15000, len(conversations)))
    for convo in sample:
        for prefix in prefixes:
            if not convo["input"].startswith(tuple(prefixes)):
                expanded.append({
                    "input": prefix + convo["input"],
                    "output": convo["output"],
                    "category": convo.get("category", "unknown") + "_prefix"
                })
    
    print(f"After prefix variations: {len(expanded):,}")
    
    # Add suffix variations
    print("Adding suffix variations...")
    suffixes = [" babe", " baby", " love", " ?", " tho", " though", " rn", " lol"]
    
    sample = random.sample(conversations, min(15000, len(conversations)))
    for convo in sample:
        for suffix in suffixes:
            if not convo["input"].endswith(tuple(suffixes)):
                expanded.append({
                    "input": convo["input"] + suffix,
                    "output": convo["output"],
                    "category": convo.get("category", "unknown") + "_suffix"
                })
    
    print(f"After suffix variations: {len(expanded):,}")
    
    # Add repetition for emphasis
    print("Adding repetition variations...")
    emphasis_words = {
        "so": "sooo",
        "very": "veryyy",
        "really": "reallyyy",
        "yes": "yesss",
        "no": "noooo",
        "hey": "heyyyy",
        "hi": "hiii",
        "please": "pleasee",
        "love": "lovee",
        "miss": "missss",
    }
    
    sample = random.sample(conversations, min(10000, len(conversations)))
    for convo in sample:
        for word, emphasized in emphasis_words.items():
            if word in convo["input"]:
                new_input = convo["input"].replace(word, emphasized)
                if new_input != convo["input"]:
                    expanded.append({
                        "input": new_input,
                        "output": convo["output"],
                        "category": convo.get("category", "unknown") + "_emphasis"
                    })
    
    print(f"After emphasis variations: {len(expanded):,}")
    
    # Add multiple punctuation variations
    print("Adding extended punctuation...")
    
    sample = random.sample(conversations, min(5000, len(conversations)))
    for convo in sample:
        for i in range(3):  # Create 3 variations per conversation
            punct = random.choice(["!!", "!!!", "?!", "??", "...", "!", "?"])
            expanded.append({
                "input": convo["input"] + punct,
                "output": convo["output"],
                "category": convo.get("category", "unknown") + "_extended_punct"
            })
    
    print(f"After extended punctuation: {len(expanded):,}")
    
    # Remove duplicates
    print("\nRemoving duplicates...")
    seen = set()
    unique = []
    for convo in expanded:
        key = (convo["input"].lower().strip(), convo["output"].strip())
        if key not in seen:
            seen.add(key)
            unique.append(convo)
    
    print(f"Removed {len(expanded) - len(unique):,} duplicates")
    print(f"Final size: {len(unique):,}")
    
    # Save
    output_file = data_dir / "final_training_dataset_100k.json"
    save_json(unique, output_file)
    
    print(f"\n{'='*60}")
    print(f"✅ Expanded dataset saved to: {output_file}")
    print(f"Total conversations: {len(unique):,}")
    print(f"{'='*60}")
    
    # Statistics
    categories = {}
    for convo in unique:
        cat = convo.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nTop 20 Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {cat}: {count:,}")

if __name__ == "__main__":
    expand_dataset()
