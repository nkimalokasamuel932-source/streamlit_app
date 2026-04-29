import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="IA EXPERT V3.2 - Dual Cycles",
    page_icon="🧬",
    layout="wide"
)

# --- 2. STYLE CSS PERSONNALISÉ (Le Visuel) ---
st.markdown("""
    <style>
    .main { background-color: #050a14; color: #ffffff; }
    .euro-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 255, 204, 0.2);
        margin-bottom: 30px;
    }
    .loto-container {
        background: linear-gradient(135deg, #1a0f1f 0%, #2d1b36 100%);
        border: 2px solid #ff00ff;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 0, 255, 0.2);
    }
    .number-circle {
        display: inline-block;
        width: 60px;
        height: 60px;
        line-height: 60px;
        border-radius: 50%;
        font-size: 24px;
        font-weight: bold;
        margin: 5px;
        color: #000;
    }
    .euro-num { background-color: #00ffcc; }
    .loto-num { background-color: #ff00ff; color: #fff; }
    .star-num { background-color: #ffcc00; }
    .stButton > button { width: 100%; font-weight: bold; height: 3.5em; border-radius: 12px; font-size: 1.1em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES DES CYCLES (Données Avril) ---
# Format : [Réussite, Écart_Actuel, Dernier_Tirage_Vu, Zone]
# Zones : 1 = Bas (1-15), 2 = Milieu (16-35), 3 = Haut (36-50)
db_euro = {
    1: [185, 4, 14, 1], 2: [179, 4, 14, 1], 3: [187, 60, 0, 1], 
    4: [197, 10, 14, 1], 6: [188, 16, 21, 1], 12: [194, 10, 21, 1],
    13: [202, 2, 21, 1], 26: [202, 0, 28, 2], 29: [216, 0, 28, 2],
    32: [178, 35, 0, 2], 41: [179, 0, 28, 3], 42: [219, 17, 0, 3],
    47: [181, 0, 28, 3]
}

db_loto = {
    2: [283, 2, 24, 1], 6: [297, 0, 27, 1], 12: [283, 2, 24, 1],
    15: [311, 0, 27, 1], 23: [291, 0, 27, 2], 25: [273, 1, 25, 2],
    27: [290, 0, 27, 2], 30: [294, 3, 22, 2], 43: [276, 0, 27, 3],
    49: [290, 1, 25, 3]
}

# --- 4. MOTEUR DE CALCUL DES CYCLES ---
def calculer_score_expert(num, database):
    d = database.get(num)
    # A. Score de base (Réussite Historique + Tension d'écart)
    score = (d[0] / 321 * 30) + (d[1] / 60 * 30)
    
    # B. Logique de Cycle Respiratoire (Expiration/Inspiration)
    if d[2] >= 28: # Surchauffe (Mardi dernier)
        score -= 25 
    elif d[2] <= 14 or d[2] == 0: # Besoin d'expiration (Absence prolongée)
        score += 40
        
    # C. Bonus de Zone (Attraction vers le bas prévue pour le 01/05)
    if d[3] == 1:
        score += 20
        
    return round(score, 2)

# --- 5. INTERFACE UTILISATEUR ---
st.title("🧬 IA EXPERT V3.2 : Système de Fusion Temporelle")
st.write(f"Analyse des cycles au {datetime.now().strftime('%d/%m/%Y')} | **Statut : Prêt pour Vendredi 01/05**")

# Barre de diagnostic
st.info("📊 **Diagnostic IA :** La saturation de la Zone 3 (40-50) est confirmée. Le cycle d'expiration force le retour vers la Zone 1 (1-15).")

tab1, tab2 = st.tabs(["🎯 GÉNÉRATEUR DE PRÉDICTIONS", "📊 MATRICE DES CYCLES"])

with tab1:
    col_left, col_right = st.columns(2)

    # --- MODULE EUROMILLIONS ---
    with col_left:
        st.subheader("🇪🇺 Pronostic Euromillions")
        if st.button("CALCULER CYCLE EURO"):
            scores_e = {n: calculer_score_expert(n, db_euro) for n in db_euro.keys()}
            res_e = sorted(scores_e, key=scores_e.get, reverse=True)[:5]
            res_e.sort()
            
            # Affichage Visuel
            st.markdown("<div class='euro-container'>", unsafe_allow_html=True)
            st.write("#### GRILLE D'EXPIRATION")
            nums_html = "".join([f"<div class='number-circle euro-num'>{n}</div>" for n in res_e])
            st.markdown(nums_html, unsafe_allow_html=True)
            
            # Étoiles (Cycle Balancier)
            e1, e2 = random.choice([(2,10), (3,8), (1,11)])
            st.markdown(f"""
                <div style='margin-top:20px;'>
                    <div class='number-circle star-num'>{e1}</div>
                    <div class='number-circle star-num'>{e2}</div>
                    <p><b>Étoiles de Tension</b></p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- MODULE LOTO ---
    with col_right:
        st.subheader("🇫🇷 Pronostic Loto")
        if st.button("CALCULER CYCLE LOTO"):
            scores_l = {n: calculer_score_expert(n, db_loto) for n in db_loto.keys()}
            res_l = sorted(scores_l, key=scores_l.get, reverse=True)[:5]
            res_l.sort()
            
            # Affichage Visuel
            st.markdown("<div class='loto-container'>", unsafe_allow_html=True)
            st.write("#### GRILLE DE BALANCIER")
            nums_l_html = "".join([f"<div class='number-circle loto
