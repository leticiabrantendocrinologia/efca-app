import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(layout="wide")

# HTML + CSS para banner full-width com logo
banner_html = """
<div style="
    width: 100%;
    height: 300px;
    background-color: #b3b795;
    background-image: url('logo.png'); 
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
">
</div>
"""

# Renderiza o banner
components.html(banner_html, height=300)

# Título do app abaixo do banner
st.title("🧠 EFCA – Escala de Fenótipo de Comportamento Alimentar")
import streamlit as st

# ---- ESTILO PERSONALIZADO (FUNDO VERDE + AJUSTES DE LAYOUT) ----
st.markdown("""
<style>
/* Fundo geral da página */
.main {
    background-color: #b3b795 !important; 
}

/* Caixa branca onde ficam os widgets */
.stApp {
    background-color: #b3b795 !important;
}

/* Cards e caixas internas padrão do Streamlit */
.block-container {
    background-color: #ffffffcc; /* branco com leve transparência */
    padding: 2rem 3rem;
    border-radius: 12px;
}

/* Estilo de botões */
.stButton>button {
    background-color: #556b2f !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="EFCA – Comportamento Alimentar",
    page_icon="🍽️",
    layout="centered",
    menu_items={
        "About": "App EFCA para avaliação do fenótipo de comportamento alimentar."
    }
)

# Logo (se você tiver uma imagem) — substitua pela URL da sua logo
# st.image("https://link-da-sua-logo.png", width=120)

# Título + descrição
st.title("Escala EFCA: Fenótipo de Comportamento Alimentar")
st.markdown("""
Bem-vindo! Este questionário avalia aspectos do seu comportamento alimentar segundo a EFCA.
Responda com sinceridade e clique em **Enviar** para ver seus resultados.
""")

# Perguntas e opções
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

# Formulário
with st.form("efca_form"):
    for q in questions:
        responses[q] = st.radio(q, options)
    submitted = st.form_submit_button("Enviar")

if submitted:
    # Pontuação
    total_score = sum(score_map[r] for r in responses.values())
    max_score = len(questions) * (len(options) - 1)

    # Layout de resultado
    st.markdown("---")
    st.header("Resultado da EFCA")
    st.subheader(f"Pontuação total: **{total_score} / {max_score}**")

    # Barra visual
    progress = total_score / max_score
    st.progress(progress)

    # Interpretação
    if total_score <= 18:
        st.success("Baixo fenótipo de comportamento alimentar disfuncional.")
    elif total_score <= 36:
        st.warning("Fenótipo moderado / intermediário.")
    else:
        st.error("Alto fenótipo de comportamento alimentar disfuncional.")

    st.markdown("**Suas respostas foram:**")
    # Mostrar respostas em duas colunas para melhor visualização
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

    # Talvez adicionar botão para “Resetar” respostas?
    if st.button("Refazer o formulário"):
        st.experimental_rerun()
