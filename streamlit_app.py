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

# Style CSS pour améliorer le visuel
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
    .result-box {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# TITRE DYNAMIQUE
st.title("🧬 Intelligence Croisée V2.1 (Expert)")
st.subheader("Analyse Prédictive : Euromillions du Mardi 28 Avril")
st.write("Dernière mise à jour : Lundi 27 Avril à 23h30 (Post-tirage Loto)")

# ==========================================
# 2. BASE DE DONNÉES STATISTIQUES (MISES À JOUR)
# ==========================================

# Numéros chauds basés sur les sorties de Samedi (17,22,23,25,49) 
# et de Lundi (6,15,23,27,43)
numeros_loto_recents = [6, 15, 23, 27, 43, 17, 22, 25, 49]

# Top stats Euromillions (Forme + Réussite)
# 13 (Forme 15), 44 (Réussite 222), 42 (Écart 16), 23 (Pivot)
stats_euro = {
    '13': {'reussite': 202, 'forme': 15, 'ecart': 1},
    '44': {'reussite': 222, 'forme': 12, 'ecart': 3},
    '42': {'reussite': 219, 'forme': 10, 'ecart': 16},
    '23': {'reussite': 218, 'forme': 4, 'ecart': 2},
    '10': {'reussite': 211, 'forme': 11, 'ecart': 4},
    '49': {'reussite': 195, 'forme': 4, 'ecart': 5}
}

# Calcul de la convergence (Numéros présents dans la dynamique Loto et Euro)
euro_cibles = [13, 23, 44, 42, 10, 49, 17, 27]
convergence = list(set(numeros_loto_recents) & set(euro_cibles))

# ==========================================
# 3. LOGIQUE DE L'ALGORITHME "ENTONNOIR"
# ==========================================

def generer_ticket_expert():
    # BASES FIXES : Le 23 (Pivot Loto) et le 13 (Forme Euro)
    bases = [13, 23]
    
    # ÉCARTS ET DYNAMIQUE : 42 (Écart synchro) et 44 (Record)
    piliers = [42, 44, 10]
    
    # SOUTIEN : Transfert du Loto (17, 27, 49)
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
    st.header("🎯 Générateur de Grilles Stratégiques")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### Cliquez pour générer")
        if st.button("🔥 GÉNÉRER MON TICKET PRIORITAIRE"):
            grille = generer_ticket_expert()
            # Sélection des étoiles (Focus sur 2, 8, 4 et 10)
            etoiles = sorted(random.sample([2, 4, 8, 10, 11], 2))
            
            st.success(f"## {grille[0]} — {grille[1]} — {grille[2]} — {grille[3]} — {grille[4]}")
            st.warning(f"## ⭐ Étoiles : {etoiles[0]} — {etoiles[1]}")
            
            # Analyse de l'équilibre
            nb_pairs = len([n for n in grille if n % 2 == 0])
            nb_impairs = 5 - nb_pairs
            
            st.info(f"⚖️ **Équilibre :** {nb_pairs} Pairs / {nb_impairs} Impairs")
            if nb_pairs in [2, 3]:
                st.write("✅ **Configuration Optimale**")
            else:
                st.write("💡 *Note : Configuration atypique*")
            st.balloons()
            
    with col2:
        st.write("### 🔍 Pourquoi ces numéros ?")
        st.markdown(f"""
        - **Le 23 (Pivot) :** Confirmé par sa sortie au Loto ce lundi soir.
        - **Le 13 (Moteur) :** Possède le score de forme le plus élevé à l'Euro (15).
        - **Le 42 (Écart) :** Attendu pour corriger son retard (Écart 16).
        - **Le 27 (Transfert) :** Sorti ce soir, forte affinité Euro.
        """)

# --- ONGLET 2 : TABLEAUX ---
with tab2:
    st.header("📊 Statistiques de Convergence")
    
    df_data = []
    for n in euro_cibles:
        prio = "HAUTE" if n in [13, 23, 42] else "MOYENNE"
        obs = "Pivot" if n == 23 else ("Écart 16" if n == 42 else "Forme 15" if n == 13 else "Stable")
        df_data.append({"Numéro": n, "Priorité": prio, "Observation": obs})
    
    df = pd.DataFrame(df_data)
    st.table(df.sort_values(by="Priorité"))

# --- ONGLET 3 : MIROIR ---
with tab3:
    st.header("🔄 Flux Miroir : Lundi ➔ Mardi")
    st.write("Analyse des numéros ayant circulé entre les tirages récents :")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Sortis Lundi (Loto)")
        st.code("6 - 15 - 23 - 27 - 43")
        st.write("Le 23 et le 27 sont les plus susceptibles de 'sauter' vers l'Euro demain.")
        
    with col_b:
        st.subheader("Attendus Mardi (Euro)")
        st.code("13 - 44 - 42 - 10")
        st.write("Ces numéros sont les piliers historiques qui équilibrent le tirage.")

# PIED DE PAGE
st.markdown("---")
st.caption(f"Propulsé par ton Algorithme de Fusion - Version 2.1 - Mise à jour {random.randint(1000,9999)}")
