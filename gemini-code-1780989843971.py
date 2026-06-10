import streamlit as st
import json
import os

FICHIER_MEMOIRE = "memoire_collective.json"

def charger_memoire():
    """Charge les mots appris depuis le fichier JSON."""
    if os.path.exists(FICHIER_MEMOIRE):
        try:
            with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def sauvegarder_memoire(memoire_a_sauver):
    """Sauvegarde les mots appris dans le fichier JSON."""
    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
        json.dump(memoire_a_sauver, f, ensure_ascii=False, indent=4)


memoire = charger_memoire()

if "mot_en_attente" not in st.session_state:
    st.session_state.mot_en_attente = None

st.title("The Royal Bot (the new)")
st.write("This is a french chatbot. Apprenez lui ce que vous voulez !")

with st.sidebar:
    st.header("⚖️ Conditions d'Utilisation")
    st.markdown("""
    En participant à l'évolution de ce chatbot, vous acceptez les règles suivantes :
    * **Respect et bienveillance :** Ne lui apprenez pas d'insultes ni de propos inappropriés.
    * **Données publiques :** Tout ce que vous lui expliquez est stocké et devient visible par les autres internautes. Ne partagez aucune info privée (nom, mots de passe, etc.).
    * **Modération :** L'administrateur se réserve le droit de vider la mémoire en cas d'abus.
    """)
    
    st.write("---")
    
    if st.button("🧠 Afficher les mots connus"):
        st.subheader("Mots dans ma base de données :")
        if memoire:
            for m, d in memoire.items():
                st.write(f"• **{m}** : {d}")
        else:
            st.write("Le bot ne connaît encore aucun mot.")

    st.write("---")
    
    st.subheader("🛠️ Zone Administrateur")
    mot_de_passe = st.text_input("Entrez le mot de passe admin :", type="password")
    
    if mot_de_passe == "prk°~°":
        st.success("Accès Admin Autorisé")
        if st.button("💢reinitilation memorie's"):
            memoire = {}
            sauvegarder_memoire(memoire)
            st.session_state.mot_en_attente = None
            st.error("Mémoire entièrement vidée !")
            st.rerun()

message_user = st.text_input("Écrivez votre message ici :", key="input_user")

if message_user:
    message = message_user.lower().strip()
    reponse = ""

    if st.session_state.mot_en_attente:
        mot_appris = st.session_state.mot_en_attente
        memoire[mot_appris] = message_user  # On garde les majuscules de l'utilisateur pour la définition
        sauvegarder_memoire(memoire)
        reponse = f"Thank you ! J'ai enregistré : **{mot_appris}**. Du coup ca veur dire *'{message_user}'* pour tout le monde."
        st.session_state.mot_en_attente = None  # Réinitialisation de l'attente

    else:
        mots = message.split()
        trouve = False
        for mot in mots:
            # Nettoyage rapide de la ponctuation autour du mot
            mot_nettoye = mot.strip(",.?!()\"'")
            if mot_nettoye in memoire:
                reponse = f"Abrege je connais déjà **{mot_nettoye}** ! Tout le monde connais la deffinission : *{memoire[mot_nettoye]}*"
                trouve = True
                break
        
        if not trouve:
            mots_interessants = [m.strip(",.?!()\"'") for m in mots if len(m.strip(",.?!()\"'")) > 3]
            if mots_interessants:
                ce_mot = mots_interessants[0]
                st.session_state.mot_en_attente = ce_mot
                reponse = f"Je ne connais pas le mot **{ce_mot}**. Pouvez-vous m'expliquer ce que c'est ?"
            else:
                reponse = "Fais des vraix phrases sans abreger!"

    st.info(reponse)
