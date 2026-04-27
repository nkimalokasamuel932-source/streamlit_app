import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. CONFIGURATION DE L'APPLICATION
# ==========================================
st.set_page_config(
    page_title="Loto-Euro Fusion Pro V2.1", 
    page_icon="🧬", 
    layout="wide"
)

# Style CSS pour l'interface
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# TITRE DYNAMIQUE (VÉRIFICATION VERSION)
st.title("🧬 Intelligence Croisée V2.1 (Expert)")
st.subheader("Analyse Prédictive : Euromillions du Mardi 28 Avril")
st.write("Dernière mise à jour : Lundi 27 Avril à 23h30 (Post-tirage Loto)")

# ==========================================
# 2. DONNÉES MISES À JOUR (POST-LOTO LUNDI)
# ==========================================

# Numéros chauds basés sur les sorties de Samedi (17,22,23,25,49) 
# et de Lundi (6,15,23,27,43)
numeros_loto_recents = [6, 15, 23, 27, 43, 17, 22, 25, 49]

# Top stats Euromillions (Forme + Réussite)
# On privilégie le 13 (Forme 15) et le 42 (Écart 16)
euro_cibles = [13, 23, 44, 42, 10, 49, 17, 27, 15, 6]

# ==========================================
# 3. LOGIQUE DE L'ALGORITHME "ENTONNOIR"
# ==========================================

def generer_ticket_expert():
    # BASES FIXES : Le 23 (Pivot Loto x2) et le 13 (Forme Euro Record)
    bases = [13, 23]
    
    # ÉCARTS ET DYNAMIQUE : 42 (Écart synchro) et 44 (Record réussite)
    piliers = [42, 44, 10]
    
    # SOUTIEN : Transfert du Loto (17, 27, 49, 15)
    soutien = [17, 27, 49, 6, 15]
    
    ticket = set(bases)
    
    # Mélange des candidats restants
    candidats = [n for n in (piliers + soutien) if n not in ticket]
    random.shuffle(candidats)
    
    while len(ticket) < 5:
        ticket.add(candidats.pop())
        
    return sorted(list(ticket))

# ==========================================
# 4. INTERFACE UTILISATEUR (ONGLETS)
# ==========================================

tab1, tab2, tab3 = st.tabs(["🏆 PRONOSTIC EXPERT", "📊 ANALYSE DATA", "🔄 FLUX MIROIR"])

# --- ONGLET 1 : GÉNÉRATEUR ---
with tab1:
    st.header("🎯 Ta Sélection Stratégique")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔥 GÉNÉRER MON TICKET PRIORITAIRE"):
            grille = generer_ticket_expert()
            # Sélection des étoiles (Focus sur 2, 8, 4 et 10)
            etoiles = sorted(random.sample([2, 4, 8, 10, 11], 2))
            
            st.success(f"## {grille[0]} — {grille[1]} — {grille[2]} — {grille[3]} — {grille[4]}")
            st.warning(f"## ⭐ Étoiles : {etoiles[0]} — {etoiles[1]}")
            
            # Analyse de l'équilibre
            nb_pairs = len([n for n in grille if n % 2 == 0])
            nb_impairs = 5 - nb_pairs
            
            st.divider()
            st.write(f"⚖️ **Analyse de l'Équilibre :**")
            st.write(f"Cette grille contient **{nb_pairs} Pairs** et **{nb_impairs} Impairs**.")
            
            if nb_pairs in [2, 3]:
                st.info("✅ **ÉQUILIBRE OPTIMAL :** Configuration la plus fréquente.")
            else:
                st.write("💡 **INFO :** Équilibre correct (1/4 ou 4/1).")
            st.balloons()
            
    with col2:
        st.write("### 🔍 Pourquoi ces numéros ?")
        st.markdown(f"""
        - **Le 23 (Pivot) :** Incontournable (sorti Samedi ET Lundi).
        - **Le 13 (Moteur) :** Forme Euro exceptionnelle (15).
        - **Le 42 (Écart) :** Grande probabilité de sortie (Écart 16).
        - **Le 27 (Transfert) :** Sorti ce lundi soir au Loto.
        """)

# --- ONGLET 2 : TABLEAUX ---
with tab2:
    st.header("📊 Statistiques de Convergence")
    df_data = []
    for n in [13, 23, 42, 44, 10, 49, 27]:
        prio = "HAUTE" if n in [13, 23, 42] else "MOYENNE"
        obs = "Pivot" if n == 23 else ("Écart 16" if n == 42 else "Forme 15" if n == 13 else "Stable")
        df_data.append({"Numéro": n, "Priorité": prio, "Observation": obs})
    
    df = pd.DataFrame(df_data)
    st.table(df.sort_values(by="Priorité"))

# --- ONGLET 3 : MIROIR ---
with tab3:
    st.header("🔄 Flux Miroir : Lundi ➔ Mardi")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Sortis Lundi (Loto)")
        st.code("6 - 15 - 23 - 27 - 43")
    with col_b:
        st.subheader("Bases Euro (Mardi)")
        st.code("13 - 44 - 42 - 10 - 49")

st.divider()
st.caption(f"Propulsé par ton IA - Version 2.1 - Mise à jour {random.randint(1000,9999)}")
