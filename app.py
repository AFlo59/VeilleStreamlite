import streamlit as st
import feedparser
import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import os
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "INSÈRE_TA_CLÉ_ICI_TEMPORAIREMENT")



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
def scrape_medium_articles(tag_url):
    """
    Scrape les titres + liens d'articles Medium depuis une URL de tag.
    """
    try:
        page = requests.get(tag_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(page.content, "html.parser")

        articles = []
        for h2 in soup.find_all("h2"):
            title = h2.get_text(strip=True)
            link_tag = h2.find_parent("a")
            if not title or not link_tag:
                continue
            link = link_tag["href"].split("?")[0]
            if not link.startswith("http"):
                link = "https://medium.com" + link
            articles.append((title, link))

        return articles
    except Exception as e:
        return [("Erreur", str(e))]



def get_channel_id_from_url(url):
    import re
    try:
        if "/channel/" in url:
            return url.split("/channel/")[1].split("/")[0]
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None
        text = res.text
        # Tentative extraction via channelId
        match = re.search(r'"channelId"\s*:\s*"([^"]+)"', text)
        if match:
            return match.group(1)
        # Tentative extraction via browseId
        match2 = re.search(r'"browseId"\s*:\s*"([^"]+)"', text)
        if match2:
            return match2.group(1)
        return None
    except Exception:
        return None

def get_channel_id_from_api(query):
    """
    Recherche l'ID d'une chaîne YouTube via le nom ou handle en utilisant l'API YouTube.
    """
    api_key = os.getenv("YOUTUBE_API_KEY", "INSÈRE_TA_CLÉ_ICI_TEMPORAIREMENT")
    if not api_key:
        return None

    search_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=channel&q={query}&key={api_key}"
    )
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            return data["items"][0]["snippet"]["channelId"]
    return None


# ---------- Tabs principaux ----------
tabs = st.tabs(["📺 YouTube RSS", "📰 Medium Articles", "📚 Feedly (manuel)", "📤 Export Logs"])

# =========================================
# 🟢 ONGLET 1 — YOUTUBE RSS
# =========================================
with tabs[0]:
    st.header("📺 Veille YouTube – Flux RSS")

    channels = load_channels()

    with st.expander("➕ Ajouter une chaîne YouTube"):
        name = st.text_input("Nom de la chaîne")
        channel_url = st.text_input("URL de la chaîne YouTube (ex: https://www.youtube.com/@AllAboutAI)")

        if st.button("Ajouter"):
            if name and channel_url:
                # Essaye d'abord d'extraire via scraping
                channel_id = get_channel_id_from_url(channel_url)
                # Sinon, fallback via API
                if not channel_id:
                    query = channel_url.strip().split("/")[-1].replace("@", "")
                    channel_id = get_channel_id_from_api(query)

                if channel_id:
                    channels[name] = channel_id
                    save_channels(channels)
                    st.success(f"Chaîne '{name}' ajoutée avec ID : {channel_id}")
                    st.rerun()
                else:
                    st.error("Impossible de récupérer l'ID de la chaîne. Vérifie l'URL ou le nom.")
            else:
                st.warning("Merci de renseigner un nom et une URL valide.")



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
    st.write("Choisis une ou plusieurs sources Medium à scraper :")

    medium_urls = {
        "AI": "https://medium.com/tag/ai",
        "Machine Learning": "https://medium.com/tag/machine-learning",
        "Large Language Models": "https://medium.com/tag/large-language-models",
        "NLP": "https://medium.com/tag/nlp",
        "Deep Learning": "https://medium.com/tag/deep-learning",
        "Generative AI": "https://medium.com/tag/generative-ai"
    }

    default_tags = ["AI", "Large Language Models"]
    selected_tags = st.multiselect(
    "Tags Medium à surveiller :",
    options=list(medium_urls.keys()),
    default=[tag for tag in default_tags if tag in medium_urls]
    )

    if st.button("Scraper les articles Medium"):
        logs = []
        for tag in selected_tags:
            url = medium_urls[tag]
            articles = scrape_medium_articles(url)  # Aucun filtrage
            for title, link in articles:
                st.markdown(f"### [{title}]({link})")
                logs.append({"source": f"Medium - {tag}", "title": title, "link": link})
        if logs:
            st.success(f"{len(logs)} article(s) collecté(s) depuis Medium.")
            st.session_state['medium_logs'] = logs
        else:
            st.warning("Aucun article récupéré.")



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
