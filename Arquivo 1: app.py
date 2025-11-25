# ------------------------------
# Importações
# ------------------------------
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(
    page_title="EFCA – Comportamento Alimentar",
    page_icon="🍽️",
    layout="wide",
    menu_items={
        "About": "App EFCA para avaliação do fenótipo de comportamento alimentar."
    }
)

# ------------------------------
# CSS personalizado
# ------------------------------
st.markdown("""
<style>
/* Fundo geral do aplicativo */
[data-testid="stAppViewContainer"] {
    background-color: #f1e3d8 !important;
}

/* Container principal */
[data-testid="stBlock"] > div {
    background-color: #f1e3d8 !important;
}

/* Container interno do Streamlit */
.block-container {
    background-color: #f1e3d8 !important;
    padding: 2rem 3rem;
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f1e3d8 !important;
}

/* Botões */
.stButton>button {
    background-color: #556b2f !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 1rem !important;
}

/* Diminui espaço acima do título */
h1 {
    margin-top: 0.5rem;
}

/* Texto preto em todo o app */
body, .stApp, .block-container, h1, h2, h3, h4, h5, h6, p, label, .css-1kyxreq {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Banner com logo
# ------------------------------
banner_html = """
<div style="
    width: 100%;
    height: 220px;  
    position: relative;
    background-color: #f1e3d8;
">
    <img src="https://raw.githubusercontent.com/leticiabrantendocrinologia/efca-app/bf9fca05f3ee47c7425829cc2ebd26733e93b0d8/logo.png"
         style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -40%);
                height: 180px;">
</div>
"""
components.html(banner_html, height=220)

# ------------------------------
# Título, referência e crédito
# ------------------------------
st.title("Escala EFCA: Fenótipo de Comportamento Alimentar")

st.markdown("""
> **Questionário baseado em:**  
> Pineda-Wieselberg RJ, Soares AH, Napoli TF, Sarto MLL, Anger V, Formoso J, Scalissi NM, Salles JEN.  
> Validation for Brazilian Portuguese of the Eating Behavior Phenotypes Scale (EFCA): Confirmatory Factor Analysis and Psychometric Properties.  
> *Arch. Endocrinol. Metab.* 2025; ahead of print.
""")

st.markdown("""
<p><strong>Criado por:</strong> <a href="https://www.instagram.com/leticiaendocrino/" target="_blank">@leticiaendocrino</a></p>
""", unsafe_allow_html=True)

st.markdown("""
Bem-vindo! Este questionário avalia aspectos do seu comportamento alimentar segundo a EFCA.
Responda com sinceridade e clique em **Enviar** para ver seus resultados.
""")

# ------------------------------
# Perguntas e subescalas
# ------------------------------
# Aqui definimos as subescalas
subscales = {
    "Comer Emocional": [
        "Como para lidar com emoções negativas.",
        "Sinto que preciso comer para me acalmar.",
        "Como mais quando estou estressado(a)."
    ],
    "Hiperfagia": [
        "Eu como rápido.",
        "Eu como até me sentir desconfortável.",
        "Eu sinto fome intensa súbita."
    ],
    "Comer Hedônico": [
        "Tenho dificuldade de parar de comer alimentos palatáveis.",
        "Tenho vontade incontrolável de comer certos alimentos."
    ],
    "Comer Desorganizado": [
        "Belisco comida ao longo do dia.",
        "Eu como escondido.",
        "Fico pensando em comida mesmo após já ter comido.",
        "Busco comida mesmo sem necessidade fisiológica."
    ],
    "Comer Compulsivo": [
        "Eu sinto que perco o controle quando começo a comer.",
        "Quando começo a comer, exagero sem perceber.",
        "Eu como por tédio.",
        "Sinto culpa depois de comer em excesso."
    ]
}

# Todas as perguntas
questions = [q for sub in subscales.values() for q in sub]

options = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]
score_map = {opt: i for i, opt in enumerate(options)}
responses = {}

# ------------------------------
# Formulário EFCA
# ------------------------------
with st.form("efca_form"):
    for q in questions:
        responses[q] = st.radio(q, options)
    submitted = st.form_submit_button("Enviar")

# ------------------------------
# Processamento de resultados
# ------------------------------
def interpret_score(score, max_score):
    pct = score / max_score
    if pct <= 0.33:
        return "Baixo"
    elif pct <= 0.66:
        return "Moderado"
    else:
        return "Alto"

if submitted:
    st.markdown("---")
    st.header("Resultado da EFCA")

    # Calcular resultados por subescala
    subscale_results = {}
    for sub, qs in subscales.items():
        score = sum(score_map[responses[q]] for q in qs)
        max_subscore = len(qs) * (len(options) - 1)
        interpretation = interpret_score(score, max_subscore)
        subscale_results[sub] = (score, interpretation)

    # Mostrar resultados
    st.markdown("**Resultados por subescala:**")
    for sub, (score, interpretation) in subscale_results.items():
        st.write(f"- {sub}: {score} pontos - {interpretation}")

    # Salvar respostas
    df = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **responses
    }])
    try:
        old = pd.read_csv("efca_respostas.csv")
        new = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        new = df
    new.to_csv("efca_respostas.csv", index=False)
    st.write("✅ Suas respostas foram salvas.")

    # Botão para exportar CSV
    csv = new.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar resultados (CSV)",
        data=csv,
        file_name="meus_resultados_efca.csv",
        mime="text/csv"
    )

    # Botão para refazer
    if st.button("Refazer o formulário"):
        st.experimental_rerun()
