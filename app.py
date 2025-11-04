import streamlit as st
from nltk.corpus import wordnet
import nltk

# Téléchargement des données WordNet si nécessaire
nltk.download('wordnet')
nltk.download('omw-1.4')

# Fonction pour obtenir synonymes et antonymes
def get_synonyms_antonyms(word):
    synonyms = set()
    antonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " "))
            if lemma.antonyms():
                antonyms.add(lemma.antonyms()[0].name().replace("_", " "))
    return list(synonyms), list(antonyms)

# -------------------- Interface Streamlit --------------------
st.set_page_config(
    page_title="English Vocabulary Helper",
    page_icon="📚",
    layout="centered"
)

st.title("📚 English Vocabulary Helper")
st.write(
    "Type an English word below to get its **synonyms** and **antonyms**. "
    "A simple tool to improve your vocabulary!"
)

# Champ de saisie
word = st.text_input("Enter an English word:")

if word:
    synonyms, antonyms = get_synonyms_antonyms(word.lower())
    
    if synonyms:
        st.subheader("Synonyms 🟢")
        st.write(", ".join(synonyms))
    else:
        st.write("No synonyms found 😕")

    if antonyms:
        st.subheader("Antonyms 🔴")
        st.write(", ".join(antonyms))
    else:
        st.write("No antonyms found 😕")

# Section conseils
st.markdown("---")
st.write(
    "💡 Tip: You can try adjectives like 'happy', verbs like 'run', or nouns like 'car'."
)
