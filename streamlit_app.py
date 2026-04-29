import streamlit as st
import pandas as pd
import random

# CONFIGURATION
st.set_page_config(page_title="Loto-Euro Fusion V2.3", page_icon="🧬", layout="wide")

st.title("🧬 Intelligence Croisée V2.3")
st.subheader("Analyse Prédictive : Vendredi 1er Mai 2026")

# --- 1. MISE À JOUR DES DONNÉES (POST-TIRAGE MARDI) ---
stats_euro = {
    34: {'reussite': 194, 'forme': 6, 'ecart_actuel': 16, 'ecart_max': 54}, # TENSION ++
    42: {'reussite': 219, 'forme': 10, 'ecart_actuel': 17, 'ecart_max': 50}, # TENSION ++
    13: {'reussite': 202, 'forme': 15, 'ecart_actuel': 2, 'ecart_max': 58}, # BASE FORME
    23: {'reussite': 218, 'forme': 4, 'ecart_actuel': 3, 'ecart_max': 46},  # BASE MIROIR
    11: {'reussite': 191, 'forme': 6, 'ecart_actuel': 6, 'ecart_max': 60},
    10: {'reussite': 211, 'forme': 11, 'ecart_actuel': 5, 'ecart_max': 56},
    7:  {'reussite': 198, 'forme': 6, 'ecart_actuel': 16, 'ecart_max': 51}, # NOUVELLE TENSION
    2:  {'reussite': 179, 'forme': 4, 'ecart_actuel': 4, 'ecart_max': 48}
}

# --- 2. TA FONCTION DE SCORE EXPERT ---
def calculer_score_expert(num):
    data = stats_euro.get(num)
    if not data: return 0
    
    # Tension (40%) : L'écart augmente, le score monte !
    tension = (data['ecart_actuel'] / data['ecart_max'] * 100)
    # Accélération (30%)
    acceleration = (data['forme'] / 20 * 100) 
    
    # Bonus Correction (Si zone 40 sortie massivement mardi, bonus aux zones 10-30)
    bonus_correction = 15 if num < 40 else 0
    
    score = (tension * 0.4) + (acceleration * 0.3) + bonus_correction
    return score

# --- 3. GÉNÉRATEUR ---
def generer_grille_v23():
    scores = {n: calculer_score_expert(n) for n in stats_euro.keys()}
    tri = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # On force la sortie des 2 plus grosses tensions (34 et 42 ?)
    bases = [tri[0][0], tri[1][0]]
    reste = [x[0] for x in tri[2:]]
    selection = bases + random.sample(reste, 3)
    return sorted(selection)

# --- 4. INTERFACE ---
tab1, tab2 = st.tabs(["🎯 PRONOSTIC VENDREDI", "📊 ANALYSE DES TENSIONS"])

with tab1:
    if st.button("🚀 GÉNÉRER LE TICKET V2.3"):
        grille = generer_grille_v23()
        etoiles = sorted(random.sample([3, 5, 9, 11], 2)) # Étoiles basées sur le 26-29
        
        st.success(f"### NUMÉROS : {', '.join(map(str, grille))}")
        st.warning(f"### ÉTOILES : {etoiles[0]} — {etoiles[1]}")
        st.info("Stratégie : Correction des écarts sur les numéros 34 et 42.")
        st.balloons()

with tab2:
    st.write("### Évolution des Scores après Mardi")
    resultats = []
    for n in stats_euro.keys():
        resultats.append({"Numéro": n, "Nouveau Score": round(calculer_score_expert(n), 2)})
    st.table(pd.DataFrame(resultats).sort_values("Nouveau Score", ascending=False))

st.caption("Version 2.3 - Mise à jour post-tirage du 28/04 - Prêt pour Vendredi !")
