# Tara AI - Streamlit Cloud Deployment Guide

## ✅ Pre-Deployment Checklist

### Files Renamed:
- ✅ `app/girlfriend_ai.py` → `app/tara_ai.py`
- ✅ `app/girlfriend_chat.py` → `app/tara_chat.py`
- ✅ Class `GirlfriendAI` → `TaraAI`
- ✅ All imports updated
- ✅ Branding changed to "Tara AI"

### Configuration Files:
- ✅ `requirements.txt` - Simplified for Streamlit Cloud
- ✅ `.streamlit/config.toml` - Theme and server settings
- ✅ `packages.txt` - System dependencies (empty - none needed)

---

## 🚀 Deployment Steps

### 1. Push to GitHub

```bash
cd /Users/ayushmishra/Desktop/Project/AI_Girl
git add .
git commit -m "Rename to Tara AI and prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Repository: `Ayush-07-Mishra/AI_Girl`
4. Branch: `main`
5. Main file path: `app/tara_chat.py`
6. Click "Deploy"

---

## 📋 Important Notes

### Simplified Requirements:
The `requirements.txt` has been streamlined to avoid dependency conflicts on Streamlit Cloud:

```
streamlit>=1.28.0
transformers>=4.35.0
torch>=2.1.0
sentencepiece>=0.1.99
```

### What Was Removed:
- Strict version pins (==) replaced with minimum versions (>=)
- Unnecessary packages (scikit-learn, joblib, pandas, numpy, regex, accelerate, protobuf, einops, praw, requests)
- These were either:
  - Already included as dependencies of transformers/torch
  - Not used in the core app functionality
  - Causing version conflicts on Streamlit Cloud

### Dataset:
- The 297K conversation dataset (`data/final_training_dataset_100k.json`) is 45MB
- Will be loaded from the repository (included in deployment)
- First load may take ~30 seconds on Streamlit Cloud

### Model Loading:
- TinyLlama-1.1B-Chat model (~2.2GB) will be downloaded on first run
- Streamlit Cloud will cache it for subsequent runs
- Initial deployment may take 5-10 minutes

---

## ⚡ Testing Locally

App is currently running at: http://localhost:8501

Test the renamed app:
```bash
streamlit run app/tara_chat.py
```

---

## 🔧 Troubleshooting

### If deployment fails with dependency errors:

1. **Check Python version**: Streamlit Cloud uses Python 3.11
2. **Try minimal requirements**:
   ```
   streamlit
   transformers
   torch
   sentencepiece
   ```

3. **Add to packages.txt if needed** (system dependencies):
   ```
   build-essential
   ```

### Common Issues:

**Issue**: "Module not found: tara_ai"
- **Fix**: Ensure `app/tara_ai.py` exists and is committed

**Issue**: "Dataset not found"
- **Fix**: Ensure `data/final_training_dataset_100k.json` is committed (check .gitignore)

**Issue**: "Torch installation failed"
- **Fix**: Change requirements.txt to use CPU version:
  ```
  torch>=2.1.0 --index-url https://download.pytorch.org/whl/cpu
  ```

---

## 📊 Expected Performance on Streamlit Cloud

- **First Load**: 5-10 minutes (model download + dataset loading)
- **Subsequent Loads**: 30-60 seconds (cached model)
- **Response Time**: 2-5 seconds per response (CPU-based inference)
- **Memory Usage**: ~4-5GB (within Streamlit Cloud free tier limits)

---

## 🎨 Branding

- **Name**: Tara AI
- **Tagline**: "Your Personal AI Companion"
- **Theme**: Neon pink (#FF006E) on dark background
- **Icon**: 💕

---

## 📝 Post-Deployment

After successful deployment:

1. Test all conversation flows
2. Verify dataset loading works
3. Check response quality
4. Monitor for any errors in Streamlit Cloud logs

---

## 🔒 Privacy & Security

- No data is stored on servers (conversation history is session-only)
- All processing happens in-memory
- Dataset is read-only
- No external API calls (except model download on first run)

---

## 📧 Support

If deployment issues persist, check:
- Streamlit Cloud logs: https://share.streamlit.io/
- GitHub repo issues: https://github.com/Ayush-07-Mishra/AI_Girl/issues
- Streamlit Community: https://discuss.streamlit.io/
