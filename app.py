import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =====================
# CONFIG STREAMLIT
# =====================
st.set_page_config(page_title="Simulation Badminton", layout="wide")
st.title("🏸 Simulation tactique de badminton")

# =====================
# INTERFACE UTILISATEUR
# =====================
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🎛️ Paramètres")
    resimuler = st.button("🔄 Resimuler la situation")

    type_volant = st.radio(
        "Type de volant",
        ["haut", "à plat", "bas"],
        index=0
    )

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
# INITIALISATION / RESIMULATION
# =====================
if resimuler or "init" not in st.session_state:
    st.session_state.init = True

    # Équipe A (gauche)
    st.session_state.joueurs_A_x = np.random.uniform(0.5, FILET_X - 0.5, 2)
    st.session_state.joueurs_A_y = np.random.uniform(0.5, LARGEUR_DOUBLE - 0.5, 2)

    # Équipe B (droite)
    st.session_state.joueurs_B_x = np.random.uniform(FILET_X + 0.5, LONGUEUR - 0.5, 2)
    st.session_state.joueurs_B_y = np.random.uniform(0.5, LARGEUR_DOUBLE - 0.5, 2)

    # Volant (position uniquement)
    st.session_state.volant_x = np.random.uniform(0.3, LONGUEUR - 0.3)
    st.session_state.volant_y = np.random.uniform(0.3, LARGEUR_DOUBLE - 0.3)

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

for i in range(2):
    ax.text(st.session_state.joueurs_A_x[i] + 0.1,
            st.session_state.joueurs_A_y[i], f"A{i+1}")
    ax.text(st.session_state.joueurs_B_x[i] + 0.1,
            st.session_state.joueurs_B_y[i], f"B{i+1}")

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
    # Vecteur volant -> joueur
    dx = x_j - x_vol
    dy = y_j - y_vol
    
    # Prolongement derrière le volant
    facteur_arriere = 2.3  # longueur derrière le volant
    x_debut = x_vol - facteur_arriere * dx
    y_debut = y_vol - facteur_arriere * dy
    
    ax.plot([x_debut, x_j], [y_debut, y_j],
            linestyle="--", color=color, linewidth=2)

if st.session_state.volant_x < FILET_X:
    # Volant côté A → vers joueurs B
    for i in range(2):
        tracer_demi_droite(st.session_state.volant_x, st.session_state.volant_y,
                            st.session_state.joueurs_B_x[i], st.session_state.joueurs_B_y[i],
                            couleur_droite)
    cote = "A (gauche)"
else:
    # Volant côté B → vers joueurs A
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

st.markdown(f"""
### ℹ️ Informations
- **Côté du volant** : {cote}  
- **Type de volant** : {icone['label']}
""")
