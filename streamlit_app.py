import streamlit as st
import pandas as pd
import io

# --- CONFIGURATION DE L'INTERFACE ---
st.set_page_config(page_title="IA PREDICT ULTIME V10", layout="wide", page_icon="🧬")

# --- 1. SYNCHRONISATION DES DERNIERS TIRAGES ---
# Ces numéros déclenchent les bonus de voisinage et d'annonce
DERNIERS_LOTO = [4, 8, 15, 18, 46]
DERNIERS_EURO = [26, 29, 41, 46, 47]

# --- 2. BASE DE DONNÉES INTÉGRÉE (TES STATISTIQUES RÉELLES) ---
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
46,281,4,42,0,18
2,284,9,55,2,9
17,284,10,58,1,41
23,291,9,52,3,32
5,289,9,46,8,9
31,299,6,67,2,13"""

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
13,202,14,58,3,26
1,185,5,58,5,44"""

# --- 3. LE MOTEUR D'INTELLIGENCE ARTIFICIELLE ---
def moteur_ia_ultime(df, tirage_jeu, tirage_autre_jeu, type_jeu):
    df = df.copy()
    limit_basse = 24.5 if type_jeu == "LOTO" else 25.5
    
    # A. Calcul de la Tension (Écart)
    df['tension'] = (df['Écart actuel'] / df['Écart maximum'] * 100)
    
    # B. Logique de Voisinage (Aspiration latérale)
    voisins = [n-1 for n in tirage_jeu] + [n+1 for n in tirage_jeu]
    df['bonus_voisin'] = df['Numéro'].apply(lambda x: 22 if x in voisins else 0)
    
    # C. Logique des Annonces (Succession réelle)
    appeles = df[df['Numéro'].isin(tirage_jeu)]['Annonceur_De'].tolist()
    df['bonus_annonce'] = df['Numéro'].apply(lambda x: 28 if x in appeles else 0)
    
    # D. Vigilance Croisée (Contagion Loto <-> Euro)
    # Si un numéro est sorti dans l'autre jeu récemment, il est "chaud"
    df['bonus_croise'] = df['Numéro'].apply(lambda x: 15 if x in tirage_autre_jeu else 0)
    
    # E. Logique des Masses (Équilibre des moitiés de grille)
    poids_bas = sum(1 for n in tirage_jeu if n < limit_basse)
    df['bonus_masse'] = 0
    if poids_bas >= 4: # Trop de petits, on booste les grands
        df.loc[df['Numéro'] > limit_basse, 'bonus_masse'] = 20
    elif poids_bas <= 1: # Trop de grands, on booste les petits
        df.loc[df['Numéro'] < limit_basse, 'bonus_masse'] = 25

    # CALCUL DU SCORE FINAL PONDÉRÉ
    df['score_final'] = (
        (df['tension'] * 0.40) + 
        (df['Forme générale'] * 1.8) + 
        df['bonus_voisin'] + 
        df['bonus_annonce'] + 
        df['bonus_croise'] + 
        df['bonus_masse']
    )
    return df.sort_values('score_final', ascending=False)

# --- 4. INTERFACE UTILISATEUR (STREAMLIT) ---
st.title("🧬 IA EXPERT V10 : Fusion Totale & Prédiction")
st.markdown(f"**Dernier Loto :** {DERNIERS_LOTO} | **Dernier Euro :** {DERNIERS_EURO}")

df_l = pd.read_csv(io.StringIO(loto_csv))
df_e = pd.read_csv(io.StringIO(euro_csv))

res_loto = moteur_ia_ultime(df_l, DERNIERS_LOTO, DERNIERS_EURO, "LOTO")
res_euro = moteur_ia_ultime(df_e, DERNIERS_EURO, DERNIERS_LOTO, "EURO")

# --- SECTION 5 : LE GÉNÉRATEUR DE TICKETS ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.header("🎰 TICKET SUGGÉRÉ LOTO")
    ticket_l = res_loto.head(5)['Numéro'].tolist()
    ticket_l.sort()
    st.subheader(f"👉 {', '.join(map(str, ticket_l))}")
    with st.expander("Pourquoi ces numéros Loto ?"):
        st.write(res_loto[['Numéro', 'score_final', 'Écart actuel']].head(5))

with c2:
    st.header("🇪🇺 TICKET SUGGÉRÉ EURO")
    ticket_e = res_euro.head(5)['Numéro'].tolist()
    ticket_e.sort()
    st.subheader(f"👉 {', '.join(map(str, ticket_e))}")
    with st.expander("Pourquoi ces numéros Euro ?"):
        st.write(res_euro[['Numéro', 'score_final', 'Écart actuel']].head(5))

# --- SECTION 6 : ÉVALUATION DES SUJETS ABORDÉS ---
st.divider()
st.subheader("🧠 Analyse Multi-Sujets")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.write("**Logique des Masses**")
    m_e = sum(1 for n in DERNIERS_EURO if n < 25)
    st.metric("Poids Bas Euro", f"{m_e}/5", "-25 pts zone haute" if m_e < 2 else "Ok")

with col_b:
    st.write("**Vigilance Croisée**")
    croises = set(DERNIERS_LOTO).intersection(set(DERNIERS_EURO))
    st.write(f"Numéros communs : {list(croises) if croises else 'Aucun'}")
    st.info("Le 46 est sorti sur les DEUX jeux ! Tension maximale sur ses voisins (45-47).")

with col_c:
    st.write("**Alerte Écart (Tension)**")
    num_t = res_loto.loc[res_loto['tension'].idxmax()]
    st.warning(f"Le n°{int(num_t['Numéro'])} est à {num_t['tension']:.1f}% de son écart max !")
