import json

# Load dataset
with open('data/final_training_dataset_100k.json', 'r') as f:
    data = json.load(f)

# Search for work-related conversations
keywords = ['manager', 'boss', 'work', 'stressed', 'rough day', 'bad day']

print("Searching for work/stress related conversations...\n")

matches = []
for item in data:
    input_lower = item['input'].lower()
    if any(kw in input_lower for kw in keywords):
        matches.append(item)

print(f"Found {len(matches)} matches\n")
print("Sample responses:\n")

# Show 15 samples
for i, match in enumerate(matches[:15], 1):
    print(f"{i}. Input: '{match['input']}'")
    print(f"   Output: '{match['output']}'")
    print()
