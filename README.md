# MOE - Dashboard Inscriptions × Instagram

Dashboard d'analyse des inscriptions MOE avec suivi de l'impact de la communication Instagram.

## 🚀 Fonctionnalités

- **Authentification sécurisée** : Accès protégé par login/mot de passe
- **Analyse des inscriptions** : Suivi détaillé des inscriptions par parcours (5K, 12K, 21K)
- **Impact communication** : Corrélation entre posts Instagram et inscriptions
- **Visualisations interactives** : Graphiques Plotly avec thème clair
- **Export de données** : Téléchargement des analyses en CSV
- **Filtres avancés** : Filtrage par dates, parcours, statuts

## 📊 Onglets disponibles

1. **Overview** : Vue d'ensemble avec KPIs principaux
2. **Inscriptions** : Analyse détaillée des inscriptions
3. **Impact Com × Inscriptions** : Analyse de l'impact des posts Instagram
4. **Charts** : Graphiques personnalisables
5. **Explorer** : Exploration des données brutes

## 🔐 Accès

- **Utilisateur** : `admin`
- **Mot de passe** : `AdminMOE13`

## 📁 Structure du projet

### Fichiers principaux :
- `app.py` : Application Streamlit
- `insta_data.csv` : Données Instagram
- `data_registration_moe.csv` : Données inscriptions
- `requirements.txt` : Dépendances Python
- `run.sh` / `run.bat` : Scripts de lancement

### Format attendu :

#### insta_data.csv
```
Date;Heure;Titre;Lien;Contenue;Type;...;Vues;Likes;Commentaires;Partages
```

#### data_registration_moe.csv
```
DATE INSCRIPTION;PARCOURS;PAIEMENT;FEDERATION;...
```

## 🛠️ Installation locale

### Prérequis
- Python 3.8+
- pip

### Installation et lancement

#### 🖥️ Windows
```cmd
git clone [URL_DU_REPO]
cd streamlit-moe-dashboard
run.bat
```

#### 🐧 Linux/Mac
```bash
git clone [URL_DU_REPO]
cd streamlit-moe-dashboard
./run.sh
```

#### 🔧 Manuel
```bash
pip install -r requirements.txt
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

## ☁️ Déploiement sur Streamlit Cloud

1. Push sur GitHub
2. Connecter sur [share.streamlit.io](https://share.streamlit.io)
3. Sélectionner le repository, fichier principal : `app.py`

## 🎨 Thème

L'application utilise un thème clair par défaut configuré dans `.streamlit/config.toml` :
- Fond : Blanc
- Couleur primaire : Rouge MOE (#FF4B4B)
- Graphiques : Template Plotly blanc

## 📈 Métriques suivies

### Inscriptions
- Total inscriptions par parcours
- Taux de paiement
- Répartition par statuts (licence, handisport)
- Évolution temporelle

### Instagram
- Vues, likes, commentaires, partages
- Impact sur les inscriptions (fenêtres 24h, 48h, 72h)
- Performance par type de post

## 🔧 Configuration

### Variables d'environnement (optionnel)
Créer un fichier `secrets.toml` à la racine pour les configurations sensibles :
```toml
[auth]
username = "admin"
password = "AdminMOE13"
```

## 📝 Notes techniques

- **Cache** : Les données sont mises en cache pour de meilleures performances
- **Sécurité** : Masquage automatique des données personnelles (emails, téléphones)
- **Responsive** : Interface adaptée aux différentes tailles d'écran
- **Export** : Boutons de téléchargement pour toutes les analyses

## 🆘 Support

Pour tout problème ou question :
1. Vérifier que les fichiers CSV sont présents et au bon format
2. Contrôler les logs d'erreur dans la console
3. S'assurer que toutes les dépendances sont installées

---

**MOE Dashboard** - Version 1.0  
Dashboard d'analyse pour le suivi des inscriptions et de l'impact communication Instagram.