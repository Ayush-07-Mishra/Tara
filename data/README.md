# Stress Dataset Labeling Guide

## Overview
This dataset contains ~300 text examples labeled as `low`, `medium`, or `high` stress levels. The goal is to train a classifier that can automatically detect stress levels in user messages.

## Labeling Guidelines

### Low Stress (100 examples)
**Characteristics:**
- Calm, peaceful language
- Positive or neutral tone
- Words like: "okay", "fine", "managing", "good", "calm", "relaxed", "peaceful"
- No urgency or pressure
- Describes routine activities or positive experiences
- Expresses contentment or satisfaction

**Examples:**
- "I'm feeling okay today. Just a bit tired from work."
- "Everything is going smoothly. No major concerns."
- "Just enjoying a peaceful evening."

---

### Medium Stress (100 examples)
**Characteristics:**
- Noticeable concern or worry
- Manageable but present pressure
- Words like: "stressed", "worried", "anxious", "pressure", "overwhelming", "struggling", "difficult"
- Describes challenges but still coping
- May mention multiple responsibilities or deadlines
- Some emotional strain but not crisis level

**Examples:**
- "I'm feeling a bit stressed with all the deadlines coming up."
- "Work has been overwhelming lately but I'm managing."
- "So many things to do and not enough time."

---

### High Stress (100 examples)
**Characteristics:**
- Severe distress or crisis language
- Intense emotional language (often with caps, exclamation marks)
- Words like: "can't handle", "breaking down", "falling apart", "drowning", "crushing", "unbearable", "panic", "crisis", "desperate"
- Expressions of being overwhelmed beyond coping
- Physical symptoms mentioned (can't breathe, shaking, etc.)
- Loss of control or hopelessness

**Examples:**
- "I CAN'T HANDLE THIS ANYMORE! Everything is falling apart!"
- "I'm completely overwhelmed and breaking down."
- "This is unbearable. I don't know how much more I can take."

---

## Distribution
- **Low stress**: 100 examples (~33%)
- **Medium stress**: 100 examples (~33%)
- **High stress**: 100 examples (~33%)

Total: 300 examples

## Usage
1. Load the CSV file (`stress_dataset.csv`)
2. Split into train/test sets (80/20 or 5-fold cross-validation)
3. Preprocess text (lowercase, remove special chars, but keep negations)
4. Vectorize using TF-IDF (unigrams + bigrams)
5. Train SVM classifier with CalibratedClassifierCV for probabilities
6. Evaluate on test set

## Quality Checks
✅ Balanced distribution across classes
✅ Diverse vocabulary and scenarios
✅ Realistic, natural language
✅ Clear distinction between stress levels
✅ No personal identifiable information
✅ Covers various domains (work, relationships, health, general)

## Next Steps
Use the Colab training notebook (`train_stress_model_colab.ipynb`) to train the classifier on this dataset.
