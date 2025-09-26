#!/usr/bin/env python3
"""
Script de vérification de la configuration du projet MOE Dashboard
Vérifie que tous les fichiers requis sont présents à la racine
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {filepath}")
        return True
    else:
        status = "❌" if required else "⚠️ "
        print(f"{status} {filepath} {'(requis)' if required else '(optionnel)'}")
        return not required

def check_directory_structure():
    """Vérifie la structure des répertoires"""
    required_files = [
        "app.py",
        "requirements.txt",
        "insta_data.csv",
        "data_registration_moe.csv",
        "README.md",
        ".gitignore"
    ]
    
    optional_files = [
        "logo_moe.png",
        "DEPLOYMENT.md",
        ".streamlit/config.toml",
        ".streamlit/secrets.toml"
    ]
    
    print("🔍 Vérification de la structure du projet MOE Dashboard\n")
    
    print("📋 Fichiers requis :")
    all_required_present = True
    for file in required_files:
        if not check_file_exists(file, required=True):
            all_required_present = False
    
    print("\n📋 Fichiers optionnels :")
    for file in optional_files:
        check_file_exists(file, required=False)
    
    print("\n📁 Structure des répertoires :")
    if os.path.exists(".streamlit"):
        print("✅ .streamlit/")
    else:
        print("❌ .streamlit/ (requis pour la configuration)")
        all_required_present = False
    
    print("\n" + "="*50)
    if all_required_present:
        print("🎉 Configuration complète ! Prêt pour le déploiement.")
        return True
    else:
        print("⚠️  Certains fichiers requis sont manquants.")
        return False

def check_csv_format():
    """Vérifie le format basique des fichiers CSV"""
    print("\n🔍 Vérification du format des données :")
    
    try:
        import pandas as pd
        
        # Vérification fichier Instagram
        if os.path.exists("insta_data.csv"):
            df_insta = pd.read_csv("insta_data.csv", sep=';', nrows=1)
            expected_cols = ['Date', 'Type', 'Vues', 'Likes']
            if all(col in df_insta.columns for col in expected_cols):
                print("✅ insta_data.csv - Format correct")
            else:
                print("⚠️  insta_data.csv - Vérifier les colonnes")
        
        # Vérification fichier inscriptions
        if os.path.exists("data_registration_moe.csv"):
            df_reg = pd.read_csv("data_registration_moe.csv", sep=';', nrows=1)
            expected_cols = ['DATE INSCRIPTION', 'PARCOURS', 'PAIEMENT']
            if all(col in df_reg.columns for col in expected_cols):
                print("✅ data_registration_moe.csv - Format correct")
            else:
                print("⚠️  data_registration_moe.csv - Vérifier les colonnes")
                
    except ImportError:
        print("⚠️  pandas non installé - impossible de vérifier le format CSV")
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification CSV : {e}")

if __name__ == "__main__":
    success = check_directory_structure()
    check_csv_format()
    
    if success:
        print("\n🚀 Commandes pour déployer :")
        print("git init")
        print("git add .")
        print("git commit -m 'Initial commit: MOE Dashboard'")
        print("git remote add origin [URL_REPO]")
        print("git push -u origin main")
        sys.exit(0)
    else:
        print("\n❌ Corrigez les erreurs avant de déployer.")
        sys.exit(1)
