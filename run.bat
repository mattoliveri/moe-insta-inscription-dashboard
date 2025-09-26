@echo off
REM Script de lancement MOE Dashboard pour Windows
REM Usage: run.bat

echo.
echo 🏃 Lancement du Dashboard MOE...
echo 📊 Inscriptions × Instagram Analytics
echo.

REM Vérification que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérification que pip est installé
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip n'est pas installé
    pause
    exit /b 1
)

REM Installation des dépendances
echo 📦 Vérification des dépendances...
pip install -r requirements.txt

REM Vérification que les fichiers de données sont présents
if not exist "insta_data.csv" (
    echo ❌ Fichier insta_data.csv manquant
    pause
    exit /b 1
)

if not exist "data_registration_moe.csv" (
    echo ❌ Fichier data_registration_moe.csv manquant
    pause
    exit /b 1
)

echo.
echo ✅ Configuration OK
echo 🚀 Lancement de l'application...
echo.
echo 📱 L'application sera accessible sur:
echo    Local:    http://localhost:8501
echo    Network:  http://[votre-ip]:8501
echo.
echo 🔐 Identifiants par défaut:
echo    Utilisateur: admin
echo    Mot de passe: AdminMOE13
echo.
echo ⏹️  Pour arrêter: Ctrl+C
echo.

REM Lancement de Streamlit
streamlit run app.py

pause
