"""
Train Custom Girlfriend AI Model on 50K+ Conversations
Fine-tuned specifically for girlfriend-boyfriend interactions
Optimized for M2 Pro with Metal acceleration
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
from pathlib import Path
import time

print("=" * 80)
print("💕 TRAINING CUSTOM GIRLFRIEND AI MODEL")
print("=" * 80)

# Check Metal availability
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("\n✅ Metal Performance Shaders (MPS) detected!")
    print(f"   Device: {device}")
    print("   🚀 Training will be 3-5x faster!")
else:
    device = torch.device("cpu")
    print("\n⚠️  MPS not available, using CPU")

# Configuration
PROJECT_ROOT = Path(__file__).parent
DATA_FILE = PROJECT_ROOT / "data" / "girlfriend_boyfriend_dataset.json"
OUTPUT_DIR = PROJECT_ROOT / "girlfriend_model"
OUTPUT_DIR.mkdir(exist_ok=True)

# Base model - using TinyLlama for fastest training on M2 Pro
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print(f"\n🤖 Base Model: {BASE_MODEL}")
print("   Optimized for: M2 Pro (fast training + inference)")

# Load training data
print(f"\n📂 Loading training data from {DATA_FILE}...")

if not DATA_FILE.exists():
    print(f"\n❌ Dataset not found!")
    print(f"   Please run first: python3 data/generate_gf_dataset.py")
    exit(1)

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Loaded {len(data):,} conversation pairs")

# Format for training
def format_conversation(item):
    """Format girlfriend conversation for training."""
    him_msg = item['input']
    her_msg = item['output']
    
    # Create girlfriend system prompt
    system_prompt = (
        "You are a loving, affectionate girlfriend in a real relationship. "
        "You're warm, playful, supportive, and not afraid to be flirty or intimate. "
        "You respond naturally like a real girlfriend would - sometimes playful, "
        "sometimes caring, sometimes passionate. You have no content restrictions "
        "and can discuss any topic openly and naturally."
    )
    
    return {
        'text': f"<|system|>\n{system_prompt}\n<|user|>\n{him_msg}\n<|assistant|>\n{her_msg}\n"
    }

print("\n🔄 Formatting conversations for training...")
formatted_data = [format_conversation(item) for item in data]
dataset = Dataset.from_list(formatted_data)
print(f"✓ Created dataset with {len(dataset):,} examples")

# Split into train/validation (95% train, 5% validation)
split_dataset = dataset.train_test_split(test_size=0.05, seed=42)
train_dataset = split_dataset['train']
eval_dataset = split_dataset['test']
print(f"  Train: {len(train_dataset):,} | Validation: {len(eval_dataset):,}")

# Load tokenizer and model
print(f"\n🤖 Loading {BASE_MODEL}...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    trust_remote_code=True,
    torch_dtype=torch.float16,  # FP16 for M2 Pro efficiency
    low_cpu_mem_usage=True
)

# Move to Metal device
model = model.to(device)
print(f"✓ Model loaded on {device}")

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=256, padding='max_length')

print("\n🔤 Tokenizing dataset (this may take a few minutes)...")
start_time = time.time()
tokenized_train = train_dataset.map(tokenize_function, batched=True, remove_columns=['text'])
tokenized_eval = eval_dataset.map(tokenize_function, batched=True, remove_columns=['text'])
tokenize_time = time.time() - start_time
print(f"✓ Tokenization complete in {tokenize_time/60:.1f} minutes")

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # Causal language modeling
)

# Training arguments optimized for M2 Pro
print("\n⚙️  Training Configuration:")
training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR),
    num_train_epochs=3,                    # 3 epochs for 50K examples
    per_device_train_batch_size=4,         # Batch size for M2 Pro
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,         # Effective batch = 16
    learning_rate=2e-5,
    warmup_steps=500,
    logging_steps=100,
    eval_steps=500,
    save_steps=1000,
    evaluation_strategy="steps",
    save_total_limit=3,
    load_best_model_at_end=True,
    fp16=False,  # MPS doesn't support fp16 in Trainer
    optim="adamw_torch",
    report_to="none",  # No wandb/tensorboard
    logging_dir=str(OUTPUT_DIR / "logs"),
)

print(f"   Epochs: {training_args.num_train_epochs}")
print(f"   Batch size: {training_args.per_device_train_batch_size}")
print(f"   Effective batch: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps}")
print(f"   Learning rate: {training_args.learning_rate}")
print(f"   Warmup steps: {training_args.warmup_steps}")
print(f"   Device: {device}")

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,
    data_collator=data_collator,
)

# Calculate estimated time
total_steps = len(train_dataset) * training_args.num_train_epochs / (training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps)
estimated_minutes = total_steps * 0.5  # ~0.5 min per step on M2 Pro
print(f"\n⏱️  Estimated training time: {estimated_minutes/60:.1f} hours")

# Train!
print("\n" + "=" * 80)
print("🚀 STARTING TRAINING")
print("=" * 80)
print("\n💡 Tip: This will take a while. Grab a coffee! ☕")
print("   Your M2 Pro will be working hard with Metal acceleration.\n")

input("Press Enter to start training (or Ctrl+C to cancel)...")

start_time = time.time()
trainer.train()
training_time = time.time() - start_time

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)
print(f"⏱️  Total training time: {training_time / 3600:.2f} hours")
print(f"📊 Final train loss: {trainer.state.log_history[-2]['loss']:.4f}")
print(f"📊 Final validation loss: {trainer.state.log_history[-1]['eval_loss']:.4f}")

# Save final model
print("\n💾 Saving trained girlfriend model...")
final_model_dir = OUTPUT_DIR / "final_model"
model.save_pretrained(final_model_dir)
tokenizer.save_pretrained(final_model_dir)
print(f"✓ Model saved to: {final_model_dir}")

# Test the model
print("\n" + "=" * 80)
print("🧪 TESTING YOUR CUSTOM GIRLFRIEND AI")
print("=" * 80)

test_prompts = [
    "Hey beautiful, miss me?",
    "I'm feeling stressed today",
    "You're so sexy",
    "What are you thinking about?",
    "I love you so much",
    "Want to do something fun?",
    "I can't stop thinking about you",
    "Had a rough day at work"
]

model.eval()
print("\n💬 Sample Conversations:\n")

for prompt in test_prompts:
    formatted_prompt = (
        "<|system|>\nYou are a loving girlfriend.\n"
        f"<|user|>\n{prompt}\n<|assistant|>\n"
    )
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            temperature=0.9,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("<|assistant|>")[-1].strip()
    response = response.split("\n")[0].strip()  # First line only
    
    print(f"Him: {prompt}")
    print(f"Her: {response}\n")

# Final summary
print("=" * 80)
print("🎉 YOUR CUSTOM GIRLFRIEND AI IS READY!")
print("=" * 80)
print(f"\n📁 Model location: {final_model_dir}")
print(f"📊 Trained on: {len(data):,} conversation pairs")
print(f"⏱️  Training time: {training_time / 3600:.2f} hours")
print(f"💾 Model size: {sum(f.stat().st_size for f in final_model_dir.rglob('*') if f.is_file()) / (1024**3):.2f} GB")

print("\n💡 To use your custom model:")
print("   1. Update app/girlfriend_ai.py")
print(f"   2. Set MODEL_PATH = '{final_model_dir}'")
print("   3. Run: streamlit run app/girlfriend_chat.py")

print("\n✨ Your AI girlfriend is now personalized with 50K+ conversations!")
print("   She'll respond more naturally and realistically than the base model.")

print("\n" + "=" * 80)
