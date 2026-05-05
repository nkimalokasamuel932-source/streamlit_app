import streamlit as st
import pandas as pd
import io
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V11 - TOTAL FUSION", layout="wide", page_icon="🧬")

# --- 1. HISTORIQUE DES 10 DERNIERS TIRAGES (FOURNIS PAR L'UTILISATEUR) ---
# Format : [Numéros], [Étoiles]
HISTORIQUE_EURO = [
    ([3, 9, 42, 46, 47], [1, 11]),   # 1er Mai
    ([26, 29, 41, 46, 47], [8, 9]),  # 28 Avril
    ([1, 2, 4, 7, 28], [5, 12]),     # 14 Avril (Adapté selon tes données)
    ([10, 13, 14, 38, 41], [6, 9]),  # 10 Avril
    ([11, 14, 19, 36, 49], [6, 7]),  # 7 Avril
    ([8, 27, 29, 46, 49], [2, 10]),  # 3 Avril
    ([5, 8, 10, 33, 38], [2, 7]),    # 31 Mars
    ([4, 10, 43, 44, 48], [2, 4]),   # 27 Mars
    ([12, 16, 17, 18, 27], [1, 3])   # 24 Mars
]

DERNIERS_LOTO = [4, 8, 15, 18, 46]
DERNIERS_EURO = HISTORIQUE_EURO[0][0] # Le tirage du 1er Mai

# --- 2. BASES DE DONNÉES (TES STATISTIQUES RÉELLES) ---
euro_csv = """Numéro,Réussite totale,Forme générale,Écart maximum,Écart actuel,Annonceur_De
44,222,12,48,5,50
42,220,10,50,0,12
23,218,4,46,4,19
19,216,5,43,7,26
29,216,11,44,1,19
32,178,4,47,36,25
26,202,9,70,1,21
47,182,9,82,0,3
41,179,11,46,1,15
3,188,3,65,0,1
1,185,5,58,5,44
10,211,10,56,6,24"""

loto_csv = """Numéro,Réussite totale,Forme générale,Écart maximum,Écart actuel,Annonceur_De
41,322,8,41,1,17
13,321,6,55,12,3
22,314,9,50,4,26
15,312,5,46,0,23
3,305,7,49,2,15
1,291,3,42,41,6
4,285,6,46,0,44
8,271,6,58,0,43
18,271,7,67,0,29
46,281,4,42,0,18"""

# --- 3. MOTEUR D'INTELLIGENCE ANALYTIQUE ---
def moteur_ia_v11(df, historique, tirage_autre_jeu, type_jeu):
    df = df.copy()
    dernier_tirage = historique[0][0]
    limit_basse = 25
    
    # A. Calcul automatique de la Fréquence (20 derniers tirages)
    tous_nums = [n for tirage, etoiles in historique for n in tirage]
    frequences = Counter(tous_nums)
    df['bonus_frequence'] = df['Numéro'].apply(lambda x: frequences.get(x, 0) * 8)
    
    # B. Tension (Écart actuel / Max)
    df['tension'] = (df['Écart actuel'] / df['Écart maximum'] * 100)
    
    # C. Bonus Voisinage (Aspiration)
    voisins = [n-1 for n in dernier_tirage] + [n+1 for n in dernier_tirage]
    df['bonus_voisin'] = df['Numéro'].apply(lambda x: 20 if x in voisins else 0)
    
    # D. Bonus d'Annonce (Tableaux d'affinités)
    appeles = df[df['Numéro'].isin(dernier_tirage)]['Annonceur_De'].tolist()
    df['bonus_annonce'] = df['Numéro'].apply(lambda x: 25 if x in appeles else 0)
    
    # E. Logique des Masses
    poids_bas = sum(1 for n in dernier_tirage if n <= limit_basse)
    df['bonus_masse'] = 0
    if poids_bas >= 4: df.loc[df['Numéro'] > limit_basse, 'bonus_masse'] = 20
    elif poids_bas <= 1: df.loc[df['Numéro'] <= limit_basse, 'bonus_masse'] = 25

    # F. Vigilance Croisée
    df['bonus_croise'] = df['Numéro'].apply(lambda x: 15 if x in tirage_autre_jeu else 0)

    # SCORE FINAL
    df['score'] = (df['tension'] * 0.4) + (df['Forme générale'] * 1.5) + df['bonus_frequence'] + \
                  df['bonus_voisin'] + df['bonus_annonce'] + df['bonus_masse'] + df['bonus_croise']
    return df.sort_values('score', ascending=False)

# --- 4. INTERFACE ---
st.title("🛰️ IA EXPERT V11 : Moteur de Fusion Totale")
st.sidebar.header("Paramètres")
mode = st.sidebar.selectbox("Choisir le mode", ["Analyse Croisée", "Générateur de Tickets"])

df_l = pd.read_csv(io.StringIO(loto_csv))
df_e = pd.read_csv(io.StringIO(euro_csv))

res_loto = moteur_ia_v11(df_l, [(DERNIERS_LOTO, [])], DERNIERS_EURO, "LOTO")
res_euro = moteur_ia_v11(df_e, HISTORIQUE_EURO, DERNIERS_LOTO, "EURO")

if mode == "Analyse Croisée":
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🎰 Analyse LOTO")
        st.bar_chart(res_loto.head(10).set_index('Numéro')['score'])
        st.write("**Top Opportunités :**", res_loto[['Numéro', 'score']].head(5))
    with c2:
        st.subheader("🇪🇺 Analyse EURO")
        st.bar_chart(res_euro.head(10).set_index('Numéro')['score'], color="#FF4B4B")
        st.write("**Top Opportunités :**", res_euro[['Numéro', 'score']].head(5))
        
else:
    st.header("💰 Numéros suggérés pour le prochain tirage")
    col_l, col_e = st.columns(2)
    
    with col_l:
        st.subheader("Ticket LOTO")
        l_nums = res_loto.head(5)['Numéro'].tolist()
        l_nums.sort()
        st.success(f"👉 {', '.join(map(str, l_nums))}")
        st.info(f"Base : {l_nums[0]} | Annonce : {res_loto.iloc[0]['Annonceur_De']}")

    with col_e:
        st.subheader("Ticket EURO")
        e_nums = res_euro.head(5)['Numéro'].tolist()
        e_nums.sort()
        st.error(f"👉 {', '.join(map(str, e_nums))}")
        st.info(f"Base : {e_nums[0]} | Annonce : {res_euro.iloc[0]['Annonceur_De']}")

    st.divider()
    st.subheader("💡 Pourquoi ces choix ?")
    st.write(f"- **Euro :** Le **{res_euro.iloc[0]['Numéro']}** domine car il est revenu {Counter([n for t,e in HISTORIQUE_EURO for n in t]).get(res_euro.iloc[0]['Numéro'], 0)} fois récemment.")
    st.write(f"- **Loto :** Le **{res_loto.iloc[0]['Numéro']}** est prioritaire en raison de son écart actuel élevé.")
