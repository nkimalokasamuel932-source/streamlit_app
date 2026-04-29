import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V3.2.1", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a14; color: #ffffff; }
    .euro-container { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; margin-bottom: 30px; }
    .loto-container { background: linear-gradient(135deg, #1a0f1f 0%, #2d1b36 100%); border: 2px solid #ff00ff; border-radius: 20px; padding: 25px; text-align: center; }
    .number-circle { display: inline-block; width: 60px; height: 60px; line-height: 60px; border-radius: 50%; font-size: 24px; font-weight: bold; margin: 5px; color: #000; text-align: center; }
    .euro-num { background-color: #00ffcc; }
    .loto-num { background-color: #ff00ff; color: #fff; }
    .star-num { background-color: #ffcc00; }
    .stButton > button { width: 100%; font-weight: bold; height: 3.5em; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 IA EXPERT V3.2.1 : Dual-Core Fix")

# --- 2. DONNÉES ---
db_euro = {
    1: [185, 4, 14, 1], 2: [179, 4, 14, 1], 3: [187, 60, 0, 1], 
    4: [197, 10, 14, 1], 13: [202, 2, 21, 1], 26: [202, 0, 28, 2], 
    32: [178, 35, 0, 2], 42: [219, 17, 0, 3]
}

db_loto = {
    2: [283, 2, 24, 1], 6: [297, 0, 27, 1], 12: [283, 2, 24, 1],
    15: [311, 0, 27, 1], 23: [291, 0, 27, 2], 43: [276, 0, 27, 3]
}

def calculer_score(num, db):
    d = db.get(num)
    score = (d[0] / 321 * 30) + (d[1] / 60 * 30)
    if d[2] >= 28: score -= 25
    elif d[2] <= 14 or d[2] == 0: score += 40
    if d[3] == 1: score += 20
    return round(score, 2)

# --- 3. INTERFACE ---
tab1, tab2 = st.tabs(["🎯 PRÉDICTIONS", "📊 FLUX"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🇪🇺 Euro")
        if st.button("CALCULER EURO"):
            sc_e = {n: calculer_score(n, db_euro) for n in db_euro.keys()}
            res_e = sorted(sc_e, key=sc_e.get, reverse=True)[:5]
            st.markdown("<div class='euro-container'>", unsafe_allow_html=True)
            nums_e_html = "".join([f"<div class='number-circle euro-num'>{n}</div>" for n in sorted(res_e)])
            st.markdown(nums_e_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    with col2:
        st.subheader("🇫🇷 Loto")
        if st.button("CALCULER LOTO"):
            sc_l = {n: calculer_score(n, db_loto) for n in db_loto.keys()}
            res_l = sorted(sc_l, key=sc_l.get, reverse=True)[:5]
            st.markdown("<div class='loto-container'>", unsafe_allow_html=True)
            nums_l_html = "".join([f"<div class='number-circle loto-num'>{n}</div>" for n in sorted(res_l)])
            st.markdown(nums_l_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write("Analyse des cycles en cours...")
    st.dataframe(pd.DataFrame([{"Num": k, "Score": calculer_score(k, db_euro)} for k in db_euro.keys()]))
