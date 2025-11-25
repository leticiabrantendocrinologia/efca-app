# ------------------------------
# EFCA – Aplicativo Completo Revisado
# Ajuste total do layout + correção definitiva do botão no celular
# ------------------------------

import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# ------------------------------ # Configuração da página # ------------------------------
st.set_page_config(
    page_title="EFCA – Comportamento Alimentar",
    page_icon="🍽️",
    layout="centered",
    menu_items={"About": "App EFCA para avaliação do fenótipo de comportamento alimentar."}
)

# ------------------------------ # CSS revisado e otimizado # ------------------------------
st.markdown("""
<style>
/* ==========================================
   CORES GERAIS DO APP
========================================== */
:root {
    --fundo: #f1e3d8;
    --botao: #b3b795;
    --botao-hover: #a4a986;
    --borda-botao: #7d816e;
}

[data-testid="stAppViewContainer"] {background-color: var(--fundo) !important;}
[data-testid="stBlock"] > div {background-color: var(--fundo) !important;}
.block-container {background-color: var(--fundo) !important; padding: 1.5rem; border-radius: 12px;}
[data-testid="stSidebar"] {background-color: var(--fundo) !important;}

body, .stApp, label, p, h1, h2, h3, h4, h5, h6 {
    color: black !important;
}

/* ==========================================
   AJUSTE REAL DO BOTÃO STREAMLIT
   Funciona em iPhone + Android + Safari + Chrome
========================================== */
.stButton > button {
    all: unset !important;
    background-color: var(--botao) !important;
    color: black !important;
    font-weight: 600 !important;
    padding: 0.9rem 1.4rem !important;
    border-radius: 10px !important;
    border: 2px solid var(--borda-botao) !important;
    width: 100% !important;
    text-align: center !important;
    display: block !important;
    font-size: 1.15rem !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background-color: var(--botao-hover) !important;
}

/* ==========================================
   BOTÕES FINAIS (WHATSAPP E REFAZER)
========================================== */
.custom-button {
    background-color: var(--botao);
    color: black !important;
    padding: 0.9rem 1.4rem;
    border-radius: 10px;
    text-align: center;
    text-decoration: none;
    display: block;
    font-size: 1.15rem;
    font-weight: 600;
    border: 2px solid var(--borda-botao);
    width: 100%;
    transition: 0.3s ease;
}

.custom-button:hover {
    background-color: var(--botao-hover);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------ # Banner com logo # ------------------------------
banner_html = """
<div style="width:100%; height:260px; position:relative; background-color:#f1e3d8;">
<img src="https://raw.githubusercontent.com/leticiabrantendocrinologia/efca-app/bf9fca05f3ee47c7425829cc2ebd26733e93b0d8/logo.png"
     style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); height:220px;">
</div>
"""
components.html(banner_html, height=260)

# ------------------------------ # Título, referência e crédito # ------------------------------
st.title("Escala EFCA: Fenótipo de Comportamento Alimentar")

st.markdown("""
> **Questionário baseado em:**
> Pineda-Wieselberg RJ, Soares AH, Napoli TF, Sarto MLL, Anger V, Formoso J, Scalissi NM, Salles JEN.
> Validation for Brazilian Portuguese of the Eating Behavior Phenotypes Scale (EFCA): Confirmatory Factor Analysis and Psychometric Properties.
> *Arch. Endocrinol. Metab.* 2025; ahead of print.
""")

st.markdown("""
<p><strong>Criado por:</strong>
<a href="https://www.instagram.com/leticiaendocrino/" target="_blank">@leticiaendocrino</a></p>
""", unsafe_allow_html=True)

st.markdown("""
Este questionário avalia aspectos do seu comportamento alimentar.
Responda com sinceridade e clique em **Ver Resultado** ao final.
""")

# ------------------------------ # Perguntas por subescala # ------------------------------
subscales = {
    "Comer Emocional": [
        "Acalmo as minhas emoções com comida.",
        "Tenho o hábito de petiscar (petiscar = fazer pequenas refeições entre as refeições principais - café da manhã, almoço, café da tarde e jantar - sem medir a quantidade do que se come).",
        "Faço lanches entre as refeições devido à ansiedade, tédio, solidão, medo, raiva, tristeza e/ou cansaço.",
        "Como nos momentos em que estou: entediado, ansioso, nervoso, triste, cansado, irritado e solitário."
    ],
    "Comer Hiperfágico": [
        "Eu como até ficar muito cheio.",
        "Peço mais comida quando termino meu prato.",
        "Costumo comer mais de um prato nas refeições principais."
    ],
    "Comer Desorganizado": [
        "Tomo café da manhã todos os dias.",
        "Pulo algumas - ou pelo menos uma - das refeições principais.",
        "Passo mais de 5 horas por dia sem comer."
    ],
    "Comer Hedônico": [
        "Quando começo a comer algo que gosto muito, tenho dificuldade em parar.",
        "Sinto-me tentado a comer quando vejo/cheiro comida que gosto.",
        "Quando me deparo com uma comida que gosto muito, mesmo sem fome, acabo comendo.",
        "Quando como algo que gosto, finalizo toda a porção."
    ],
    "Comer Compulsivo": [
        "Como muita comida em pouco tempo.",
        "Quando como algo que gosto muito, como muito rápido."
    ]
}

questions = [q for sub in subscales.values() for q in sub]
options = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]
score_map = {opt: i for i, opt in enumerate(options)}
responses = {}

# ------------------------------ # Formulário EFCA # ------------------------------
with st.form("efca_form"):
    for q in questions:
        responses[q] = st.radio(q, options)
    submitted = st.form_submit_button("Ver Resultado")

# ------------------------------ # Funções de interpretação # ------------------------------
def interpret_score(score, max_score):
    pct = score / max_score
    if pct <= 0.33:
        return "Baixo"
    elif pct <= 0.66:
        return "Moderado"
    else:
        return "Alto"

# ------------------------------ # Resultado # ------------------------------
if submitted:
    st.markdown("---")
    st.header("Resultado da EFCA")

    subscale_results = {}

    for sub, qs in subscales.items():
        score = 0
        for q in qs:
            s = score_map[responses[q]]
            if q == "Tomo café da manhã todos os dias.":
                s = (len(options) - 1) - s
            score += s

        max_sub = len(qs) * (len(options) - 1)
        subscale_results[sub] = (score, interpret_score(score, max_sub))

    st.markdown("**Resultados por subescala:**")
    for sub, (score, interp) in subscale_results.items():
        st.write(f"- {sub}: {score} pontos — {interp}")

    # ------------------------------ # Botão WhatsApp # ------------------------------
    msg = (
    "Aqui está meu resultado EFCA:
"
    + "
".join([f"{s}: {v[0]} pontos - {v[1]}" for s, v in subscale_results.items()])
)
link = "https://api.whatsapp.com/send?phone=+5531996515760&text=" + urllib.parse.quote(msg)

    st.markdown(
        f'<a class="custom-button" href="{link}" target="_blank">📩 Enviar resultado pelo WhatsApp</a>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ------------------------------ # Botão Refazer # ------------------------------
    st.markdown(
        '<a class="custom-button" href="#" onclick="window.location.reload();">🔄 Refazer o formulário</a>',
        unsafe_allow_html=True
    )
