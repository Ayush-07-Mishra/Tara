"""
Merge all datasets and create final training dataset
Combines massive_girlfriend_dataset.json with existing datasets
"""

import json
import os
from pathlib import Path

def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """Save JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    data_dir = Path(__file__).parent
    
    print("Loading all datasets...")
    
    # Load all available datasets
    all_conversations = []
    
    datasets = [
        "massive_girlfriend_dataset.json",
        "girlfriend_boyfriend_advanced.json",
        "girlfriend_complete_dataset.json",
    ]
    
    for dataset_file in datasets:
        filepath = data_dir / dataset_file
        if filepath.exists():
            data = load_json(filepath)
            print(f"Loaded {len(data):,} conversations from {dataset_file}")
            all_conversations.extend(data)
        else:
            print(f"Warning: {dataset_file} not found, skipping...")
    
    # Remove duplicates
    print("\nRemoving duplicates...")
    seen = set()
    unique_conversations = []
    
    for convo in all_conversations:
        # Create a key from input-output pair
        key = (convo.get("input", "").lower().strip(), convo.get("output", "").strip())
        if key not in seen and key[0] and key[1]:  # Ensure both input and output exist
            seen.add(key)
            unique_conversations.append(convo)
    
    print(f"Removed {len(all_conversations) - len(unique_conversations):,} duplicates")
    print(f"Final dataset size: {len(unique_conversations):,} unique conversations")
    
    # Save merged dataset
    output_file = data_dir / "final_training_dataset.json"
    save_json(unique_conversations, output_file)
    
    print(f"\n{'='*60}")
    print(f"✅ Final dataset saved to: {output_file}")
    print(f"Total conversations: {len(unique_conversations):,}")
    print(f"{'='*60}")
    
    # Print statistics
    categories = {}
    for convo in unique_conversations:
        cat = convo.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nTop 30 Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:30]:
        print(f"  {cat}: {count:,}")
    
    # Also create a CSV version for easy inspection
    print("\nCreating CSV version for inspection...")
    csv_file = data_dir / "final_training_dataset.csv"
    
    import csv
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['input', 'output', 'category'])
        writer.writeheader()
        for convo in unique_conversations:
            writer.writerow({
                'input': convo.get('input', ''),
                'output': convo.get('output', ''),
                'category': convo.get('category', 'unknown')
            })
    
    print(f"CSV version saved to: {csv_file}")
    print("\n✅ All done! You can now use final_training_dataset.json for training.")

if __name__ == "__main__":
    main()
