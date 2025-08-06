import streamlit as st
import feedparser
import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ---------- Config Streamlit ----------
st.set_page_config(page_title="Veille IA", layout="wide")
st.title("🧠 Tableau de bord de veille IA")

# ---------- Fichier local pour les chaînes YouTube ----------
CHANNEL_FILE = "youtube_channels.json"

def load_channels():
    if os.path.exists(CHANNEL_FILE):
        with open(CHANNEL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_channels(channels):
    with open(CHANNEL_FILE, "w") as f:
        json.dump(channels, f, indent=4)

# ---------- Fonction pour scraper Medium ----------
def scrape_medium_articles(tag_url, keywords=None):
    """
    Scrape les titres d'articles Medium depuis une URL de tag.
    Filtre selon une liste de mots-clés (insensibles à la casse).
    """
    try:
        page = requests.get(tag_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(page.content, "html.parser")
        articles = soup.find_all("h2")

        filtered_articles = []

        for a in articles:
            title = a.get_text(strip=True)
            if not title:
                continue
            if keywords:
                if any(kw.lower() in title.lower() for kw in keywords):
                    filtered_articles.append(title)
            else:
                filtered_articles.append(title)

        return filtered_articles

    except Exception as e:
        return [f"Erreur : {e}"]


# ---------- Tabs principaux ----------
tabs = st.tabs(["📺 YouTube RSS", "📰 Medium Articles", "📚 Feedly (manuel)", "📤 Export Logs"])

# =========================================
# 🟢 ONGLET 1 — YOUTUBE RSS
# =========================================
with tabs[0]:
    st.header("📺 Veille YouTube – Flux RSS")

    channels = load_channels()

    # Ajouter une chaîne
    with st.expander("➕ Ajouter une chaîne YouTube"):
        name = st.text_input("Nom de la chaîne")
        channel_id = st.text_input("Channel ID (YouTube)")
        if st.button("Ajouter"):
            if name and channel_id:
                channels[name] = channel_id
                save_channels(channels)
                st.success(f"Chaîne '{name}' ajoutée !")
                st.rerun()


    # Supprimer une chaîne
    with st.expander("➖ Supprimer une chaîne"):
        if channels:
            to_delete = st.selectbox("Sélectionner une chaîne :", list(channels.keys()))
            if st.button("Supprimer"):
                del channels[to_delete]
                save_channels(channels)
                st.success(f"Chaîne '{to_delete}' supprimée.")
                st.rerun()

        else:
            st.info("Aucune chaîne enregistrée.")

    # Affichage des vidéos
    if channels:
        selected = st.selectbox("Voir les vidéos de :", list(channels.keys()))
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channels[selected]}"
        feed = feedparser.parse(rss_url)
        logs = []
        for entry in feed.entries[:5]:
            st.markdown(f"### [{entry.title}]({entry.link})")
            st.write(f"🕒 {entry.published}")
            logs.append({
                "source": selected,
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })
        st.session_state['yt_logs'] = logs

# =========================================
# 🔵 ONGLET 2 — MEDIUM
# =========================================
with tabs[1]:
    st.header("📰 Veille Medium – Articles filtrés IA")

    # Liste de mots-clés IA
    default_keywords = ["NLP", "LLM", "language model", "transformer", "GPT", "chatbot", "token"]

    # Lien Medium à scraper
    url = st.text_input("Lien Medium à scraper :", 
                        "https://medium.com/tag/large-language-models")

    # Personnalisation des mots-clés
    keywords_input = st.text_input("Mots-clés à filtrer (séparés par des virgules)", 
                                   ", ".join(default_keywords))
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

    if st.button("Scraper les articles Medium"):
        articles = scrape_medium_articles(url, keywords)
        logs = []
        if articles:
            st.success(f"{len(articles)} article(s) trouvé(s) contenant les mots-clés.")
            for a in articles:
                st.markdown(f"### {a}")
                logs.append({"source": "Medium", "title": a, "link": url})
            st.session_state['medium_logs'] = logs
        else:
            st.warning("Aucun article trouvé avec les mots-clés spécifiés.")


# =========================================
# 🟣 ONGLET 3 — FEEDLY MANUEL
# =========================================
with tabs[2]:
    st.header("📚 Veille Feedly – Saisie manuelle")
    st.info("Ajoute ici les titres d’articles que tu as trouvés via Feedly :")
    feedly_logs = st.text_area("Articles pertinents (titre par ligne)", height=200)

    if feedly_logs:
        st.session_state['feedly_logs'] = [
            {"source": "Feedly", "title": line.strip()}
            for line in feedly_logs.split("\n") if line.strip()
        ]

# =========================================
# 🟡 ONGLET 4 — EXPORT LOGS
# =========================================
with tabs[3]:
    st.header("📤 Export des logs de veille")

    # Fusion de tous les logs
    all_logs = (
        st.session_state.get('yt_logs', []) +
        st.session_state.get('medium_logs', []) +
        st.session_state.get('feedly_logs', [])
    )

    if all_logs:
        df = pd.DataFrame(all_logs)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger les logs en CSV", csv, "veille_ia.csv", "text/csv")
    else:
        st.warning("Aucune donnée à exporter.")
