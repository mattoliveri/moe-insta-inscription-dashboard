# 🚀 Guide de déploiement

## 📋 Checklist avant déploiement

### ✅ Fichiers essentiels présents à la racine :
- [ ] `app.py` - Application principale
- [ ] `requirements.txt` - Dépendances Python
- [ ] `insta_data.csv` - Données Instagram
- [ ] `data_registration_moe.csv` - Données inscriptions
- [ ] `logo_moe.png` - Logo MOE (optionnel)
- [ ] `README.md` - Documentation
- [ ] `DEPLOYMENT.md` - Guide de déploiement
- [ ] `.gitignore` - Fichiers à ignorer
- [ ] `.streamlit/config.toml` - Configuration thème
- [ ] `.streamlit/secrets.toml` - Secrets (local seulement)

### ✅ Configuration :
- [ ] Thème configuré en mode clair
- [ ] Authentification sécurisée
- [ ] Gestion des secrets pour Streamlit Cloud

## 🐙 Déploiement sur GitHub

### 1. Initialiser le repository Git
```bash
cd "Streamlit Insta+Registration MOE"
git init
git add .
git commit -m "Initial commit: MOE Dashboard with authentication"
```

### 2. Créer le repository sur GitHub
1. Aller sur [github.com](https://github.com)
2. Cliquer sur "New repository"
3. Nom suggéré : `moe-dashboard-streamlit`
4. Description : "Dashboard d'analyse MOE - Inscriptions × Instagram"
5. Repository public ou privé selon vos besoins
6. Ne pas initialiser avec README (déjà présent)

### 3. Connecter et pousser
```bash
git remote add origin https://github.com/[USERNAME]/moe-dashboard-streamlit.git
git branch -M main
git push -u origin main
```

## ☁️ Déploiement sur Streamlit Cloud

### 1. Accès à Streamlit Cloud
- Aller sur [share.streamlit.io](https://share.streamlit.io)
- Se connecter avec GitHub

### 2. Déployer l'application
1. Cliquer sur "New app"
2. Repository : Sélectionner votre repository GitHub
3. Branch : `main`
4. Main file path : `app.py`
5. Advanced settings (optionnel) :
   - Python version : 3.9 ou 3.10
   - Secrets : Ajouter les secrets si nécessaire

### 3. Configuration des secrets (si nécessaire)
Dans l'interface Streamlit Cloud, section "Secrets" :
```toml
[auth]
username = "admin"
password = "AdminMOE13"
```

### 4. Lancement
- Cliquer sur "Deploy!"
- Attendre le déploiement (2-5 minutes)
- L'application sera accessible via l'URL fournie

## 🔧 Configuration post-déploiement

### URLs d'accès :
- **URL publique** : `https://[app-name]-[random-id].streamlit.app`
- **URL personnalisée** : Configurable dans les paramètres

### Gestion des données :
- Les fichiers CSV sont déployés avec l'application
- Pour mettre à jour les données : commit + push sur GitHub
- Streamlit Cloud redéploiera automatiquement

### Monitoring :
- Logs accessibles via l'interface Streamlit Cloud
- Métriques d'usage disponibles
- Notifications par email en cas d'erreur

## 🛠️ Maintenance

### Mise à jour des données :
1. Remplacer les fichiers CSV localement
2. Commit et push sur GitHub
3. Redéploiement automatique

### Mise à jour du code :
1. Modifier le code localement
2. Tester avec `streamlit run app.py`
3. Commit et push
4. Vérifier le déploiement

### Gestion des versions :
- Utiliser des tags Git pour les versions stables
- Branches de développement pour les nouvelles fonctionnalités

## ⚠️ Points d'attention

### Sécurité :
- Le fichier `.streamlit/secrets.toml` n'est PAS commité (dans .gitignore)
- Les secrets sont configurés directement sur Streamlit Cloud
- Les données personnelles sont masquées dans l'interface

### Performance :
- Cache Streamlit activé pour les gros datasets
- Optimisation des graphiques Plotly
- Limitation des requêtes simultanées par l'authentification

### Limites Streamlit Cloud :
- **CPU** : Limité pour les applications gratuites
- **Mémoire** : 1GB max pour les comptes gratuits
- **Stockage** : Limité aux fichiers du repository
- **Bande passante** : Limites selon le plan

## 📞 Support

### En cas de problème :
1. Vérifier les logs sur Streamlit Cloud
2. Tester l'application localement
3. Vérifier la conformité des fichiers CSV
4. Consulter la documentation Streamlit

### Ressources utiles :
- [Documentation Streamlit](https://docs.streamlit.io)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Forum Streamlit](https://discuss.streamlit.io)

---

**Prêt pour le déploiement !** 🎉
