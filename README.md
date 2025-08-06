# 🧠 Veil## 🚀 Déploiement

### 🌐 Streamlit Community Cloud
Ce projet est conçu## 🔐 Configura## 🧩 Fonctionnalités

### 📺 Y## ☁️ Déploiement sur Streamlit Cloud

1. **Poussez votre projet sur GitHub**
2. **Connectez-vous sur [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Connectez votre compte GitHub**
4. **Sélectionnez le dépôt** contenant `app.py`
5. **Configurez les variables d'environnement** (optionnel)
   - Ajoutez `YOUTUBE_API_KEY` si vous utilisez l'API YouTube
6. **Cliquez sur Deploy** et profitez de votre dashboard interactif !

## 📃 Licence

Ce projet est libre et open-source sous licence MIT. Vous pouvez l'utiliser et le modifier librement dans un cadre personnel, académique ou professionnel.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une nouvelle fonctionnalité
- Soumettre une pull requestt/suppression de chaînes YouTube
- Récupération automatique des vidéos récentes via flux RSS
- Interface intuitive pour gérer vos sources

### 📰 Medium Scraper
- Sélection de tags thématiques (IA, Machine Learning, NLP, etc.)
- Scraping automatique des derniers articles publiés
- Filtrage intelligent par mots-clés

### 📚 Feedly manuel
- Saisie libre d'articles collectés via veille manuelle
- Support pour Feedly, newsletters et autres sources

### 📤 Export des données
- Téléchargement de l'ensemble des données collectées au format CSV
- Historique complet de votre veille technologiquenel)

Pour activer les fonctionnalités avancées de l'API YouTube, créez un fichier `.env` à la racine du projet :

```env
YOUTUBE_API_KEY=votre_clé_api_youtube
```

**Note :** L'application fonctionne sans clé API en utilisant les flux RSS publics.tre déployé facilement sur Streamlit Community Cloud.

| Plateforme | Docker nécessaire ? | Notes |
|------------|-------------------|-------|
| Streamlit Community Cloud | ❌ Non | Déploie directement à partir d'un repo GitHub contenant `app.py` et `requirements.txt` |

## 📁 Structure du projet

Assurez-vous d'avoir ces fichiers à la racine de votre dépôt :

- `app.py` : application principale Streamlit
- `requirements.txt` : liste des dépendances Python
- `youtube_channels.json` : configuration des chaînes YouTube
- `.gitignore` : fichiers à ignorer par Git
- `.streamlit/config.toml` (optionnel) : configuration de l'interfaceau de bord Streamlit

Ce projet est un tableau de bord interactif développé avec Streamlit pour effectuer une veille technologique sur l'intelligence artificielle (IA). Il collecte des informations à partir de plusieurs sources :

- 📺 **Chaînes YouTube** via flux RSS
- 📰 **Articles Medium** via scraping
- 📚 **Articles manuels** saisis depuis Feedly
- 📤 **Export des données** collectées en fichier CSV

🚀 Déploiement
🌐 Plateforme : Streamlit Community Cloud
Plateforme	Docker nécessaire ?	Notes
Streamlit Community Cloud	❌ Non	Déploie directement à partir d’un repo GitHub contenant app.py et requirements.txt

📁 Structure minimale du projet
Assurez-vous d’avoir ces fichiers à la racine de votre dépôt :

app.py : application principale

requirements.txt : liste des dépendances Python

.streamlit/config.toml (optionnel) : configuration de l’interface (thème, port…)

## ✅ Installation et lancement local

### 1. Cloner le projet
```bash
git clone https://github.com/AFlo59/VeilleStreamlite.git
cd VeilleStreamlite
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate          # Linux/macOS
# ou
.\venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`
## 🛠️ Dépendances

Les principales bibliothèques utilisées :

- `streamlit` : Framework pour l'interface web
- `feedparser` : Analyse des flux RSS YouTube
- `requests` : Requêtes HTTP
- `beautifulsoup4` : Scraping des articles Medium
- `pandas` : Manipulation des données
- `python-dotenv` : Gestion des variables d'environnement

Voir le fichier `requirements.txt` pour les versions exactes.

🔐 Variables d’environnement (optionnel)
Pour activer les fonctionnalités liées à l’API YouTube, ajoute un fichier .env à la racine du projet :

ini
Copier
Modifier
YOUTUBE_API_KEY=ta_clé_API_YOUTUBE
🧩 Fonctionnalités principales
YouTube RSS
→ Ajout/suppression de chaînes, récupération des vidéos récentes via flux RSS.

Medium Scraper
→ Sélection de tags, scraping des derniers articles publiés sur Medium, filtrage par mots-clés.

Feedly manuel
→ Saisie libre d’articles collectés via veille manuelle (ex. Feedly, newsletter, etc.).

Export des logs
→ Téléchargement de l’ensemble des données collectées au format CSV.

🖼️ Exemple d’interface

☁️ Déploiement sur Streamlit Cloud
Pousse ton projet sur GitHub.

Va sur https://streamlit.io/cloud et connecte ton compte GitHub.

Sélectionne le dépôt contenant app.py.

(Optionnel) Ajoute une clé .env dans l'interface si tu utilises l'API YouTube.

Clique sur Deploy et profite de ton dashboard interactif.

📃 Licence
Ce projet est libre et open-source. Tu peux l’utiliser et le modifier librement dans un cadre personnel, académique ou professionnel.

Souhaites-tu que je t’ajoute le fichier requirements.txt ou config.toml également ?