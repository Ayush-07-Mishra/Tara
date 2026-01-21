import json
from collections import Counter

# Load dataset
with open('data/final_training_dataset_100k.json', 'r') as f:
    data = json.load(f)

print('='*70)
print('📊 DATASET STATISTICS')
print('='*70)
print(f'Total Conversations: {len(data):,}')
print()

# Category breakdown
categories = {}
for convo in data:
    cat = convo.get('category', 'unknown')
    # Simplify category name
    base_cat = cat.split('_')[0] if '_' in cat else cat
    categories[base_cat] = categories.get(base_cat, 0) + 1

print('Top 15 Base Categories:')
for i, (cat, count) in enumerate(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:15], 1):
    pct = (count / len(data)) * 100
    print(f'{i:2d}. {cat:30s} {count:8,} ({pct:5.1f}%)')

print()

# Length analysis
input_lengths = [len(c['input']) for c in data[:10000]]
output_lengths = [len(c['output']) for c in data[:10000]]

print('Length Analysis (sample of 10,000):')
print(f'  Avg Input Length:  {sum(input_lengths)/len(input_lengths):.1f} chars')
print(f'  Avg Output Length: {sum(output_lengths)/len(output_lengths):.1f} chars')
print()

# Common inputs
inputs = Counter([c['input'] for c in data])
print('Most Common Inputs (Top 10):')
for i, (inp, count) in enumerate(inputs.most_common(10), 1):
    print(f'{i:2d}. "{inp[:40]}" - {count:4d} variations')

print()
print('='*70)
print('✅ Dataset is ready for training!')
print('   File: data/final_training_dataset_100k.json')
print('='*70)
