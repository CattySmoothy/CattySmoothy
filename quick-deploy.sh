#!/bin/bash

# Quick deployment script for local use
# This script helps push changes to GitHub and trigger deployment

echo "🎨 Raichuu Website Quick Deploy"
echo "================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the CattySmoothy directory"
    exit 1
fi

# Check git status
echo "📋 Checking for changes..."
git status --porcelain

if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No changes to commit"
    exit 0
fi

# Add all changes
echo "📝 Adding all changes..."
git add .

# Commit with timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "💾 Committing changes..."
git commit -m "Update website - $TIMESTAMP"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Changes pushed successfully!"
echo "🌐 Your website will update automatically at https://eclipsogate.org/"
echo "⏱️  It may take 1-2 minutes for changes to appear"
echo ""
echo "💡 Tip: You can also use VS Code's Source Control panel for this!"
