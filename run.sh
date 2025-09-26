#!/bin/bash

# Script de lancement MOE Dashboard pour Unix/Linux/Mac
# Usage: ./run.sh

echo "🏃 Lancement du Dashboard MOE..."
echo "📊 Inscriptions × Instagram Analytics"
echo ""

# Vérification que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérification que pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Installation des dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip3 install -r requirements.txt

# Vérification que les fichiers de données sont présents
if [ ! -f "insta_data.csv" ]; then
    echo "❌ Fichier insta_data.csv manquant"
    exit 1
fi

if [ ! -f "data_registration_moe.csv" ]; then
    echo "❌ Fichier data_registration_moe.csv manquant"
    exit 1
fi

echo ""
echo "✅ Configuration OK"
echo "🚀 Lancement de l'application..."
echo ""
echo "📱 L'application sera accessible sur:"
echo "   Local:    http://localhost:8501"
echo "   Network:  http://[votre-ip]:8501"
echo ""
echo "🔐 Identifiants par défaut:"
echo "   Utilisateur: admin"
echo "   Mot de passe: AdminMOE13"
echo ""
echo "⏹️  Pour arrêter: Ctrl+C"
echo ""

# Lancement de Streamlit
streamlit run app.py
