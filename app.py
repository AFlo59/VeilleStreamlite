import streamlit as st
import feedparser
import json
import os

# ---------- Fonctions Utilitaires ----------

CHANNEL_FILE = "youtube_channels.json"

def load_channels():
    if os.path.exists(CHANNEL_FILE):
        with open(CHANNEL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_channels(channels):
    with open(CHANNEL_FILE, "w") as f:
        json.dump(channels, f, indent=4)

# ---------- Interface Streamlit ----------

st.set_page_config(page_title="Veille IA YouTube", layout="wide")
st.title("📺 Veille YouTube – Flux RSS IA")

channels = load_channels()

# --- Section : Ajouter une nouvelle chaîne ---
with st.expander("➕ Ajouter une chaîne YouTube"):
    name = st.text_input("Nom de la chaîne")
    channel_id = st.text_input("Channel ID (YouTube)")

    if st.button("Ajouter"):
        if name and channel_id:
            channels[name] = channel_id
            save_channels(channels)
            st.success(f"Chaîne '{name}' ajoutée !")
            st.experimental_rerun()
        else:
            st.warning("Merci de renseigner un nom et un Channel ID.")

# --- Section : Supprimer une chaîne existante ---
with st.expander("➖ Supprimer une chaîne YouTube"):
    if channels:
        to_delete = st.selectbox("Sélectionner une chaîne à supprimer :", list(channels.keys()))
        if st.button("Supprimer"):
            del channels[to_delete]
            save_channels(channels)
            st.success(f"Chaîne '{to_delete}' supprimée.")
            st.experimental_rerun()
    else:
        st.info("Aucune chaîne enregistrée.")

# --- Section : Affichage des vidéos ---
st.subheader("🎬 Dernières vidéos disponibles")

if not channels:
    st.warning("Aucune chaîne enregistrée. Ajoutez-en ci-dessus.")
else:
    selected = st.selectbox("Choisir une chaîne :", list(channels.keys()))
    channel_id = channels[selected]
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(rss_url)

    for entry in feed.entries[:5]:
        st.markdown(f"### [{entry.title}]({entry.link})")
        st.write(f"🕒 {entry.published}")
        st.write("---")
