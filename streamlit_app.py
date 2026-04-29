import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="IA EXPERT V3.3 ELITE", page_icon="🧪", layout="wide")

# Injection de polices et style Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&family=Poppins:wght@300;600&display=swap');
    
    .main { background-color: #050a14; font-family: 'Urbanist', sans-serif; }
    
    /* Effet Glassmorphism pour les cartes */
    .game-card {
        padding: 30px;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .euro-border { border-top: 5px solid #00ffcc; box-shadow: 0 10px 30px rgba(0, 255, 204, 0.1); }
    .loto-border { border-top: 5px solid #ff00ff; box-shadow: 0 10px 30px rgba(255, 0, 255, 0.1); }

    /* Boules de tirage stylisées */
    .ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 65px;
        height: 65px;
        border-radius: 50%;
        font-size: 26px;
        font-weight: 700;
        margin: 8px;
        color: #000;
        box-shadow: inset -5px -5px 15px rgba(0,0,0,0.2), 5px 5px 15px rgba(0,0,0,0.3);
    }
    .euro-ball { background: linear-gradient(145deg, #00ffcc, #009988); }
    .loto-ball { background: linear-gradient(145deg, #ff00ff, #aa00aa); color: #fff; }
    .star-ball { background: linear-gradient(145deg, #ffd700, #b8860b); width: 55px; height: 55px; font-size: 22px; }

    /* Badges de raison */
    .reason-tag {
        display: block;
        font-size: 10px;
        text-transform: uppercase;
        color: #94a3b8;
        margin-top: -5px;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #1e293b, #334155);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        height: 4em;
        letter-spacing: 1px;
    }
    .stButton > button:hover { border-color: #00ffcc; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE ET DONNÉES ---
db_euro = {
    1: [185, 4, 14, 1, "Masse"], 2: [179, 4, 14, 1, "Masse"], 
    3: [187, 60, 0, 1, "Tension Max"], 4: [197, 10, 14, 1, "Forme"],
    12: [194, 10, 21, 1, "Voisinage"], 13: [202, 2, 21, 1, "Élite"], 
    32: [178, 35, 0, 2, "Oublié"], 42: [219, 17, 0, 3, "Aspiration"]
}

db_loto = {
    2: [283, 2, 24, 1, "Ancre"], 6: [297, 0, 27, 1, "Voisin"], 
    12: [283, 2, 24, 1, "Ancre"], 15: [311, 0, 27, 1, "Masse"], 
    23: [291, 0, 27, 2, "Pivot"], 43: [276, 0, 27, 3, "Saturation"]
}

def calculer_score(n, db):
    d = db.get(n)
    score = (d[0] / 321 * 30) + (d[1] / 60 * 30)
    if d[2] >= 28: score -= 25
    elif d[2] <= 14 or d[2] == 0: score += 40
    if d[3] == 1: score += 20
    return round(score, 2)

# --- 3. INTERFACE ---
st.title("🧪 IA EXPERT V3.3 : Elite Analytics")
st.caption(f"Système de Fusion Temporelle synchronisé | {datetime.now().strftime('%H:%M:%S')}")

tab1, tab2 = st.tabs(["🎯 TERMINAL DE PRÉDICTION", "📊 ANALYSEUR DE CYCLES"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='game-card euro-border'>", unsafe_allow_html=True)
        st.write("### 🇪🇺 EUROMILLIONS")
        st.write("Phase : **Expiration Zone 1**")
        
        if st.button("LANCER L'ALGORITHME EURO"):
            sc_e = {n: calculer_score(n, db_euro) for n in db_euro.keys()}
            res_e = sorted(sc_e, key=sc_e.get, reverse=True)[:5]
            
            # Affichage boules
            html_res = ""
            for n in sorted(res_e):
                tag = db_euro[n][4]
                html_res += f"<div style='display:inline-block;text-align:center;'><div class='ball euro-ball'>{n}</div><span class='reason-tag'>{tag}</span></div>"
            st.markdown(html_res, unsafe_allow_html=True)
            
            # Étoiles
            st.write("---")
            stars = random.choice([(2,10), (3,11), (5,9)])
            st.markdown(f"<div class='ball star-ball'>{stars[0]}</div><div class='ball star-ball'>{stars[1]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='game-card loto-border'>", unsafe_allow_html=True)
        st.write("### 🇫🇷 LOTO NATIONAL")
        st.write("Phase : **Balancier Symétrique**")
        
        if st.button("LANCER L'ALGORITHME LOTO"):
            sc_l = {n: calculer_score(n, db_loto) for n in db_loto.keys()}
            res_l = sorted(sc_l, key=sc_l.get, reverse=True)[:5]
            
            html_loto = ""
            for n in sorted(res_l):
                tag = db_loto[n][4]
                html_loto += f"<div style='display:inline-block;text-align:center;'><div class='ball loto-ball'>{n}</div><span class='reason-tag'>{tag}</span></div>"
            st.markdown(html_loto, unsafe_allow_html=True)
            
            # Chance
            st.write("---")
            chance = random.choice([4, 6, 1])
            st.markdown(f"<div class='ball star-ball' style='background:#ff4b4b;color:white;'>{chance}</div><br><span class='reason-tag'>Chance</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write("#### 🛡️ Indice de Confiance des Cycles")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Tension Globale Euro", "85%", "+12% ce tirage")
        st.dataframe(pd.DataFrame([{"Num": k, "Score IA": calculer_score(k, db_euro)} for k in db_euro.keys()]).sort_values("Score IA", ascending=False), use_container_width=True)
    with col_b:
        st.metric("Équilibre Loto", "Mixte", "Optimal")
        st.dataframe(pd.DataFrame([{"Num": k, "Score IA": calculer_score(k, db_loto)} for k in db_loto.keys()]).sort_values("Score IA", ascending=False), use_container_width=True)

st.caption("Application V3.3 Elite - IA de rupture de cycles temporels.")
