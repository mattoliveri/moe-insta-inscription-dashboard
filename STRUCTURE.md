# 📁 Structure du projet MOE Dashboard

## 🗂️ Architecture des fichiers

```
Streamlit Insta+Registration MOE/
├── app.py                          # 🚀 Application Streamlit principale
├── requirements.txt                # 📦 Dépendances Python
├── insta_data.csv                  # 📊 Données posts Instagram
├── data_registration_moe.csv       # 📋 Données inscriptions MOE
├── logo_moe.png                    # 🖼️ Logo MOE (optionnel)
├── README.md                       # 📚 Documentation principale
├── DEPLOYMENT.md                   # 🚀 Guide de déploiement
├── STRUCTURE.md                    # 📁 Ce fichier - Structure du projet
├── check_setup.py                  # ✅ Script de vérification
├── .gitignore                      # 🚫 Fichiers à ignorer par Git
└── .streamlit/
    ├── config.toml                 # 🎨 Configuration thème clair
    └── secrets.toml               # 🔐 Secrets (non versionné)
```

## 📝 Description des fichiers

### 🎯 **Fichiers principaux**

| Fichier | Description | Requis |
|---------|-------------|---------|
| `app.py` | Application Streamlit avec authentification et dashboard | ✅ |
| `requirements.txt` | Dépendances Python optimisées pour le cloud | ✅ |
| `insta_data.csv` | Données des posts Instagram (Date, Type, Vues, Likes...) | ✅ |
| `data_registration_moe.csv` | Données des inscriptions (Parcours, Paiement...) | ✅ |

### 📄 **Documentation**

| Fichier | Description | Requis |
|---------|-------------|---------|
| `README.md` | Documentation complète du projet | ✅ |
| `DEPLOYMENT.md` | Guide étape par étape pour déployer | 📋 |
| `STRUCTURE.md` | Structure du projet (ce fichier) | 📋 |

### ⚙️ **Configuration**

| Fichier | Description | Requis |
|---------|-------------|---------|
| `.streamlit/config.toml` | Configuration thème clair | ✅ |
| `.streamlit/secrets.toml` | Secrets (login/password) | 🔐 |
| `.gitignore` | Fichiers à exclure de Git | ✅ |

### 🛠️ **Utilitaires**

| Fichier | Description | Requis |
|---------|-------------|---------|
| `check_setup.py` | Script de vérification de la config | 🔧 |
| `logo_moe.png` | Logo MOE | 🖼️ |

## 🔄 **Chemins dans le code**

L'application utilise des chemins relatifs simples :

```python
# Dans app.py
INSTAGRAM_CSV = "insta_data.csv"          # ✅ Racine du projet
REG_CSV = "data_registration_moe.csv"     # ✅ Racine du projet
```

## ✅ **Vérification de la structure**

Exécuter le script de vérification :
```bash
python3 check_setup.py
```

Résultat attendu : `🎉 Configuration complète ! Prêt pour le déploiement.`

## 🚀 **Prêt pour le déploiement**

Avec cette structure :
- ✅ **GitHub** : Tous les fichiers sont prêts pour être versionnés
- ✅ **Streamlit Cloud** : Structure optimisée pour le déploiement
- ✅ **Local** : Fonctionne directement avec `streamlit run app.py`

## 🔐 **Sécurité**

- ✅ Authentification intégrée (`admin` / `AdminMOE13`)
- ✅ Secrets dans `.streamlit/secrets.toml` (exclu de Git)
- ✅ Données personnelles masquées dans l'interface

---

**Structure validée le 26/09/2025** ✅
