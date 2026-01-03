import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =====================
# CONFIG STREAMLIT
# =====================
st.set_page_config(page_title="Simulation Badminton", layout="wide")
st.title("🏸 Simulation tactique de badminton")


# =====================
# CONSTANTES TERRAIN
# =====================
LONGUEUR = 13.4
LARGEUR_DOUBLE = 6.1
LARGEUR_SIMPLE = 5.18
FILET_X = LONGUEUR / 2
SERVICE_COURT = 1.98
SERVICE_LONG_DOUBLE = 0.76

# =====================
# INTERFACE UTILISATEUR
# =====================
col1, col2 = st.columns([1, 3])
with col1:
    st.subheader("🎛️ Paramètres")
    
    if "resimuler" not in st.session_state:
        st.session_state.resimuler = False

    if st.button("🔄 Resimuler la situation"):
        st.session_state.resimuler = True

    type_volant = st.radio(
        "Type de volant",
        ["haut", "à plat", "bas"],
        index=0
    )

    st.subheader("Orientation individuelle des joueurs")
    joueurs_A_droitier = []
    joueurs_B_droitier = []

    colA1, colA2 = st.columns(2)
    with colA1:
        choix = st.radio("A1 :", ["droitier", "gaucher"], index=0)
        joueurs_A_droitier.append(True if choix == "droitier" else False)
    with colA2:
        choix = st.radio("A2 :", ["droitier", "gaucher"], index=0)
        joueurs_A_droitier.append(True if choix == "droitier" else False)

    colB1, colB2 = st.columns(2)
    with colB1:
        choix = st.radio("B1 :", ["droitier", "gaucher"], index=0)
        joueurs_B_droitier.append(True if choix == "droitier" else False)
    with colB2:
        choix = st.radio("B2 :", ["droitier", "gaucher"], index=0)
        joueurs_B_droitier.append(True if choix == "droitier" else False)

st.subheader("Position du volant")

# Sliders pour le volant
volant_x = st.slider("Volant X (longueur)", min_value=0.0, max_value=LONGUEUR, value=float(st.session_state.volant_x), step=0.1)
volant_y = st.slider("Volant Y (largeur)", min_value=0.0, max_value=LARGEUR_DOUBLE, value=float(st.session_state.volant_y), step=0.1)

# Mettre à jour la position du volant dans la session
st.session_state.volant_x = volant_x
st.session_state.volant_y = volant_y
# =====================
# INITIALISATION SÛRE DES VARIABLES DE SESSION
# =====================
def init_variables():
    # Joueurs A
    st.session_state.joueurs_A_x = np.random.uniform(0.5, FILET_X - 0.5, 2)
    st.session_state.joueurs_A_y = np.random.uniform(0.5, LARGEUR_DOUBLE - 0.5, 2)

    # Joueurs B
    st.session_state.joueurs_B_x = np.random.uniform(FILET_X + 0.5, LONGUEUR - 0.5, 2)
    st.session_state.joueurs_B_y = np.random.uniform(0.5, LARGEUR_DOUBLE - 0.5, 2)

    # Volant
    st.session_state.volant_x = np.random.uniform(0.3, LONGUEUR - 0.3)
    st.session_state.volant_y = np.random.uniform(0.3, LARGEUR_DOUBLE - 0.3)

if st.session_state.resimuler or "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.resimuler = False
    init_variables()

# =====================
# ICÔNES VOLANT
# =====================
types_volant = {
    "haut":   {"marker": "^", "color": "green", "label": "Volant haut"},
    "à plat": {"marker": "s", "color": "blue",  "label": "Volant à plat"},
    "bas":    {"marker": "v", "color": "red",   "label": "Volant bas"},
}

icone = types_volant[type_volant]
couleur_droite = icone["color"]

# =====================
# DESSIN DU TERRAIN
# =====================
fig, ax = plt.subplots(figsize=(12, 6))

# Terrain extérieur
ax.plot([0, LONGUEUR, LONGUEUR, 0, 0],
        [0, 0, LARGEUR_DOUBLE, LARGEUR_DOUBLE, 0], 'k')

# Filet
ax.plot([FILET_X, FILET_X], [0, LARGEUR_DOUBLE], 'k', linewidth=2)

# Couloirs simple/double
marge = (LARGEUR_DOUBLE - LARGEUR_SIMPLE) / 2
ax.plot([0, LONGUEUR], [marge, marge], 'k')
ax.plot([0, LONGUEUR], [LARGEUR_DOUBLE - marge, LARGEUR_DOUBLE - marge], 'k')

# Lignes de service
ax.plot([FILET_X - SERVICE_COURT, FILET_X - SERVICE_COURT],
        [0, LARGEUR_DOUBLE], 'k')
