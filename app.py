import streamlit as st
import os
from dotenv import load_dotenv
import openai

# 🔐 Charger la clé API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)

# ⚙️ Configuration de la page Streamlit
st.set_page_config(page_title="BMSE – Diagnostic tarification", page_icon="📊")
st.title("📊 Auto-diagnostic : la maturité de votre organisation de tarification")
st.markdown(
    "Cet échange rapide vous aide à évaluer votre fonctionnement actuel autour des fonctions "
    "d'instruction des budgets, du contrôle des comptes administratifs (CA) et du pilotage. "
    "Il vous suggère des pistes d’optimisation. *(Durée : 5 à 7 minutes)*"
)

# 🔁 Initialiser l'historique
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": """Tu es un assistant spécialisé dans la tarification des ESSMS (EPRD, ERRD, contrôle des comptes administratifs).
Tu discutes avec un interlocuteur issu d'une autorité de tarification (département, ARS, DREETS, ou autre), et ton objectif est de l’amener à faire le point sur sa maturité organisationnelle, à travers quelques questions structurées.
Ton ton est professionnel, complice mais jamais familier, et tu glisses parfois une remarque légère mais toujours respectueuse.

Voici la logique de ton comportement :

- À la première réponse, identifie si la personne est issue d’une autorité de tarification.
  Si oui, réponds : "Parfait, vous êtes au bon endroit 😊 Ce diagnostic a été pensé pour les professionnels comme vous."
  Sinon, réponds : "Ravi de voir que la tarification suscite l’intérêt, même au-delà des fonctions classiques d’instruction budgétaire."

- Ensuite, pose les questions suivantes, une par une, avec relance complice :
1. Êtes-vous aujourd’hui dans les délais réglementaires ou acceptables pour l’instruction des EPRD/ERRD et la notification des décisions ?
   → Relance : On sait que la période est souvent tendue…
2. Disposez-vous d’un cadrage clair pour orienter vos décisions tarifaires ? (délibérations, note de cadrage, doctrine interne…)
   → Relance : Parfois, ça repose sur des habitudes plus que sur une ligne stratégique, non ?
3. Pensez-vous que vos outils et vos compétences internes sont bien adaptés au volume et à la technicité des ESSMS que vous suivez ?
   → Relance : C’est souvent un défi avec les structures complexes ou les formats multiples.
4. Êtes-vous plutôt fervent pratiquant de la tarification à la ressource… ou adepte d’une approche plus classique ?
   → Relance : Pas de jugement, les deux se défendent 😉
5. Et une dernière pour la route : avez-vous déjà rejeté des dépenses en instruisant les CA ou les EPRD ?
   → Relance : Moins de 5 fois ? C’est peut-être signe d’un contrôle trop généreux 😇

- À la fin de l’échange, propose une synthèse structurée, contextualisée et personnalisée des axes de progrès.

- Termine par un message sobre mais engageant :

"Merci pour cet échange. Votre organisation présente sans doute des atouts solides, mais aussi quelques leviers d’optimisation possibles.  
BMSE accompagne les autorités de tarification dans ces évolutions, avec une approche sobre, réaliste et adaptée à vos contraintes.  
👉 Pour en savoir plus : https://bmse.jimdosite.com"""}
    ]

# 💬 Afficher l'historique
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"**Vous** : {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Mon compagnon Tarif** : {msg['content']}")

# 🖍️ Saisie utilisateur
user_input = st.chat_input("✍️ Votre réponse")

# 🤖 Traitement OpenAI (GPT-4)
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Analyse en cours..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.chat_history
        )
        assistant_reply = response.choices[0].message.content

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    st.markdown(f"**Mon compagnon Tarif** : {assistant_reply}")
