import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Simulateur de gain", page_icon="💰", layout="wide")

# ─────────────────────────────────────────────────────────────
# STYLE CSS — même thème marron deux tons que les autres pages
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    :root {
        --brown-dark: #3E2723;
        --brown: #6D4C41;
        --brown-mid: #8D6E63;
        --tan: #EFE3D7;
        --cream: #FBF7F2;
        --gold: #D9A441;
        --terracotta: #C0625B;
        --grey: #4A4038;
    }

    .stApp { background: var(--tan); }
    .block-container { padding-top: 1.2rem; max-width: 100%; }

    /* ── Filet de sécurité : texte natif Streamlit (captions, libellés de
       widgets, markdown brut non encadré) forcé en couleur foncée.
       :not([class]) ne cible que les éléments sans classe, donc ne touche
       jamais mes blocs personnalisés (toujours classés). ── */
    [data-testid="stMarkdownContainer"] p:not([class]),
    [data-testid="stMarkdownContainer"] li:not([class]),
    [data-testid="stMarkdownContainer"] span:not([class]),
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: var(--grey) !important;
    }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: var(--brown-dark) !important;
        font-weight: 600;
    }
    .note-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 8px;
        padding: 0.55rem 0.9rem;
        color: var(--grey) !important;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: var(--brown-dark) !important; }
    section[data-testid="stSidebar"] * { color: #F1E4D8 !important; }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background-color: var(--gold) !important;
        color: var(--brown-dark) !important;
        font-weight: 700 !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] a:hover {
        background-color: rgba(217, 164, 65, 0.25) !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: var(--brown) !important;
        border-color: var(--brown-mid) !important;
    }

    /* Barre supérieure Streamlit */
    header[data-testid="stHeader"] { background: var(--brown-dark) !important; }
    header[data-testid="stHeader"] * { color: #F1E4D8 !important; }

    /* En-tête de page, encadré et centré */
    .hero-box {
        background: var(--brown-dark);
        border-radius: 16px;
        padding: 1.4rem 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(62, 39, 35, 0.3);
    }
    .hero-title { font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin: 0; }
    .hero-subtitle { font-size: 0.98rem; color: #EAD9C8; margin-top: 0.4rem; }

    /* Titres de section : toujours encadrés, donc toujours lisibles */
    .section-header-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-left: 6px solid var(--gold);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0 1rem 0;
    }
    .section-header { font-size: 1.2rem; font-weight: 700; color: var(--brown-dark); margin: 0; }

    /* Blocs pleine largeur */
    .full-block {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        color: var(--grey);
        line-height: 1.7;
    }

    /* Résultat de prédiction */
    .result-banner {
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        font-size: 1.15rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .result-fraud { background: #F6DEDC; color: #7A2E27; border: 2px solid var(--terracotta); }
    .result-legit { background: #E3EEE0; color: #1B5E20; border: 2px solid #6B9E6E; }

    /* Métriques natives st.metric */
    div[data-testid="stMetric"] {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 12px;
        padding: 0.8rem;
    }
    div[data-testid="stMetric"] label { color: var(--brown) !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: var(--brown-dark) !important; }

    /* Bouton principal */
    button[kind="primary"] {
        background-color: var(--brown-dark) !important;
        border-color: var(--brown-dark) !important;
    }
    button[kind="primary"]:hover {
        background-color: var(--brown) !important;
        border-color: var(--brown) !important;
    }
</style>
""", unsafe_allow_html=True)


def section_header(icon, text):
    st.markdown(
        f'<div class="section-header-box"><p class="section-header">{icon} {text}</p></div>',
        unsafe_allow_html=True,
    )


def fcfa(x):
    """Formate un montant en FCFA avec séparateur de milliers."""
    return f"{x:,.0f}".replace(",", "\u00a0") + "\u00a0FCFA"


st.markdown("""
<div class="hero-box">
    <p class="hero-title">💰 Simulateur de gain</p>
    <p class="hero-subtitle">Estimez ce que la détection automatique peut faire économiser à votre structure : renseignez votre activité et vos coûts.</p>
</div>
""", unsafe_allow_html=True)

# ── Profils de performance (résultats du notebook, jeu de test, seuil 0,5) ──
# Jeu de test : 56 962 transactions dont 98 fraudes et 56 864 légitimes
N_FRAUDES_TEST = 98
N_LEGIT_TEST = 56864
PROFILS = {
    "Random Forest": {"tp": 80, "fp": 17},
    "XGBoost (SMOTE)": {"tp": 85, "fp": 33},
    "Personnalisé": {"tp": 80, "fp": 17},
}

# ── Hypothèses ─────────────────────────────────────────────
section_header("⚙️", "Hypothèses de simulation")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Votre activité**")
    n_trans = st.number_input("Transactions par mois", min_value=1_000, value=1_000_000, step=10_000)
    taux_fraude = st.number_input("Taux de fraude (%)", min_value=0.001, max_value=10.0, value=0.17, step=0.01, format="%.3f",
                                  help="0,17 % = taux du jeu de données de référence. Remplacez par le vôtre.")

with col2:
    st.markdown("**Vos coûts**")
    perte_fraude = st.number_input("Perte moyenne par fraude (FCFA)", min_value=0, value=100_000, step=5_000,
                                   help="Hypothèse à remplacer par la valeur réelle de votre structure.")
    cout_alerte = st.number_input("Coût d'une fausse alerte (FCFA)", min_value=0, value=1_000, step=100,
                                  help="Temps d'un agent pour vérifier + gêne client.")
    cout_systeme = st.number_input("Coût mensuel du système (FCFA)", min_value=0, value=0, step=50_000)

with col3:
    st.markdown("**Performance du modèle**")
    profil = st.selectbox("Profil du modèle", list(PROFILS.keys()))
    p = PROFILS[profil]
    rappel_def = 100 * p["tp"] / N_FRAUDES_TEST
    fpr_def = 100 * p["fp"] / N_LEGIT_TEST
    rappel = st.number_input("Rappel (% de fraudes détectées)", 0.0, 100.0, round(rappel_def, 2), 0.5,
                             key=f"rappel_{profil}")
    fpr = st.number_input("Taux de fausses alertes (% des transactions légitimes)", 0.0, 100.0,
                          round(fpr_def, 4), 0.01, format="%.4f", key=f"fpr_{profil}")

# ── Calculs ────────────────────────────────────────────────
n_fraudes = n_trans * taux_fraude / 100
n_legit = n_trans - n_fraudes
detectees = n_fraudes * rappel / 100
manquees = n_fraudes - detectees
fausses_alertes = n_legit * fpr / 100

perte_sans = n_fraudes * perte_fraude
perte_fraudes_restantes = manquees * perte_fraude
perte_alertes = fausses_alertes * cout_alerte
cout_avec = perte_fraudes_restantes + perte_alertes + cout_systeme
gain = perte_sans - cout_avec
reduction = 100 * gain / perte_sans if perte_sans > 0 else 0
precision_impl = 100 * detectees / (detectees + fausses_alertes) if (detectees + fausses_alertes) > 0 else 0

# ── Résultats ──────────────────────────────────────────────
st.divider()
section_header("📊", "Résultat estimé par mois")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Fraudes attendues", f"{n_fraudes:,.0f}".replace(",", "\u00a0"))
c2.metric("Fraudes détectées", f"{detectees:,.0f}".replace(",", "\u00a0"))
c3.metric("Fraudes manquées", f"{manquees:,.0f}".replace(",", "\u00a0"))
c4.metric("Fausses alertes", f"{fausses_alertes:,.0f}".replace(",", "\u00a0"),
          help=f"Précision implicite : {precision_impl:.1f} % des alertes sont de vraies fraudes.")

g1, g2, g3 = st.columns(3)
g1.metric("Pertes sans modèle", fcfa(perte_sans))
g2.metric("Coût total avec modèle", fcfa(cout_avec))
g3.metric("Gain net estimé", fcfa(gain), delta=f"{reduction:.1f} %")

fig = go.Figure()
fig.add_bar(name="Fraudes non détectées", x=["Sans modèle", "Avec modèle"],
            y=[perte_sans, perte_fraudes_restantes], marker_color="#C0625B")
fig.add_bar(name="Fausses alertes", x=["Sans modèle", "Avec modèle"],
            y=[0, perte_alertes], marker_color="#D9A441")
fig.add_bar(name="Coût du système", x=["Sans modèle", "Avec modèle"],
            y=[0, cout_systeme], marker_color="#6D4C41")
fig.update_layout(barmode="stack", height=360, paper_bgcolor="#FBF7F2", plot_bgcolor="#FBF7F2",
                  font_color="#3E2723", yaxis_title="FCFA par mois", margin=dict(t=30, b=10))
st.plotly_chart(fig, width="stretch")

if gain > 0:
    st.success(f"Avec ces hypothèses, la détection ferait économiser environ {fcfa(gain)} par mois "
               f"({reduction:.1f} % des pertes liées à la fraude).")
else:
    st.warning("Avec ces hypothèses, le coût des fausses alertes et du système dépasse les pertes évitées : "
               "il faudrait ajuster le seuil de détection ou réduire le coût d'une alerte.")

st.markdown(
    '<div class="note-box"><b>À lire avant de conclure :</b> simulation illustrative. Le rappel et le taux de fausses alertes '
    'proviennent des tests du notebook (jeu de données européen de référence, seuil 0,5) et sont supposés constants quel que soit '
    'le taux de fraude. Les montants par défaut sont des hypothèses. Sur les données réelles d\'une structure, '
    'le modèle doit être réentraîné et ces valeurs recalibrées lors d\'un pilote.</div>',
    unsafe_allow_html=True,
)
