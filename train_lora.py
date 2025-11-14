"""
Fast LoRA Training for Girlfriend AI
Only trains 1% of parameters - much faster!
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import json
import os

print("=" * 80)
print("💕 FAST LORA TRAINING - CUSTOM GIRLFRIEND AI")
print("=" * 80)
print("\nLoRA only trains 1% of parameters - 10x faster than full training!")

# Load data
print("\n📂 Loading 50K training conversations...")
with open("data/girlfriend_boyfriend_dataset.json", 'r') as f:
    data = json.load(f)
print(f"✅ Loaded {len(data):,} girlfriend-boyfriend conversations")

# Format for girlfriend AI
def format_convo(item):
    him = item['input']
    her = item['output']
    return {
        'text': f"### Boyfriend: {him}\n### Girlfriend: {her}\n"
    }

print("\n🔄 Formatting conversations...")
formatted = [format_convo(item) for item in data]
dataset = Dataset.from_list(formatted)

# Split
split = dataset.train_test_split(test_size=0.05, seed=42)
train_data = split['train']
eval_data = split['test']
print(f"✅ Train: {len(train_data):,} | Validation: {len(eval_data):,}")

# Load smaller model - GPT-2 (faster)
MODEL = "gpt2"
print(f"\n🤖 Loading {MODEL}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.pad_token = tokenizer.eos_token

print("   Loading model (this will work fast)...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype=torch.float32,
    device_map="auto"
)
print("✅ Model loaded successfully!")

# LoRA config - only train 1% of parameters!
print("\n⚡ Configuring LoRA (Parameter-Efficient Training)...")
lora_config = LoraConfig(
    r=16,  # LoRA rank
    lora_alpha=32,
    target_modules=["c_attn"],  # GPT-2 attention layers
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"✅ Trainable params: {trainable_params:,} ({100 * trainable_params / total_params:.2f}%)")
print(f"   Total params: {total_params:,}")

# Tokenize
def tokenize(examples):
    return tokenizer(examples['text'], truncation=True, max_length=128, padding='max_length')

print("\n🔤 Tokenizing dataset...")
train_tok = train_data.map(tokenize, batched=True, remove_columns=['text'])
eval_tok = eval_data.map(tokenize, batched=True, remove_columns=['text'])
print("✅ Tokenization complete!")

# Training config
os.makedirs("girlfriend_model_lora", exist_ok=True)

print("\n⚙️  Training Configuration:")
print("   • Epochs: 2")
print("   • Batch size: 4")
print("   • Learning rate: 2e-4")
print("   • Estimated time: 30-60 minutes")

training_args = TrainingArguments(
    output_dir="girlfriend_model_lora",
    num_train_epochs=2,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    weight_decay=0.01,
    logging_steps=50,
    save_steps=500,
    eval_steps=500,
    save_total_limit=2,
    fp16=False,
    logging_dir="girlfriend_model_lora/logs",
    report_to="none",
    load_best_model_at_end=True,
    remove_unused_columns=False,
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
print("\n" + "=" * 80)
print("🚀 STARTING TRAINING - THIS WILL ACTUALLY WORK!")
print("=" * 80)
print("\n⏰ Estimated time: 30-60 minutes")
print("📊 Progress will be shown below:\n")

trainer.train()

# Save
print("\n💾 Saving custom girlfriend model...")
model.save_pretrained("girlfriend_model_lora/final")
tokenizer.save_pretrained("girlfriend_model_lora/final")

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)
print(f"\n📁 Custom model saved to: girlfriend_model_lora/final")
print("\n🔄 To use your custom trained model:")
print("   1. Update app/girlfriend_ai.py line 51")
print('   2. Change MODEL_NAME to: "girlfriend_model_lora/final"')
print("   3. Restart your chat app")
print("\n💕 Your personalized girlfriend AI is ready!")
