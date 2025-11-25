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
# CSS para fundo uniforme e estilo
# ------------------------------
st.markdown("""
<style>
/* Fundo geral do aplicativo (página inteira) */
[data-testid="stAppViewContainer"] {
    background-color: #f1e3d8 !important;
}

/* Container principal do app (onde ficam widgets, título, formulário) */
[data-testid="stBlock"] > div {
    background-color: #f1e3d8 !important;
}

/* Container interno do Streamlit (blocos / cards) */
.block-container {
    background-color: #f1e3d8 !important;
    padding: 2rem 3rem;
    border-radius: 12px;
}

/* Sidebar (se você usar) */
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
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Banner com logo
# ------------------------------
banner_html = """
<div style="
    width: 100%;
    height: 500px;  /* altura do topo */
    position: relative;
    background-color: #f1e3d8;  /* fundo igual ao da logo */
">
    <img src="https://raw.githubusercontent.com/leticiabrantendocrinologia/efca-app/bf9fca05f3ee47c7425829cc2ebd26733e93b0d8/logo.png"
         style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                height: 250px;">
</div>
"""
components.html(banner_html, height=300)

# ------------------------------
# Título, referência científica e crédito
# ------------------------------
st.title("Escala EFCA: Fenótipo de Comportamento Alimentar")

# Referência científica abaixo do título
st.markdown("""
> **Questionário baseado em:**  
> Pineda-Wieselberg RJ, Soares AH, Napoli TF, Sarto MLL, Anger V, Formoso J, Scalissi NM, Salles JEN.  
> Validation for Brazilian Portuguese of the Eating Behavior Phenotypes Scale (EFCA): Confirmatory Factor Analysis and Psychometric Properties.  
> *Arch. Endocrinol. Metab.* 2025; ahead of print.
""")

# Crédito / Instagram
st.markdown("""
<p><strong>Criado por:</strong> <a href="https://www.instagram.com/leticiaendocrino/" target="_blank">@leticiaendocrino</a></p>
""", unsafe_allow_html=True)

# Descrição do questionário
st.markdown("""
Bem-vindo! Este questionário avalia aspectos do seu comportamento alimentar segundo a EFCA.
Responda com sinceridade e clique em **Enviar** para ver seus resultados.
""")

# ------------------------------
# Perguntas e opções
# ------------------------------
questions = {
    "Eu como rápido.": [],
    "Eu como até me sentir desconfortável.": [],
    "Eu como mesmo quando não estou com fome.": [],
    "Eu sinto que perco o controle quando começo a comer.": [],
    "Belisco comida ao longo do dia.": [],
    "Eu como escondido.": [],
    "Eu sinto fome intensa súbita.": [],
    "Tenho dificuldade de parar de comer alimentos palatáveis.": [],
    "Como para lidar com emoções negativas.": [],
    "Tenho vontade incontrolável de comer certos alimentos.": [],
    "Sinto que preciso comer para me acalmar.": [],
    "Quando começo a comer, exagero sem perceber.": [],
    "Eu como por tédio.": [],
    "Como mais quando estou estressado(a).": [],
    "Fico pensando em comida mesmo após já ter comido.": [],
    "Busco comida mesmo sem necessidade fisiológica.": [],
    "Fico ansiando por comida durante o dia.": [],
    "Sinto culpa depois de comer em excesso.": [],
}

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
if submitted:
    total_score = sum(score_map[r] for r in responses.values())
    max_score = len(questions) * (len(options) - 1)

    st.markdown("---")
    st.header("Resultado da EFCA")
    st.subheader(f"Pontuação total: **{total_score} / {max_score}**")

    # Barra de progresso
    progress = total_score / max_score
    st.progress(progress)

    # Interpretação
    if total_score <= 18:
        st.success("Baixo fenótipo de comportamento alimentar disfuncional.")
    elif total_score <= 36:
        st.warning("Fenótipo moderado / intermediário.")
    else:
        st.error("Alto fenótipo de comportamento alimentar disfuncional.")

    # Mostrar respostas em duas colunas
    st.markdown("**Suas respostas foram:**")
    col1, col2 = st.columns(2)
    items = list(responses.items())
    for i, (q, resp) in enumerate(items):
        if i % 2 == 0:
            col1.write(f"- {q}: **{resp}**")
        else:
            col2.write(f"- {q}: **{resp}**")

    # Salvar respostas
    df = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pontuacao": total_score,
        **responses
    }])
    try:
        old = pd.read_csv("efca_respostas.csv")
        new = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        new = df
    new.to_csv("efca_respostas.csv", index=False)
    st.write("✅ Suas respostas foram salvas.")

    # Botão para exportar como CSV
    csv = new.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar resultados (CSV)",
        data=csv,
        file_name="meus_resultados_efca.csv",
        mime="text/csv"
    )

    # Botão para resetar o formulário
    if st.button("Refazer o formulário"):
        st.experimental_rerun()
