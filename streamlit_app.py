import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURATION DE L'INTERFACE ---
st.set_page_config(page_title="IA EXPERT V3.0", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background: #161b22; border: 1px solid #00ffcc; border-radius: 10px; padding: 15px; }
    .ticket-box { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #38bdf8; border-radius: 20px; padding: 25px; text-align: center; }
    div.stButton > button:first-child { background: #00ffcc; color: #000; font-weight: bold; width: 100%; border-radius: 10px; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 IA EXPERT V3.0 : Fusion des Cycles")
st.write(f"**Analyse Multidimensionnelle : Loto & Euromillions** | Date : {datetime.now().strftime('%d/%m/%Y')}")

# --- 1. BASE DE DONNÉES CONSOLIDÉE (MÉMOIRE AVRIL) ---
# Format : { Numéro: [Réussite_T_Euro, Tension_Euro, Présence_Loto, Type_Zone] }
# Type_Zone : 1=Bas (1-15), 2=Milieu (16-35), 3=Haut (36-50)
db = {
    1:  [185, 4, 1, 1],  # Présent Loto 24/04
    2:  [179, 4, 2, 1],  # Présent Loto 20/04 et 24/04
    3:  [187, 60, 0, 1], # TENSION MAX (Alerte Rouge)
    4:  [197, 4, 1, 1],  # Présent Loto 27/04 (Chance)
    6:  [188, 16, 1, 1], # Présent Loto 27/04
    12: [194, 10, 2, 1], # Présent Loto 20/04 et 24/04
    13: [202, 2, 0, 1],  # Masse Euro Élite
    23: [218, 3, 1, 2],  # Présent Loto 27/04
    32: [178, 35, 0, 2], # Oublié d'Avril
    42: [219, 17, 0, 3], # Masse + Tension (Voisin du 43 Loto)
    43: [179, 9, 2, 3]   # Présent Loto 22/04 et 27/04
}

# --- 2. LOGIQUE DE CALCUL HARMONIQUE (V3.0) ---
def calculer_score_final(n):
    d = db.get(n)
    if not d: return 0
    
    # A. Poids Masse (Réussite Totale) - 30%
    score_masse = (d[0] / 222) * 30
    
    # B. Poids Tension (Écart Euro) - 35%
    score_tension = (d[1] / 60) * 35
    
    # C. Poids Résonance (Présence Loto) - 25%
    # Migration des numéros qui "chauffent" au Loto
    score_resonance = (d[2] * 12.5)
    
    # D. Correction de Zone (Respiration) - 10%
    # Si zone Haute (3) -> Malus (Surcharge)
    # Si zone Basse (1) -> Bonus (Retour aux sources)
    correction = 10 if d[3] == 1 else (-5 if d[3] == 3 else 0)
    
    return round(score_masse + score_tension + score_resonance + correction, 2)

# --- 3. INTERFACE UTILISATEUR ---
tab1, tab2, tab3 = st.tabs(["🎯 GÉNÉRATEUR HARMONIQUE", "📊 ANALYSEUR DE FLUX", "📝 HISTORIQUE CYCLIQUE"])

with tab1:
    st.info("Cette version fusionne le cycle de respiration (14 jours) et le balancier Loto (Paires/Impaires).")
    
    if st.button("🚀 CALCULER LA GRILLE DE RUPTURE"):
        scores = {n: calculer_score_final(n) for n in db.keys()}
        tri = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Sélection Top 5
        grille = sorted([x[0] for x in tri[:5]])
        # Étoiles basées sur le balancier (2 et 10 sont les ancres du mois)
        etoiles = [2, 10] if random.random() > 0.5 else [3, 9]
        
        st.markdown("<div class='ticket-box'>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, n in enumerate(grille):
            cols[i].metric(label=f"N°{i+1}", value=n)
        st.markdown(f"### ⭐ ÉTOILES : {etoiles[0]} — {etoiles[1]}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.balloons()

with tab2:
    st.subheader("Puissance des Numéros (Masse + Résonance)")
    sc = {n: calculer_score_final(n) for n in db.keys()}
    df = pd.DataFrame([
        {"Numéro": k, "Score Global": v, "Tension": db[k][1], "Résonance Loto": db[k][2]} 
        for k, v in sc.items()
    ]).sort_values("Score Global", ascending=False)
    
    st.table(df)

with tab3:
    st.write("### Rappel des logiques détectées")
    colA, colB = st.columns(2)
    with colA:
        st.write("**Euromillions (Cycle Respiratoire)**")
        st.write("* 14/04 : Zone Basse")
        st.write("* 28/04 : Zone Haute (Saturation)")
        st.warning("Action : Retour Zone Basse attendu.")
    with colB:
        st.write("**Loto (Cycle Balancier)**")
        st.write("* 24/04 : 100% Paires")
        st.write("* 25/04 : 80% Impaires")
        st.success("Action : Équilibre Mixte attendu.")

st.divider()
st.caption("Système Expert V3.0 - Logiciel de prédiction basé sur la saturation zonale.")
