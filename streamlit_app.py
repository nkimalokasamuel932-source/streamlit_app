import streamlit as st
import pandas as pd
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V2 - PRÉDICTIONS", layout="wide", page_icon="🎯")

# Tirages réels pour les calculs de voisinage (Voisins du dernier tirage)
DERNIERS_LOTO = [4, 12, 25, 33, 48]
DERNIERS_EURO = [25, 26, 30, 40, 45]

# --- FONCTION DE CALCUL AVANCÉ ---
def calculer_scores_expert(df, derniers_numeros, limite):
    df = df.copy()
    
    # 1. Calcul de la TENSION (Proximité de l'écart max)
    # Plus le score approche 100, plus le numéro est statistiquement "dû"
    df['tension'] = (df['ecart_actuel'] / df['ecart_max'] * 100).fillna(0)
    
    # 2. Calcul de l'ACCÉLÉRATION (Forme récente vs historique)
    # Un score > 100 signifie que le numéro sort plus souvent que sa moyenne
    moyenne_historique = df['reussite'].mean()
    df['acceleration'] = (df['forme_generale'] / (moyenne_historique / 10) * 100).fillna(0)
    
    # 3. Bonus VOISINAGE
    voisins = [n-1 for n in derniers_numeros] + [n+1 for n in derniers_numeros]
    df['bonus_voisin'] = df['numero'].apply(lambda x: 20 if x in voisins else 0)

    # 4. SCORE FINAL EXPERT (Pondération)
    # 40% Tension + 30% Accélération + 20% Sniper (Ecart Fav) + 10% Voisins
    df['score_expert'] = (df['tension'] * 0.4) + (df['acceleration'] * 0.3) + (df['ecart_fav'] * 2) + df['bonus_voisin']
    
    return df.sort_values('score_expert', ascending=False)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    if os.path.exists('data_expert.csv'):
        df = pd.read_csv('data_expert.csv')
        df['jeu'] = df['jeu'].astype(str).str.upper().str.strip()
        return df
    return None

df_raw = load_data()

# --- INTERFACE ---
st.title("🛰️ IA EXPERT V2 : Analyse Multi-Jeux")
st.markdown("Système de détection de **Tension** et d'**Accélération** fréquentielle.")

if df_raw is not None:
    # Traitement des données
    df_euro_final = calculer_scores_expert(df_raw[df_raw['jeu'] == 'EURO'], DERNIERS_EURO, 50)
    df_loto_final = calculer_scores_expert(df_raw[df_raw['jeu'] == 'LOTO'], DERNIERS_LOTO, 49)

    # --- BARRE DE RÉSUMÉ (METRICS) ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎯 Top Tension EURO", int(df_euro_final.iloc[0]['numero']), f"Score: {df_euro_final.iloc[0]['score_expert']:.1f}")
    m2.metric("🎰 Top Tension LOTO", int(df_loto_final.iloc[0]['numero']), f"Score: {df_loto_final.iloc[0]['score_expert']:.1f}")
    m3.metric("🔥 Accélération Max", int(df_euro_final.sort_values('acceleration', ascending=False).iloc[0]['numero']), "Signal Forme")
    m4.metric("📊 Données", "Synchronisées", "GitHub OK")

    st.divider()

    # --- AFFICHAGE PAR ONGLETS ---
    tab1, tab2, tab3 = st.tabs(["🇪🇺 EURO : Analyse Profonde", "🎰 LOTO : Analyse Profonde", "🧠 Comprendre les scores"])

    with tab1:
        st.subheader("Classement Expert Euromillions")
        st.dataframe(
            df_euro_final[['numero', 'score_expert', 'tension', 'acceleration', 'ecart_actuel', 'affinite']],
            use_container_width=True,
            column_config={
                "score_expert": st.column_config.ProgressColumn("Score Global", min_value=0, max_value=150, format="%.1f"),
                "tension": "Tension %",
                "acceleration": "Vitesse"
            }
        )

    with tab2:
        st.subheader("Classement Expert Loto France")
        st.dataframe(
            df_loto_final[['numero', 'score_expert', 'tension', 'acceleration', 'ecart_actuel', 'affinite']],
            use_container_width=True,
            column_config={
                "score_expert": st.column_config.ProgressColumn("Score Global", min_value=0, max_value=150, format="%.1f"),
                "tension": "Tension %",
                "acceleration": "Vitesse"
            }
        )

    with tab3:
        st.markdown("""
        ### Comment utiliser cette V2 ?
        * **La Tension % :** Si un numéro dépasse **80%**, il entre en zone critique de sortie (Ecart proche du record).
        * **L'Accélération :** Si le score est haut, le numéro est dans une 'série'. Il faut souvent en inclure un ou deux.
        * **Le Score Global :** C'est la synthèse. Un numéro avec un score élevé combine retard et probabilité de réveil.
        """)

    # --- SIDEBAR RECHERCHE ---
    with st.sidebar:
        st.header("🔍 Analyse par Numéro")
        num = st.number_input("Choisir un numéro", 1, 50)
        if num:
            stats = df_raw[df_raw['numero'] == num]
            st.write(stats)

else:
    st.error("Le fichier data_expert.csv est manquant sur votre GitHub.")