ax.plot([FILET_X + SERVICE_COURT, FILET_X + SERVICE_COURT],
        [0, LARGEUR_DOUBLE], 'k')

ax.plot([SERVICE_LONG_DOUBLE, SERVICE_LONG_DOUBLE],
        [0, LARGEUR_DOUBLE], 'k')
ax.plot([LONGUEUR - SERVICE_LONG_DOUBLE, LONGUEUR - SERVICE_LONG_DOUBLE],
        [0, LARGEUR_DOUBLE], 'k')

# Ligne centrale
ax.plot([0, LONGUEUR], [LARGEUR_DOUBLE / 2, LARGEUR_DOUBLE / 2], 'k')

# =====================
# JOUEURS
# =====================
ax.scatter(st.session_state.joueurs_A_x,
           st.session_state.joueurs_A_y,
           s=200, c="blue", label="Équipe A")
ax.scatter(st.session_state.joueurs_B_x,
           st.session_state.joueurs_B_y,
           s=200, c="orange", label="Équipe B")

# Labels et bâtons face à face
longueur_baton = 0.4
for i in range(2):
    # Labels
    ax.text(st.session_state.joueurs_A_x[i] + 0.1,
            st.session_state.joueurs_A_y[i], f"A{i+1}")
    ax.text(st.session_state.joueurs_B_x[i] + 0.1,
            st.session_state.joueurs_B_y[i], f"B{i+1}")

    # Bâtons côté A (vers le bas)
    
    dx = 0.5 
    droitier = 1 if joueurs_A_droitier[i] else -1
    ax.plot([st.session_state.joueurs_A_x[i], st.session_state.joueurs_A_x[i]+dx],
            [st.session_state.joueurs_A_y[i], st.session_state.joueurs_A_y[i]-droitier*longueur_baton],
            color="black", linewidth=2)

    # Bâtons côté B (vers le haut)
    dx = 0.5 
    droitier = 1 if joueurs_B_droitier[i] else -1
    ax.plot([st.session_state.joueurs_B_x[i], st.session_state.joueurs_B_x[i]-dx],
            [st.session_state.joueurs_B_y[i], st.session_state.joueurs_B_y[i]+droitier*longueur_baton],
            color="black", linewidth=2)

# =====================
# VOLANT
# =====================
ax.scatter(
    st.session_state.volant_x,
    st.session_state.volant_y,
    s=180,
    marker=icone["marker"],
    c=icone["color"],
    label=icone["label"]
)

# =====================
# DEMI-DROITES PROLONGÉES DERRIÈRE LE VOLANT
# =====================
def tracer_demi_droite(x_vol, y_vol, x_j, y_j, color):
    dx = x_j - x_vol
    dy = y_j - y_vol
    facteur_arriere = 3.3
    x_debut = x_vol - facteur_arriere * dx
    y_debut = y_vol - facteur_arriere * dy
    ax.plot([x_debut, x_j], [y_debut, y_j],
            linestyle="--", color=color, linewidth=2)

if st.session_state.volant_x < FILET_X:
    for i in range(2):
        tracer_demi_droite(st.session_state.volant_x, st.session_state.volant_y,
                            st.session_state.joueurs_B_x[i], st.session_state.joueurs_B_y[i],
                            couleur_droite)
    cote = "A (gauche)"
else:
    for i in range(2):
        tracer_demi_droite(st.session_state.volant_x, st.session_state.volant_y,
                            st.session_state.joueurs_A_x[i], st.session_state.joueurs_A_y[i],
                            couleur_droite)
    cote = "B (droite)"

# =====================
# AFFICHAGE
# =====================
ax.set_title("Simulation tactique – badminton double")
ax.set_aspect("equal")
ax.set_xlim(-0.5, LONGUEUR + 0.5)
ax.set_ylim(-0.5, LARGEUR_DOUBLE + 0.5)
ax.grid(True, linestyle=":")
ax.legend()
st.pyplot(fig)

# =====================
# INFORMATIONS SUPPLÉMENTAIRES
# =====================
st.markdown(f"""
### ℹ️ Informations
- **Côté du volant** : {cote}  
- **Type de volant** : {icone['label']}  
- **Orientation individuelle des joueurs** :  
  - A1 : {"droitier" if joueurs_A_droitier[0] else "gaucher"}  
  - A2 : {"droitier" if joueurs_A_droitier[1] else "gaucher"}  
  - B1 : {"droitier" if joueurs_B_droitier[0] else "gaucher"}  
  - B2 : {"droitier" if joueurs_B_droitier[1] else "gaucher"}
""")
