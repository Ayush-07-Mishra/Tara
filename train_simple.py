"""
Simple Fast Training for Girlfriend AI
Optimized to actually work and complete training
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import json
import os

print("=" * 80)
print("💕 TRAINING CUSTOM GIRLFRIEND AI MODEL")
print("=" * 80)

# Use CPU to avoid Metal hanging issues
device = "cpu"
print(f"\n✅ Using device: {device}")

# Load data
print("\n📂 Loading training data...")
with open("data/girlfriend_boyfriend_dataset.json", 'r') as f:
    data = json.load(f)
print(f"✓ Loaded {len(data):,} conversation pairs")

# Format data
def format_convo(item):
    return {
        'text': f"Boyfriend: {item['input']}\nGirlfriend: {item['output']}\n"
    }

print("\n🔄 Formatting conversations...")
formatted = [format_convo(item) for item in data]
dataset = Dataset.from_list(formatted)

# Split
split = dataset.train_test_split(test_size=0.05, seed=42)
train_data = split['train']
eval_data = split['test']
print(f"  Train: {len(train_data):,} | Validation: {len(eval_data):,}")

# Load model - using much smaller GPT-2 for faster training
MODEL = "gpt2"  # Only 124M parameters - much faster!
print(f"\n🤖 Loading {MODEL} (small & fast)...")
print("   (Loading...)")

tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(MODEL)
print("✓ Model loaded!")

# Tokenize
def tokenize(examples):
    return tokenizer(examples['text'], truncation=True, max_length=128, padding='max_length')

print("\n🔤 Tokenizing dataset...")
train_tok = train_data.map(tokenize, batched=True, remove_columns=['text'])
eval_tok = eval_data.map(tokenize, batched=True, remove_columns=['text'])
print("✓ Tokenization complete!")

# Training config
os.makedirs("girlfriend_model", exist_ok=True)

training_args = TrainingArguments(
    output_dir="girlfriend_model",
    num_train_epochs=1,  # Just 1 epoch for faster training
    per_device_train_batch_size=2,  # Small batch for CPU
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_steps=100,
    save_steps=500,
    eval_steps=500,
    save_total_limit=2,
    fp16=False,  # No FP16 on CPU
    logging_dir="girlfriend_model/logs",
    report_to="none",
    load_best_model_at_end=True,
)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tok,
    eval_dataset=eval_tok,
    data_collator=data_collator,
)

# Train!
print("\n🚀 Starting training...")
print("   This will take 2-4 hours")
print("   Progress will be shown below:\n")

trainer.train()

# Save
print("\n💾 Saving model...")
trainer.save_model("girlfriend_model/final_model")
tokenizer.save_pretrained("girlfriend_model/final_model")

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)
print(f"\n📁 Model saved to: girlfriend_model/final_model")
print("\nTo use your custom model, update girlfriend_ai.py line 51:")
print('   MODEL_NAME = "girlfriend_model/final_model"')
print("\n💕 Your custom girlfriend AI is ready!")
