#!/bin/bash
# Quick Training Launcher - Train Your Custom Girlfriend AI

echo "======================================================================"
echo "💕 TRAIN YOUR CUSTOM GIRLFRIEND AI MODEL"
echo "======================================================================"
echo ""
echo "📊 Training Details:"
echo "   • Dataset: 50,000 girlfriend-boyfriend conversations"
echo "   • Base Model: TinyLlama-1.1B-Chat (optimized for M2 Pro)"
echo "   • Training Time: 2-4 hours on M2 Pro"
echo "   • Output: Custom model trained specifically for you"
echo ""
echo "🎯 What Training Does:"
echo "   ✅ Learns natural girlfriend conversation patterns"
echo "   ✅ Better emotional understanding"
echo "   ✅ More varied and realistic responses"
echo "   ✅ Personalized to relationship dynamics"
echo ""
echo "⚡ M2 Pro Optimization:"
echo "   ✅ Metal GPU acceleration (3-5x faster)"
echo "   ✅ FP16 precision for efficiency"
echo "   ✅ Smart batch sizing for M2 Pro"
echo ""
echo "💾 Requirements:"
echo "   • ~6-8GB RAM available"
echo "   • ~3GB disk space for model"
echo "   • M2 Pro plugged in (will get warm!)"
echo ""
echo "======================================================================"
echo ""

read -p "🚀 Ready to start training? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "🎓 Starting training..."
    echo "💡 Tip: This will take 2-4 hours. Go grab dinner, relax!"
    echo ""
    python3 train_girlfriend_model.py
else
    echo ""
    echo "❌ Training cancelled."
    echo "   You can run this anytime with: bash start_training.sh"
    echo ""
fi
