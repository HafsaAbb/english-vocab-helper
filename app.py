import streamlit as st
import requests

# Fonction pour récupérer les mots avec définition
def fetch_datamuse(word, relation, max_results=20, pos_filter=None):
    url = f"https://api.datamuse.com/words?{relation}={word}&max={max_results}&md=pd"
    resp = requests.get(url)
    results = []
    if resp.status_code == 200:
        data = resp.json()
        for item in data:
            w = item['word']
            definition = item.get('defs', [''])[0] if 'defs' in item else ''
            if definition:
                definition = definition.split('\t')[-1]
            # Filtrer par partie du discours si demandé
            if pos_filter:
                tags = item.get('tags', [])
                if pos_filter in tags:
                    results.append((w, definition))
            else:
                results.append((w, definition))
    return results

# ----------------- Interface Streamlit -----------------
st.set_page_config(page_title="English Vocabulary Helper", page_icon="📚", layout="wide")
st.title("📚 English Vocabulary Helper – Styled Cards")
st.write("Type a word to get **synonyms and antonyms** with definitions in colorful styled cards!")

# Entrée du mot
word = st.text_input("Enter an English word:")

# Slider pour nombre de résultats
max_results = st.slider("Number of results", min_value=5, max_value=50, value=10)

# Filtre type de mot
pos_option = st.selectbox("Filter by part of speech (optional)", 
                          ["All", "Adjective", "Verb", "Noun", "Adverb"])
pos_map = {"Adjective":"adj", "Verb":"v", "Noun":"n", "Adverb":"r"}
pos_filter = pos_map.get(pos_option, None) if pos_option != "All" else None

# Fonction pour créer une carte stylée
def display_card(word, definition, color):
    st.markdown(f"""
    <div style="
        background-color: {color};
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        text-align: center;
        box-shadow: 2px 2px 5px #aaaaaa;">
        <strong>{word}</strong><br>
        <em>{definition}</em>
    </div>
    """, unsafe_allow_html=True)

if word:
    synonyms = fetch_datamuse(word, 'rel_syn', max_results, pos_filter)
    antonyms = fetch_datamuse(word, 'rel_ant', max_results, pos_filter)

    # Affichage des synonymes
    if synonyms:
        st.subheader("Synonyms 🟢")
        cols = st.columns(min(len(synonyms), 5))
        for i, (w, definition) in enumerate(synonyms):
            with cols[i % len(cols)]:
                display_card(w, definition, "#d4edda")  # vert clair
    else:
        st.write("No synonyms found 😕")

    # Affichage des antonymes
    if antonyms:
        st.subheader("Antonyms 🔴")
        cols = st.columns(min(len(antonyms), 5))
        for i, (w, definition) in enumerate(antonyms):
            with cols[i % len(cols)]:
                display_card(w, definition, "#f8d7da")  # rouge clair
    else:
        st.write("No antonyms found 😕")

st.markdown("---")
st.info("💡 Tip: Use the slider to choose the number of results and the dropdown to filter by part of speech!")
